from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, FormView, DetailView, ListView
from django.urls import reverse_lazy
from .forms import Checar_PedidoForms, ClienteRegistrarForms, ClienteEntrarForms, EnderecoRegistrarForms
from.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
import os
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import serializers, status

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
        return super().dispatch(request,*args,**kwargs)

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

        context['banners'] = Banner.objects.all()

        return context

class SobreView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.all()

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
        produto.visualizacao += 1
        produto.save()
        return context

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

class FormaDeEntregaView(LojaMixin, BaseContextMixin, CreateView):
    template_name = "forma_de_entrega.html"
    form_class = Checar_PedidoForms
    success_url = reverse_lazy("lojaapp:home")

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and request.user.cliente:
            pass
        else:
            return redirect("/entrar/?next=/forma-de-entrega/")
        return super().dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
        else:
            carro_obj = None
        context["carro"] = carro_obj

        context["enderecos"] = Endereco.objects.filter(cliente=self.request.user.cliente)
        context["enderecosLojas"] = Endereco.objects.filter(cliente=Cliente.objects.get(nome="Casa", sobrenome="HG"))

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
    
def pedido_carro_endereco(request):
    if request.method == 'POST':
        try:
            print(request.POST)
            usuario = User.objects.get(username=request.user.username)
            cliente = Cliente.objects.get(user=usuario)
            nome_cliente = f"{cliente.nome} {cliente.sobrenome}"
            cpf_cnpj = cliente.cpf_ou_cnpj_formatado
            # codigo_cliente = 
            telefone = cliente.telefone

            carro = Carro.objects.get(id=request.POST["carro_id"])
            pedido_status = "Pedido em Andamento"
            total_bruto = carro.total
            
            endereco_envio = Endereco.objects.get(id=request.POST["local_entrega"])
            endereco_envio_formatado = f"{endereco_envio.rua} {endereco_envio.numero} {endereco_envio.complemento}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"

            pedido = Pedido_order.objects.create(cliente=cliente, nome_cliente=nome_cliente, cpf_cnpj=cpf_cnpj, telefone=telefone, carro=carro, total_bruto=total_bruto, pedido_status=pedido_status, endereco_envio=endereco_envio, endereco_envio_formatado=endereco_envio_formatado)
            pedido.save()

            return redirect('lojaapp:checkout')
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")


class CheckOutView(LojaMixin, BaseContextMixin, CreateView):
    template_name = "processar.html"
    form_class = Checar_PedidoForms
    success_url = reverse_lazy("lojaapp:home")

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and request.user.cliente:
            pass
        else:
            return redirect("/entrar/?next=/checkout/")
        return super().dispatch(request,*args, **kwargs)

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


class ClientePerfilView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "clienteperfil.html"

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated and Cliente.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user.cliente
        context['cliente'] = cliente

        pedidos = Pedido_order.objects.filter(carro__cliente=cliente).order_by("-id")
        context['pedidos'] = pedidos

        enderecos = Endereco.objects.filter(cliente=cliente).order_by("-id")
        context['enderecos'] = enderecos
        return context

class ClientePedidoDetalheView(DetailView):
    template_name = "clientepedidodetalhe.html"
    model = Pedido_order
    context_object_name = "pedido_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.cliente:
            order_id = self.kwargs["pk"]
            pedido = Pedido_order.objects.get(id=order_id)
            if request.user.cliente != pedido.carro.cliente:
                return redirect("lojaapp:clienteperfil")

        else:
            return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)

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

    context_object_name = "todospedido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PedidosPendentes"] = Pedido_order.objects.filter(pedido_status="Pedido Recebido").order_by("-id")

        return context


class AdminPedidoMudarView(AdminRequireMixin, BaseContextMixin, ListView):
    def post(self,request,*args,**kwargs):
        pedido_id = self.kwargs["pk"]
        pedido_obj = Pedido_order.objects.get(id=pedido_id)
        novo_status = request.POST.get("status")
        pedido_obj.pedido_status = novo_status
        pedido_obj.save()

        return redirect(reverse_lazy("lojaapp:adminpedido", kwargs={"pk" : pedido_id}))

class PesquisarView(BaseContextMixin, TemplateView):
    template_name = "pesquisar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("query")
        resultado = Produto.objects.filter(Q(titulo__icontains=kw) | Q(descricao__icontains = kw))
        context["resultado"] = resultado
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
        all_produtos = Produto.objects.filter(Categoria = categoria).order_by("-id").all()
        produto_list = self.preprocessar_precos(all_produtos)
        paginator = Paginator(produto_list, 20)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        
        return context

class CadastrarEnderecoView(LojaMixin, BaseContextMixin, CreateView):
    template_name = "enderecocadastrar.html"
    form_class = EnderecoRegistrarForms
    success_url = reverse_lazy("lojaapp:clienteperfil")

    def form_valid(self, form):
        # Obtenha os dados do formulário

        form.instance.cliente = self.request.user.cliente

        # Retorne a resposta de sucesso
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

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

            return redirect('lojaapp:clienteperfil')
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

class deletarEnderecoView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):
        endereco_id = self.kwargs['endereco_id']
        Endereco.objects.filter(id=endereco_id).delete()

        return redirect("lojaapp:clienteperfil")
