from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy, reverse
from .forms import Checar_PedidoForms, ClienteRegistrarForms, ClienteEntrarForms, EnderecoRegistrarForms
from .models import *
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
import os
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import serializers, status
import requests
import decimal
# import json
from django_teste import settings

class AdminRequireMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request,*args,**kwargs)

class LojaMixin(object):
    def dispatch(self,request,*args,**kwargs):
        carro_id = request.session.get("carro_id")
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            if request.user.is_authenticated and request.user.cliente:
                carro_obj.cliente = request.user.cliente
                carro_obj.save()
        else:
            carro_obj = Carro.objects.create(total=0)
            carro_obj.save()
            self.request.session['carro_id'] = carro_obj.id
        return super().dispatch(request,*args,**kwargs)

class LogedMixin(object):
    def dispatch(self,request,*args, **kwargs):
        next = request.path
        if request.user.is_authenticated and request.user.cliente:
            pass
        else:
            return redirect(f"/entrar/?next={next}")
        return super().dispatch(request,*args, **kwargs)

class CarroComItemsMixin(object):
    def dispatch(self,request,*args, **kwargs):
        carro_id = request.session.get("carro_id")
        carro_obj = Carro.objects.get(id=carro_id)

        if carro_obj.total:
            pass
        else:
            return redirect("lojaapp:home")
        return super().dispatch(request,*args, **kwargs)

class PedidoExisteMixin(object):
    def dispatch(self,request,*args, **kwargs):
        carro_id = request.session.get("carro_id")
        carro_obj = Carro.objects.get(id=carro_id)
        pedido = Pedido_order.objects.filter(carro=carro_obj)

        if pedido:
            pass
        else:
            return redirect("lojaapp:home")
        return super().dispatch(request,*args, **kwargs)

class BaseContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['todoscategorias'] = Categoria.objects.all()
        context['footer'] = Empresa.objects.all()

        return context

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class HomeView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "home.html"

    def preprocessar_precos(self, produtos):
        for produto in produtos:
            venda_parts = str(produto.venda).split('.')
            produto.integer_part = venda_parts[0]
            produto.decimal_part = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
        return produtos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_produtos = Produto.objects.all().order_by("-id")
        produto_list = self.preprocessar_precos(all_produtos)

        paginator = Paginator(produto_list, 20)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        context['mais_vendidos'] = Produto.objects.all().order_by("-quantidade_vendas")[:7]

        context['banners'] = Banner.objects.all()

        return context

class SobreView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['empresa'] = Empresa.objects.all()
        context["enderecosLojas"] = Endereco.objects.filter(cliente=Cliente.objects.get(nome="Casa", sobrenome="HG"))
        context["mapsKey"] = settings.GOOGLE_MAPS_KEY

        return context

class ContatoView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "contato.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.all()

        return context

class TodosProdutosView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "todos-produtos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class ProdutosDetalheView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "produtodetalhe.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']

        produto = Produto.objects.get(slug=url_slug)
        context['produto'] = produto

        context['fotos_produtos'] = produto.images.all() #Fotos_Produto.objects.filter(produto=produto)

        produto.visualizacao += 1
        produto.save()

        return context

class AddCarroView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):
        produto_id = self.kwargs['prod_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carro_id = self.request.session.get("carro_id",None)
        try:
            carro_obj = Carro.objects.get(id=carro_id)
            produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)

            if produto_no_carro.exists():
                carroproduto = produto_no_carro.last()
                carroproduto.quantidade += 1
                carroproduto.subtotal += produto_obj.venda
                carroproduto.save()

            else:
                carroproduto = CarroProduto.objects.create(
                carro = carro_obj,
                produto = produto_obj,
                preco_unitario = produto_obj.venda,
                quantidade = 1,
                subtotal = produto_obj.venda

                )

            carro_obj.total += produto_obj.venda
            carro_obj.save()


        except Carro.DoesNotExist:
            carro_obj = Carro.objects.create(total=0)
            self.request.session['carro_id'] = carro_obj.id
            carroproduto = CarroProduto.objects.create(
                carro=carro_obj,
                produto=produto_obj,
                preco_unitario=produto_obj.venda,
                quantidade=1,
                subtotal=produto_obj.venda

            )
            carro_obj.total += produto_obj.venda
            carro_obj.save()

        return redirect("lojaapp:home")
    
class AddCarroView2(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "produtodetalhe.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_id = self.kwargs['prod_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carro_id = self.request.session.get("carro_id",None)
        try:
            carro_obj = Carro.objects.get(id=carro_id)
            produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)

            if produto_no_carro.exists():
                carroproduto = produto_no_carro.last()
                carroproduto.quantidade += 1
                carroproduto.subtotal += produto_obj.venda
                carroproduto.save()

            else:
                carroproduto = CarroProduto.objects.create(
                carro = carro_obj,
                produto = produto_obj,
                preco_unitario = produto_obj.venda,
                quantidade = 1,
                subtotal = produto_obj.venda

                )

            carro_obj.total += produto_obj.venda
            carro_obj.save()


        except Carro.DoesNotExist:
            carro_obj = Carro.objects.create(total=0)
            self.request.session['carro_id'] = carro_obj.id
            carroproduto = CarroProduto.objects.create(
                carro=carro_obj,
                produto=produto_obj,
                preco_unitario=produto_obj.venda,
                quantidade=1,
                subtotal=produto_obj.venda

            )
            carro_obj.total += produto_obj.venda
            carro_obj.save()

        return context
    
class AddCarroQuantView(LojaMixin, BaseContextMixin, TemplateView):
    def get(self,request,*arg,**kwargs):
        produto_id = request.GET.get("prod_id")
        produto_quantidade = int(request.GET.get("quantidade"))

        produto_obj = Produto.objects.get(id=produto_id)
        carro_id = self.request.session.get("carro_id",None)
        try:
            carro_obj = Carro.objects.get(id=carro_id)
            produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)

            if produto_no_carro.exists():
                carroproduto = produto_no_carro.last()
                carroproduto.quantidade += produto_quantidade
                carroproduto.subtotal += (produto_obj.venda * produto_quantidade)
                carroproduto.save()

            else:
                carroproduto = CarroProduto.objects.create(
                carro = carro_obj,
                produto = produto_obj,
                preco_unitario = produto_obj.venda,
                quantidade = produto_quantidade,
                subtotal = (produto_obj.venda * produto_quantidade)

                )

            carro_obj.total += (produto_obj.venda * produto_quantidade)
            carro_obj.save()


        except Carro.DoesNotExist:
            carro_obj = Carro.objects.create(total=0)
            self.request.session['carro_id'] = carro_obj.id
            carroproduto = CarroProduto.objects.create(
                carro = carro_obj,
                produto = produto_obj,
                preco_unitario = produto_obj.venda,
                quantidade = produto_quantidade,
                subtotal = (produto_obj.venda * produto_quantidade)

            )
            carro_obj.total += (produto_obj.venda * produto_quantidade)
            carro_obj.save()

        # return context
        return redirect("lojaapp:home")

class MeuCarroView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "meucarro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro_id = Carro.objects.get(id=carro_id)
        else:
            carro_id = None
        context["carro"] = carro_id
        return context

class ManipularCarroView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):

        cp_id = self.kwargs["cp_id"]
        acao = request.GET.get("acao")
        cp_obj = CarroProduto.objects.get(id=cp_id)
        carro_obj = cp_obj.carro

        if acao =="inc":
            cp_obj.quantidade += 1
            cp_obj.subtotal += cp_obj.preco_unitario
            cp_obj.save()
            carro_obj.total += cp_obj.preco_unitario
            carro_obj.save()
        elif acao =="dcr":
            cp_obj.quantidade -= 1
            cp_obj.subtotal -= cp_obj.preco_unitario
            cp_obj.save()
            carro_obj.total -= cp_obj.preco_unitario
            carro_obj.save()
            if cp_obj.quantidade <= 0:
                cp_obj.delete()
        elif acao =="rmv":
            carro_obj.total -= cp_obj.subtotal
            carro_obj.save()
            cp_obj.delete()

        else:
            pass
        return redirect("lojaapp:meucarro")

class LimparCarroView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):

        carro_id = request.session.get("carro_id",None)
        if carro_id:
            carro = Carro.objects.get(id=carro_id)
            carro.carroproduto_set.all().delete()
            carro.total = 0
            carro.save()
        return redirect("lojaapp:meucarro")

class FormaDeEntregaView(LogedMixin, LojaMixin, CarroComItemsMixin, BaseContextMixin, CreateView):
    template_name = "forma_de_entrega.html"
    form_class = Checar_PedidoForms
    success_url = reverse_lazy("lojaapp:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
        else:
            carro_obj = None
        context["carro"] = carro_obj

        context["enderecos"] = Endereco.objects.filter(cliente=self.request.user.cliente).order_by("-id")
        context["enderecosLojas"] = Endereco.objects.filter(cliente=Cliente.objects.get(nome="Casa", sobrenome="HG"))

        return context
    
def pedido_carro_endereco(request):
    if request.method == 'POST':
        try:
            # if Pedido_order.objects.filter(carro=request.POST["carro_id"]):
                # print(request.POST)
                # Pedido_order.objects.get(carro=request.POST["carro_id"]).delete()

            usuario = User.objects.get(username=request.user.username)
            cliente = Cliente.objects.get(user=usuario)
            nome_cliente = f"{cliente.nome} {cliente.sobrenome}"
            cpf_cnpj = cliente.cpf_ou_cnpj_formatado
            # codigo_cliente = 
            telefone = cliente.telefone
            email = cliente.email

            carro = Carro.objects.get(id=request.POST["carro_id"])
            pedido_status = "Pedido em Andamento"
            total_bruto = carro.total
            frete = decimal.Decimal(request.POST["frete"])
            total_final = (decimal.Decimal(total_bruto) + decimal.Decimal(frete))
            
            endereco_envio = Endereco.objects.get(id=request.POST["local_entrega"])
            if endereco_envio.complemento and endereco_envio.numero:
                endereco_envio_formatado = f"{endereco_envio.rua} {endereco_envio.numero} {endereco_envio.complemento}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"
            elif endereco_envio.numero:
                endereco_envio_formatado = f"{endereco_envio.rua} {endereco_envio.numero}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"
            elif endereco_envio.complemento:
                endereco_envio_formatado = f"{endereco_envio.rua} {endereco_envio.complemento}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"
            else:
                endereco_envio_formatado = f"{endereco_envio.rua}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"

            
            if Pedido_order.objects.filter(carro=request.POST["carro_id"]):
                pedido = Pedido_order.objects.get(carro=request.POST["carro_id"])
                pedido.endereco_envio = endereco_envio
                pedido.endereco_envio_formatado = endereco_envio_formatado
                pedido.frete = frete
                pedido.total_final = total_final
            else:
                pedido = Pedido_order.objects.create(cliente=cliente, nome_cliente=nome_cliente, cpf_cnpj=cpf_cnpj, telefone=telefone, email=email, carro=carro, pedido_status=pedido_status, total_bruto=total_bruto, total_final=total_final, frete=frete, endereco_envio=endereco_envio, endereco_envio_formatado=endereco_envio_formatado)
            pedido.save()

            return redirect('lojaapp:checkout')
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

class CheckOutView(LogedMixin, LojaMixin, CarroComItemsMixin, PedidoExisteMixin, BaseContextMixin, CreateView):
    template_name = "processar.html"
    form_class = Checar_PedidoForms
    success_url = reverse_lazy("lojaapp:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
        else:
            carro_obj = None
        context["carro"] = carro_obj
        context["pedido"] = Pedido_order.objects.get(carro=carro_obj)

        return context

    def form_valid(self,form):
        carro_id = self.request.session.get("carro_id")
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            form.instance.carro = carro_obj
            form.instance.subtotal = carro_obj.total
            form.instance.desconto = 0
            form.instance.total = carro_obj.total
            form.instance.pedido_status = "Pedido Recebido"
            del self.request.session['carro_id']
        else:
            return redirect("lojaapp:home")
        return super().form_valid(form)

def pedido_carro_pagamento(request):
    if request.method == 'POST':
        try:
            # print(request.POST)
            # usuario = User.objects.get(username=request.user.username)

            # Termina de preencher os dados de pagamento
            pedido = Pedido_order.objects.get(id=request.POST["pedido_id"])

            pedido.local_de_pagamento = request.POST["local_pagamento"]
            if "metodo_pagamento" in request.POST:
                pedido.forma_de_pagamento = request.POST["metodo_pagamento"]

                if "parcelas" in request.POST:
                    pedido.parcelas = request.POST["parcelas"]
                    pedido.valor_parcela = pedido.total_final / decimal.Decimal(request.POST["parcelas"])
                else:
                    pedido.parcelas = 1
                    pedido.valor_parcela = pedido.total_final
            else:
                pedido.forma_de_pagamento = "dinheiro"
                pedido.parcelas = 1
                pedido.valor_parcela = pedido.total_final

            pedido.pedido_status = "Pedido Recebido"

            pedido.save()

            # Cria os Pedido_Produto
            for produtosCarro in CarroProduto.objects.filter(carro=pedido.carro):
                produto = Produto.objects.get(id=produtosCarro.produto.id)
                Pedido_Produto.objects.create(pedido=pedido, produto=produto, codigo=produto.codigo, 
                                              descricao=produto.descricao, codigo_GTIN=produto.codigo_GTIN, preco_unitario_bruto=produto.preco_unitario_bruto, 
                                              desconto_dinheiro=produto.desconto_dinheiro, desconto_retira=produto.desconto_retira, unidade=produto.unidade, 
                                              quantidade=produtosCarro.quantidade, total_bruto=produtosCarro.subtotal)#, 
                                            #   desconto_total=, desconto_unitario=, total_final=)

            # Direciona pro pagamento
            if pedido.local_de_pagamento == "online":
                pedido.pedido_status = "Pagamento Processando"
                pedido.save()

                return create_payment(request)
            else:
                # pedido.pedido_status = "Pagamento Pendente"
                # pedido.save()
                         
                # return redirect(request.POST["path"])
                return redirect(f"{reverse_lazy('lojaapp:pedidoconfirmado')}?id={pedido.id}&status=Pagamento_Pendente")
            
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

def create_payment(request):
    pedido = Pedido_order.objects.get(id=request.POST["pedido_id"])
    carro = pedido.carro
    produtos = CarroProduto.objects.filter(carro=carro)

    telefone_numeros = pedido.telefone.replace("-", "")
    cpf_cnpj_numeros = pedido.cpf_cnpj.replace(".", "").replace("-", "")
    cep_numeros = pedido.endereco_envio.cep.replace("-", "")

    url = "https://sandbox.api.pagseguro.com/checkouts"
    
    payload = {
        "customer": {
            "phone": {
                "area": pedido.telefone[5:7],
                "country": "+55",
                "number": telefone_numeros[9:]
            },
            "name": pedido.nome_cliente,
            "email": pedido.email,
            "tax_id": cpf_cnpj_numeros
        },
        "shipping": {
            "address": {
                "street": pedido.endereco_envio.rua,
                "number": pedido.endereco_envio.numero,
                "complement": pedido.endereco_envio.complemento,
                "locality": pedido.endereco_envio.bairro,
                "city": pedido.endereco_envio.cidade,
                "region_code": pedido.endereco_envio.estado,
                "country": "BRA",
                "postal_code": cep_numeros
            },
        },
        "reference_id": request.POST["pedido_id"],
        "customer_modifiable": False,
        "items": [],
        "payment_methods": [],
        "payment_methods_configs": [
            {
                "type": "CREDIT_CARD",
                "config_options": [
                    {
                        "option": "INSTALLMENTS_LIMIT",
                        "value": "12"
                    },
                    {
                        "option": "INTEREST_FREE_INSTALLMENTS",
                        "value": "12"
                    }
                ]
            }
        ],
        "redirect_url": f"https://vendashg.pythonanywhere.com/pedido-cofirmado/?id={pedido.id}", # f"http://127.0.0.1:8000/pedido-cofirmado/?id={pedido.id}&status=Pagamento_Confirmado",
        # f"{reverse_lazy('lojaapp:pedidoconfirmado')}?id={pedido.id}&status=Pagamento_Confirmado"
        # "notification_urls": ["https://vendashg.pythonanywhere.com/test_atualizacao_pag/"],
        # "payment_notification_urls": ["notificacaoPagamento.com.br"]
    }

    if pedido.frete:
        payload["shipping"]["type"] = "FIXED"
        payload["shipping"]["service_type"] = "SEDEX"
        payload["shipping"]["address_modifiable"] = False
        payload["shipping"]["amount"] = int(pedido.frete * 100)
    else:
        payload["shipping"]["type"] = "FREE"
        payload["shipping"]["address_modifiable"] = False

    for prod in produtos:
        payload["items"].append(
            {
                "reference_id": prod.produto.codigo,
                "name": prod.produto.titulo,
                "description": prod.produto.descricao,
                "quantity": prod.quantidade,
                "unit_amount": int(prod.preco_unitario * 100),
                "image_url": "https://vendashg.pythonanywhere.com" + prod.produto.image.url
            }
        )
    
    payload["payment_methods"].append({ "type": pedido.forma_de_pagamento })

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN_SANDBOX,
        "Content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code >= 200 and response.status_code < 300:
        respJson = response.json()
        links = respJson.get("links")
        for dic in links:
            if dic["rel"] == "PAY":
                payment_url = dic["href"]
        
        # print(response.text)
        pedido.id_PagBank = respJson["id"]
        pedido.save()

        return redirect(payment_url)
    else:
        # TODO: Melhorar essa tela de erro pra versão final
        return HttpResponse(f"Error: {response.status_code} - {response.text}")

class PedidoConfirmadoView(LogedMixin, BaseContextMixin, TemplateView):
    template_name = "pedidoConfirmado.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        pedido_id = self.request.GET.get("id")
        pedido_status = self.request.GET.get("status")

        # TODO: Acho que só funfa automaticamente pra cartão de credito
        # Muda status do pedido
        pedido = Pedido_order.objects.get(id=pedido_id)

        if ta_pago(pedido):
            pedido.pedido_status = "Pagamento Confirmado"

        # pedido.pedido_status = pedido_status.replace("_", " ")
        pedido.save()

        # Aumenta a quantidade de venda de cada produto
        pedidoProduto = Pedido_Produto.objects.filter(pedido=pedido)
        for pp in pedidoProduto:
            produto = Produto.objects.get(id=pp.produto.id)
            produto.quantidade_vendas += 1

        # Cria carro novo
        carro_obj = Carro.objects.create(total=0)
        carro_obj.save()
        self.request.session['carro_id'] = carro_obj.id

        return context

class ClienteRegistrarView(LojaMixin, BaseContextMixin, CreateView):
    template_name = "clienteregistrar.html"
    form_class = ClienteRegistrarForms
    success_url = reverse_lazy("lojaapp:home")

    def form_valid(self, form):
        # Obtenha os dados do formulário
        nome = form.cleaned_data.get("nome")
        sobrenome = form.cleaned_data.get("sobrenome")
        email = form.cleaned_data.get("email")
        cpf = form.cleaned_data.get("cpf")
        telefone = form.cleaned_data.get("telefone")
        endereco = form.cleaned_data.get("endereco")
        senha = form.cleaned_data.get("senha")

        # Crie o usuário
        user = User.objects.create_user(username=email, email=email, password=senha,first_name=nome, last_name=sobrenome)
        form.instance.user = user
        login(self.request, user)

        # Retorne a resposta de sucesso
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class ClienteLogoutView(LojaMixin, View):
    def get (self, request):
        logout(request)
        return redirect("lojaapp:home")

class ClienteEntrarView(LojaMixin, BaseContextMixin, FormView):
    template_name = "clienteentrar.html"
    form_class = ClienteEntrarForms
    success_url = reverse_lazy("lojaapp:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("senha")
        user = authenticate(username=email, password=password)

        if user is not None:
            if Cliente.objects.filter(user=user).exists():
                login(self.request, user)
            else:
                return render(self.request, self.template_name,
                              {"form": form, "error": "Cliente nao existe"})
        else:
            error_message = "Falha na autenticação. Email: {}, Senha: {}".format(email, password)
            return render(self.request, self.template_name,
                          {"form": form, "error": error_message})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class ClientePerfilView(LogedMixin, LojaMixin, BaseContextMixin, TemplateView):
    template_name = "clienteperfil.html"

    # def dispatch(self,request,*args, **kwargs):
    #     if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
    #         pass
    #     else:
    #         return redirect("/entrar/?next=/perfil/")
    #     return super().dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        perfil_select = self.request.GET.get("perfil", "ClienteInfo")
        context['caixaPerfil'] = perfil_select
        print(perfil_select)

        cliente = self.request.user.cliente
        context['cliente'] = cliente

        pedidos = Pedido_order.objects.filter(carro__cliente=cliente).order_by("-id")
        context['pedidos'] = pedidos

        enderecos = Endereco.objects.filter(cliente=cliente).order_by("-id")
        context['enderecos'] = enderecos
        return context

class ClientePedidoDetalheView(LogedMixin, BaseContextMixin, DetailView):
    template_name = "clientepedidodetalhe.html"
    model = Pedido_order
    context_object_name = "pedido_obj"

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated and request.user.cliente:
        order_id = self.kwargs["pk"]
        pedido = Pedido_order.objects.get(id=order_id)
        if request.user.cliente != pedido.carro.cliente:
            return redirect("lojaapp:clienteperfil")

        # else:
        #     return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)

class CadastrarEnderecoView(LogedMixin, LojaMixin, BaseContextMixin, CreateView):
    template_name = "enderecocadastrar.html"
    form_class = EnderecoRegistrarForms
    success_url = reverse_lazy("lojaapp:clienteperfil")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "next" in self.request.GET:
            context["next"] = self.request.GET.get("next")

        return context

    def form_valid(self, form):
        # Obtenha os dados do formulário

        form.instance.cliente = self.request.user.cliente

        # Retorne a resposta de sucesso
        return super().form_valid(form)

    # def get_success_url(self):
    #     if "next" in self.request.GET:
    #         next_url = self.request.GET.get("next")
    #         return next_url
    #     else:
    #         return self.success_url

def endereco_cadastrar(request):
    if request.method == 'POST':
        try:
            print(request.POST)
            usuario = User.objects.get(username=request.user.username)
            cliente = Cliente.objects.get(user=usuario)
            titulo = request.POST["titulo"]
            cep = request.POST["cep"]
            estado = request.POST["estado"]
            cidade = request.POST["cidade"]
            bairro = request.POST["bairro"]
            rua = request.POST["rua"]
            numero = request.POST["numero"]
            complemento = request.POST["complemento"]

            endereco = Endereco.objects.create(cliente=cliente, titulo=titulo, cep=cep, estado=estado, cidade=cidade, bairro=bairro , rua=rua , numero=numero , complemento=complemento)
            endereco.save()

            next_url = request.POST.get("next", reverse("lojaapp:clienteperfil"))
            if  not next_url:
                next_url = reverse("lojaapp:clienteperfil")
            return redirect(next_url)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

class deletarEnderecoView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):
        endereco_id = self.kwargs['endereco_id']
        Endereco.objects.filter(id=endereco_id).delete()

        return redirect("lojaapp:clienteperfil")

class PesquisarView(BaseContextMixin, TemplateView):
    template_name = "pesquisar.html"

    def preprocessar_precos(self, produtos):
        for produto in produtos:
            venda_parts = str(produto.venda).split('.')
            produto.integer_part = venda_parts[0]
            produto.decimal_part = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
        return produtos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        classificar_selected = self.request.GET.get("Classificar", "Destaque")
        if classificar_selected == "Destaque":
            context["classificar"] = "Destaque"
            order = "-visualizacao"
        elif classificar_selected ==  "MaisVendidos":
            context["classificar"] = "MaisVendidos"
            order = "-quantidade_vendas"
        elif classificar_selected ==  "MenorPreço":
            context["classificar"] = "MenorPreço"
            order = "preco_unitario_bruto"
        elif classificar_selected ==  "MaiorPreço":
            context["classificar"] = "MaiorPreço"
            order = "-preco_unitario_bruto"

        kw = self.request.GET.get("query")
        
        resultado = Produto.objects.filter(Q(titulo__icontains=kw) | Q(descricao__icontains = kw)).order_by(order)
        resultadoList = self.preprocessar_precos(resultado)

        resultadoPag = Paginator(resultadoList, 20)
        page_number = self.request.GET.get('page')

        context["resultado"] = resultadoPag.get_page(page_number)
        return context

class CategoriaView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "categoria.html"

    def preprocessar_precos(self, produtos):
        for produto in produtos:
            venda_parts = str(produto.venda).split('.')
            produto.integer_part = venda_parts[0]
            produto.decimal_part = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
        return produtos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url_slug = self.kwargs['slug']

        categoria = Categoria.objects.get(slug=url_slug)
        context['categoria'] = categoria

        classificar_selected = self.request.GET.get("Classificar", "Destaque")
        if classificar_selected == "Destaque":
            context["classificar"] = "Destaque"
            order = "-visualizacao"
        elif classificar_selected ==  "MaisVendidos":
            context["classificar"] = "MaisVendidos"
            order = "-quantidade_vendas"
        elif classificar_selected ==  "MenorPreço":
            context["classificar"] = "MenorPreço"
            order = "preco_unitario_bruto"
        elif classificar_selected ==  "MaiorPreço":
            context["classificar"] = "MaiorPreço"
            order = "-preco_unitario_bruto"
        
        all_produtos = Produto.objects.filter(Categoria = categoria).order_by(order).all()
        produto_list = self.preprocessar_precos(all_produtos)
        paginator = Paginator(produto_list, 20)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        
        return context

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class AdminLoginView(BaseContextMixin, FormView):
    template_name = "admin_paginas/adminlogin.html"
    form_class = ClienteEntrarForms
    success_url = reverse_lazy("lojaapp:adminhome")
    def form_valid(self, form):
        unome = form.cleaned_data.get("usuario")
        pword = form.cleaned_data.get("senha")
        usr = authenticate(username = unome, password = pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name,{"form":self.form_class,"error":"usuario nao corresponde"})
        return super().form_valid(form)

class AdminHomeView(AdminRequireMixin, BaseContextMixin, TemplateView):
    template_name = "admin_paginas/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PedidosPendentes"] = Pedido_order.objects.filter(pedido_status="Pedido Recebido").order_by("-id")

        return context

class AdminPedidoView(AdminRequireMixin, BaseContextMixin, DetailView):
    template_name = "admin_paginas/adminpedidodetalhe.html"

    model = Pedido_order

    context_object_name = "pedido_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PEDIDO_STATUS"] = PEDIDO_STATUS
        return context

class AdminTodosPedidoView(AdminRequireMixin, BaseContextMixin, ListView):
    template_name = "admin_paginas/admintodospedido.html"

    queryset = Pedido_order.objects.all().order_by("-id")
    # context_object_name = "todospedido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pedidoType_select = self.request.GET.get('pedidos', 'Todos')

        context = {
            'PedidosAndamento' : Pedido_order.objects.filter(pedido_status="Pedido  em Andamento").order_by("-id"),
            'PedidosRecebido' : Pedido_order.objects.filter(pedido_status="Pedido Recebido").order_by("-id"),
            'PagamentoPendente' : Pedido_order.objects.filter(pedido_status="Pagamento Pendente").order_by("-id"),
            'PagamentoProcessando' : Pedido_order.objects.filter(pedido_status="Pagamento Processando").order_by("-id"),
            'PagamentoConfirmado' : Pedido_order.objects.filter(pedido_status="Pagamento Confirmado").order_by("-id"),
            'PedidosProcessando' : Pedido_order.objects.filter(pedido_status="Pedido Processando").order_by("-id"),
            'PedidosCaminho' : Pedido_order.objects.filter(pedido_status="Pedido Caminho").order_by("-id"),
            'PedidosCompletado' : Pedido_order.objects.filter(pedido_status="Pedido Completado").order_by("-id"),
            'PedidosCancelado' : Pedido_order.objects.filter(pedido_status="Pedido Cancelado").order_by("-id"),
        }
        
        statusList = []
        for i,j in PEDIDO_STATUS:
            statusList.append((i, j.replace(" ", "_")))
        context["pedidoType"] = statusList

        return context

class AdminPedidoMudarView(AdminRequireMixin, BaseContextMixin, ListView):
    def post(self,request,*args,**kwargs):
        pedido_id = self.kwargs["pk"]
        pedido_obj = Pedido_order.objects.get(id=pedido_id)
        novo_status = request.POST.get("status")
        pedido_obj.pedido_status = novo_status
        pedido_obj.save()

        return redirect(reverse_lazy("lojaapp:adminpedido", kwargs={"pk" : pedido_id}))
    
class PesquisarAdminView(AdminRequireMixin, BaseContextMixin, TemplateView):
    template_name = "admin_paginas/PesquisarAdmin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        kw = self.request.GET.get("query")

        result = Pedido_order.objects.filter(Q(nome_cliente__contains = kw) | Q(email__icontains = kw) | Q(id = kw)).order_by("-id")
        context['resultados'] = result

        return context
    
def consultar_checkout_pag(request):
    if request.method == 'POST':
        # print(request.POST)
        if request.POST["checkout_id"]:
            pedido = Pedido_order.objects.get(id=request.POST["pedido_id"])

            url = "https://sandbox.api.pagseguro.com/checkouts/" + request.POST["checkout_id"] + "?offset=0&limit=10"

            headers = {
                "accept": "*/*",
                "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN_SANDBOX,
            }

            consulta_response = requests.get(url, headers=headers)
                    
            if consulta_response.status_code >= 200 and consulta_response.status_code < 300:
                respJson = consulta_response.json()
                order_urls = respJson.get("orders")[0].get("links")
                for dic in order_urls:
                    if dic["rel"] == "GET":
                        consulta_order_url = dic["href"]

                order_response = requests.get(consulta_order_url, headers=headers)

                if order_response.status_code >= 200 and order_response.status_code < 300:
                    charges = order_response.json().get("charges")[0]
                    # data = json.dumps(charges, indent=4)
                    # print(order_response.text)
                    # return redirect(consulta_url)
                    # return redirect(request.POST["path"])
                    return render(request, "admin_paginas/adminpedidodetalhe.html", {"pedido_obj":pedido,"PEDIDO_STATUS":PEDIDO_STATUS, "data_Pag":charges, "pagseguro_display":True})
                    # return JsonResponse(charges)
                else:
                    # TODO: Melhorar essa tela de erro pra versão final
                    return HttpResponse(f"Error: {order_response.status_code} - {order_response.text}")
            else:
                # TODO: Melhorar essa tela de erro pra versão final
                return HttpResponse(f"Error: {consulta_response.status_code} - {consulta_response.text}")
        
    return HttpResponse("Invalid request.")

def cancelar_checkout_pag(request):
    if request.method == 'POST':
        # print(request.POST)
        # pedido = Pedido_order.objects.get(id=request.POST["pedido_id"])
        url = "https://internal.sandbox.api.pagseguro.com/charges/" + request.POST["id_cancel"] + "/cancel"
        # internal.

        payload = { "amount": { "value": request.POST["valor_pago"] } }

        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN_SANDBOX,
            "Content-type": "application/json"
        }

        cancelar_response = requests.get(url, json=payload, headers=headers)

        if cancelar_response.status_code >= 200 and cancelar_response.status_code < 300:
            print(cancelar_response.text)
        else:
            # TODO: Melhorar essa tela de erro pra versão final
            return HttpResponse(f"Error: {cancelar_response.status_code} - {cancelar_response.text}")
        
    return HttpResponse("Invalid request.")

def test_atualizacao_pag(request):
    if request.method == 'POST':
        pedido_id = "52"
        pedido = Pedido_order.objects.get(id=pedido_id)

        notification_code = request.POST.get("notificationCode")
        notification_type = request.POST.get("notificationType")

        if notification_type == "transaction":
            pedido.status_test = notification_code
            pedido.save()

        return JsonResponse({"status": "success"}, status=200)

    return HttpResponse("Invalid request.")

def ta_pago(_pedido):
    url = "https://sandbox.api.pagseguro.com/checkouts/" + _pedido.id_PagBank + "?offset=0&limit=10"

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN_SANDBOX,
    }

    consulta_response = requests.get(url, headers=headers)
                    
    if consulta_response.status_code >= 200 and consulta_response.status_code < 300:
        respJson = consulta_response.json()
        order_urls = respJson.get("orders")[0].get("links")
        for dic in order_urls:
            if dic["rel"] == "GET":
                consulta_order_url = dic["href"]

        order_response = requests.get(consulta_order_url, headers=headers)

        if order_response.status_code >= 200 and order_response.status_code < 300:
            status = order_response.json().get("charges")[0].get("status")

            if status == "PAID":
                return True
            
    return False
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def testPOST(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect(request.POST["path"])

    return HttpResponse("Invalid request.")