import os
from .forms import *
from .models import *
from .serializers import *
from django_teste import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, DetailView, ListView
from django.views.generic.edit import DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.core.cache import cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from rest_framework import serializers, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from PIL import Image
from io import BytesIO
from random import randint
# from threading import Thread
import unicodedata
import requests
import datetime
import holidays
import decimal
import json

class AdminRequireMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request,*args,**kwargs)
    
class GeraHistoricoProdutosMixin(object):
    def dispatch(self, request, *args, **kwargs):
        geraHistoricoProdutos(Produto.objects.all())
        
        return super().dispatch(request, *args, **kwargs)

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

class VerifMixin(object):
    def dispatch(self,request,*args, **kwargs):
        if request.user.cliente.verificado:
            pass
        else:
            messages.success(request, 'Conta não verificada. Verifique seu e-mail para ativar o acesso.')
            return redirect("lojaapp:home")
        
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
        pedido = PedidoOrder.objects.filter(carro=carro_obj)

        if pedido:
            pass
        else:
            return redirect("lojaapp:home")
        return super().dispatch(request,*args, **kwargs)

class BaseContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        carro_id = self.request.session.get("carro_id")
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            produtos = list(CarroProduto.objects.filter(carro=carro_obj))
            if produtos:
                context["numProdCarro"] = len(produtos)

        context['todoscategorias'] = Categoria.objects.all()

        context['footer'] = [Empresa.objects.get(titulo="Hefesto"), Empresa.objects.get(titulo="Casa HG"), Empresa.objects.get(titulo="Pagseguro")]

        return context

class CrazyAlvaPaymentCheckMixin(object):
    def dispatch(self,request,*args,**kwargs):
        pedidos = list(PedidoOrder.objects.filter(pedido_status="Pagamento Processando", local_de_pagamento="online"))
        # print(len(pedidos))
        if len(pedidos):
            pedido_aleatorio = pedidos[randint(0, (len(pedidos) - 1))]

            try:
                if ta_pago(pedido_aleatorio):
                    pedido_aleatorio.pedido_status = "Pagamento Confirmado"
                    pedido_aleatorio.save()
            except:
                print(f"Pedido {pedido_aleatorio.id}: Pagamento pendente")

        return super().dispatch(request,*args,**kwargs)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

class HomeView(LojaMixin, CrazyAlvaPaymentCheckMixin, BaseContextMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_produtos = Produto.objects.all().order_by("-quantidade_vendas")
        produto_list = preprocessar_precos(all_produtos)

        # TODO: Deletar esse paginator se for ficar com a aparencia separada por categoria
        paginator = Paginator(produto_list, 20)
        page_number = self.request.GET.get('page', 1)
        context['page_obj'] = paginator.get_page(page_number)

        # Não sei se tem uma forma mais eficiente de fazer essa merda
        if paginator.num_pages > 4:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = int(page_number) + 4
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == 2:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = False
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == (paginator.num_pages - 1):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = False
            elif int(page_number) == (paginator.num_pages):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = int(page_number) - 4
            else:
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = int(page_number) + 2
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = False
                context['quatroAtras'] = False
        elif paginator.num_pages > 2:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
            elif int(page_number) == (paginator.num_pages):
                context['duasAtras'] = int(page_number) - 2
            else:
                context['duasFrente'] = False
                context['duasAtras'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False
        else:
            context['duasFrente'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['duasAtras'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False

        context['produtos_por_categoria'] = {
            categoria: preprocessar_precos(Produto.objects.filter(Categoria=categoria, em_estoque=True).order_by("-quantidade_vendas")[:11]) # Tem que ser um numero impar de pordutos
            for categoria in Categoria.objects.all()
        }
        
        context['mais_vendidos'] = preprocessar_precos(Produto.objects.filter(em_estoque=True).order_by("-quantidade_vendas")[:7]) # Tem que ser um numero impar de pordutos

        context['banners'] = Banner.objects.all()

        # TODO: Apagar esse teste
        # testEmail("jggenio@gmail.com", User.objects.get(username="Alva"), PedidoOrder.objects.get(id=96))

        return context

class SobreView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enderecosLojas"] = Endereco.objects.filter(cliente=Cliente.objects.get(nome="Casa", sobrenome="HG"))
        context["mapsKey"] = settings.GOOGLE_MAPS_KEY

        return context

class ContatoView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "contato.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['API'] = list(TestStatus.objects.all())[-1]

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

        context['preco_dinheiro'] = round((produto.preco_unitario_bruto * (1 - ((produto.desconto_dinheiro + produto.desconto_retira) / 100))), 2)
        
        context['preco_caixa'] = round(produto.preco_unitario_bruto * produto.fechamento_embalagem, 2)

        context['limite_estoque'] = sum(produto.estoque_lojas.values())

        context['fotos_produtos'] = produto.images.all().order_by("img_num") #FotosProduto.objects.filter(produto=produto)

        if produto.Categoria.slug == "porcelanatos" or produto.Categoria.slug == "ceramicas":
            context['variacao_faces_pisos'] = VARIACAO_FACES_PISOS
            context['indicacao_uso_pisos'] = INDICACAO_DE_USO_PISOS

        produtos_similares_list = list(Produto.objects.filter(Categoria=produto.Categoria, em_estoque=True).order_by("-quantidade_vendas")[:11]) # Tem que ser um numero impar de pordutos
        if produto in produtos_similares_list:
            produtos_similares_list = list(Produto.objects.filter(Categoria=produto.Categoria, em_estoque=True).order_by("-quantidade_vendas")[:12])
            produtos_similares_list.pop(produtos_similares_list.index(produto))

        produtos_similares = preprocessar_precos(produtos_similares_list)
        context['produtos_similares'] = produtos_similares

        return context

class AddCarroView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):
        produto_id = self.kwargs['prod_id']
        produto_obj = Produto.objects.get(id=produto_id)

        carro_id = self.request.session.get("carro_id",None)

        if produto_obj.em_estoque:
            try:
                carro_obj = Carro.objects.get(id=carro_id)
                produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)

                if produto_no_carro.exists():
                    carroproduto = produto_no_carro.last()
                    carroproduto.quantidade += 1
                    carroproduto.subtotal_bruto += produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                    carroproduto.subtotal += produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                    carroproduto.save()

                else:
                    carroproduto = CarroProduto.objects.create(
                        carro = carro_obj,
                        produto = produto_obj,
                        preco_unitario = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                        quantidade = 1,
                        subtotal_bruto = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                        subtotal = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                    )

                carro_obj.total += produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                carro_obj.save()

            except Carro.DoesNotExist:
                carro_obj = Carro.objects.create(total=0)
                self.request.session['carro_id'] = carro_obj.id
                carroproduto = CarroProduto.objects.create(
                    carro=carro_obj,
                    produto=produto_obj,
                    preco_unitario=produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                    quantidade=1,
                    subtotal_bruto=produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                    subtotal=produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                )
                carro_obj.total += produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                carro_obj.save()

        return redirect("lojaapp:home")

# TODO: Verificar se essa porra é usada, tenho quase certeza que é inutil e não funfa
class AddCarroView2(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "produtodetalhe.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        produto_id = self.kwargs['prod_id']
        produto_obj = Produto.objects.get(id=produto_id)

        carro_id = self.request.session.get("carro_id",None)
        
        if produto_obj.em_estoque:
            try:
                carro_obj = Carro.objects.get(id=carro_id)
                produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)

                if produto_no_carro.exists():
                    carroproduto = produto_no_carro.last()
                    carroproduto.quantidade += 1
                    carroproduto.subtotal_bruto += produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                    carroproduto.subtotal += produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                    carroproduto.save()

                else:
                    carroproduto = CarroProduto.objects.create(
                        carro = carro_obj,
                        produto = produto_obj,
                        preco_unitario = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                        quantidade = 1,
                        subtotal_bruto = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                        subtotal = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                    )

                carro_obj.total += carroproduto.subtotal
                carro_obj.save()


            except Carro.DoesNotExist:
                carro_obj = Carro.objects.create(total=0)
                self.request.session['carro_id'] = carro_obj.id
                carroproduto = CarroProduto.objects.create(
                    carro=carro_obj,
                    produto=produto_obj,
                    preco_unitario=produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                    quantidade=1,
                    subtotal_bruto=produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                    subtotal=produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem
                )
                carro_obj.total += carroproduto.subtotal
                carro_obj.save()

        return context
    
class AddCarroQuantView(LojaMixin, BaseContextMixin, TemplateView):
    def get(self,request,*arg,**kwargs):
        produto_id = request.GET.get("prod_id")
        produto_quantidade = int(request.GET.get("quantidade"))

        produto_obj = Produto.objects.get(id=produto_id)
        carro_id = self.request.session.get("carro_id",None)
        if produto_obj.em_estoque:
            try:
                carro_obj = Carro.objects.get(id=carro_id)
                produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)

                if produto_no_carro.exists():
                    carroproduto = produto_no_carro.last()
                    carroproduto.quantidade += produto_quantidade
                    carroproduto.subtotal_bruto += (produto_obj.preco_unitario_bruto * produto_quantidade * produto_obj.fechamento_embalagem)
                    carroproduto.subtotal += (produto_obj.preco_unitario_bruto * produto_quantidade * produto_obj.fechamento_embalagem)
                    carroproduto.save()

                else:
                    carroproduto = CarroProduto.objects.create(
                    carro = carro_obj,
                    produto = produto_obj,
                    preco_unitario = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                    quantidade = produto_quantidade,
                    subtotal_bruto = (produto_obj.preco_unitario_bruto * produto_quantidade * produto_obj.fechamento_embalagem),
                    subtotal = (produto_obj.preco_unitario_bruto * produto_quantidade * produto_obj.fechamento_embalagem)

                    )

                carro_obj.total += carroproduto.subtotal
                carro_obj.save()


            except Carro.DoesNotExist:
                carro_obj = Carro.objects.create(total=0)
                self.request.session['carro_id'] = carro_obj.id
                carroproduto = CarroProduto.objects.create(
                    carro = carro_obj,
                    produto = produto_obj,
                    preco_unitario = produto_obj.preco_unitario_bruto * produto_obj.fechamento_embalagem,
                    quantidade = produto_quantidade,
                    subtotal_bruto = (produto_obj.preco_unitario_bruto * produto_quantidade * produto_obj.fechamento_embalagem),
                    subtotal = (produto_obj.preco_unitario_bruto * produto_quantidade * produto_obj.fechamento_embalagem)

                )
                carro_obj.total += carroproduto.subtotal
                carro_obj.save()

            return redirect("lojaapp:meucarro")
        
        return redirect("lojaapp:produtodetalhe", slug=produto_obj.slug)

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
            if (cp_obj.quantidade * cp_obj.produto.fechamento_embalagem) < sum(cp_obj.produto.estoque_lojas.values()):
                cp_obj.quantidade += 1
                cp_obj.subtotal += cp_obj.preco_unitario
                cp_obj.subtotal_bruto += cp_obj.preco_unitario
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

            order = PedidoOrder.objects.filter(carro=carro_obj)
            if order:
                order.delete()

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

            order = PedidoOrder.objects.filter(carro=carro)
            if order:
                order.delete()

        return redirect("lojaapp:meucarro")

class FormaDeEntregaView(LogedMixin, VerifMixin, LojaMixin, CarroComItemsMixin, BaseContextMixin, TemplateView):
    template_name = "forma_de_entrega.html"
    # form_class = Checar_PedidoForms # TODO: Acho que pode tirar
    success_url = reverse_lazy("lojaapp:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
        else:
            carro_obj = None
        context["carro"] = carro_obj

        lojas = Endereco.objects.filter(cliente=Cliente.objects.get(nome="Casa", sobrenome="HG"))

        # desconto retirada / estoque do carrinho nas lojas
        # TODO: Acho que pode tirar esse desconto retirada
        estoque_carro = {"estoque_carro": {"Casa HG - Várzea": True, "Casa HG - Magé/Guapimirim": True, "Casa HG - Atacadão Dos Pisos": True}}
        desc_retirada = 0
        for prod in CarroProduto.objects.filter(carro=carro_obj):
            desc_retirada += prod.preco_unitario * prod.quantidade * (prod.produto.desconto_retira / 100)
            
            # estoque_prod = prod.produto.estoque_lojas.all()
            # for loja in lojas:
            #     if loja not in estoque_prod:
            #         estoque_carro["estoque_carro"][loja.titulo] = False
            estoque_prod = prod.produto.estoque_lojas
            for estoque_loja in estoque_prod.items():
                if estoque_loja[1] < prod.quantidade:
                    estoque_carro["estoque_carro"][estoque_loja[0]] = False

        context.update(estoque_carro)

        context["desconto_retirada"] = str(round(desc_retirada, 2))

        context["enderecos"] = Endereco.objects.filter(cliente=self.request.user.cliente).order_by("-id")
        context["enderecosLojas"] = lojas

        # Calculo da data de entrega
        hoje = datetime.date.today()
        feriados = holidays.BR(state='RJ')
        diasUteis = 0
        dia = datetime.date.today()
        interv = datetime.timedelta(days=1)
        amanha = hoje + datetime.timedelta(days=1)

        ## Calcula o proximo dia util
        while (amanha in feriados) or (amanha.isoweekday() > 5):
            amanha += datetime.timedelta(days=1)

        ## Calcula o setimo dia util
        while diasUteis < 7:
            dia += interv

            if (dia not in feriados) and (dia.isoweekday() < 6):
                diasUteis += 1

        context["dataAmanha"] = amanha.strftime("%d/%m/%y")
        context["dataEntrega"] = dia.strftime("%d/%m/%y")

        return context
    
def pedido_carro_endereco(request):
    if request.method == 'POST':
        try:
            # if PedidoOrder.objects.filter(carro=request.POST["carro_id"]):
                # print(request.POST)
                # PedidoOrder.objects.get(carro=request.POST["carro_id"]).delete()
            # print(request.POST)

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
            desconto_retirada = decimal.Decimal(request.POST["desconto_retirada"])
            total_final = (decimal.Decimal(total_bruto) + frete) # - desconto_retirada)
            
            endereco_envio = Endereco.objects.get(id=request.POST["local_entrega"])
            if endereco_envio.complemento and endereco_envio.numero:
                endereco_envio_formatado = f"{endereco_envio.rua} {endereco_envio.numero} {endereco_envio.complemento}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"
            elif endereco_envio.numero:
                endereco_envio_formatado = f"{endereco_envio.rua} {endereco_envio.numero}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"
            elif endereco_envio.complemento:
                endereco_envio_formatado = f"{endereco_envio.rua} {endereco_envio.complemento}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"
            else:
                endereco_envio_formatado = f"{endereco_envio.rua}, {endereco_envio.bairro} - {endereco_envio.cep} {endereco_envio.cidade}/{endereco_envio.estado}"

            
            if PedidoOrder.objects.filter(carro=request.POST["carro_id"]):
                pedido = PedidoOrder.objects.get(carro=request.POST["carro_id"])
                pedido.endereco_envio = endereco_envio
                pedido.endereco_envio_formatado = endereco_envio_formatado
                pedido.total_bruto = total_bruto
                pedido.frete = frete
                pedido.desconto_retirada = desconto_retirada
                pedido.total_final = total_final
            else:
                pedido = PedidoOrder.objects.create(cliente=cliente, nome_cliente=nome_cliente, cpf_cnpj=cpf_cnpj, telefone=telefone, email=email, carro=carro, pedido_status=pedido_status, total_bruto=total_bruto, total_final=total_final, frete=frete, desconto_retirada=desconto_retirada, endereco_envio=endereco_envio, endereco_envio_formatado=endereco_envio_formatado)
            pedido.save()

            return redirect('lojaapp:checkout')
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

class CheckOutView(LogedMixin, VerifMixin, LojaMixin, CarroComItemsMixin, PedidoExisteMixin, BaseContextMixin, TemplateView):
    template_name = "processar.html"    
    # form_class = Checar_PedidoForms # TODO: Acho que pode tirar
    success_url = reverse_lazy("lojaapp:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id",None)
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
        else:
            carro_obj = None
        context["carro"] = carro_obj

        pedido = PedidoOrder.objects.get(carro=carro_obj)
        context["pedido"] = pedido

        # Reseta o carro produto e pedido produto pro caso do usuario não finalizar a compra online
        if pedido.local_de_pagamento == "online":
            for prod in CarroProduto.objects.filter(carro=carro_obj):
                prod.subtotal = prod.subtotal_bruto
                prod.save()

            if pedido.pedido_status == "Pagamento Processando":
                for pedProd in PedidoProduto.objects.filter(pedido=pedido):
                    pedProd.delete()
    
        # descontos formas de pagamento
        desc_dinheiro = 0
        for prod in CarroProduto.objects.filter(carro=carro_obj):
            desc_dinheiro += prod.preco_unitario * (prod.produto.desconto_dinheiro / 100) * prod.quantidade
        context["desconto_dinheiro"] = decimal.Decimal(round(desc_dinheiro, 2))

        desc_credito_list = [0.07, 0.04, 0.04, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        desconto_credito = pedido.total_bruto * decimal.Decimal(desc_credito_list[0])
        context["desconto_credito"] = decimal.Decimal(round(desconto_credito, 2))
        
        desc_a_vista = pedido.total_bruto * decimal.Decimal(0.15)
        context["desconto_a_vista"] = decimal.Decimal(round(desc_a_vista, 2))

        context['desconto_dinheiro_a_vista'] = decimal.Decimal(round(desc_dinheiro, 2) + round(desc_a_vista, 2))

        context["desconto_tot_init"] = str(round(float(desc_dinheiro + desc_a_vista), 2)).replace(",", ".")

        context["descontos"] = json.dumps({
            "desconto_a_vista": round(float(desc_a_vista), 2),
            "desconto_dinheiro": round(float(desc_dinheiro), 2),
            "desconto_credito": round(float(desconto_credito), 2),
            "desc_credito_list": desc_credito_list,
            "total_bruto": float(pedido.total_bruto),
        })

        context["total_dinheiro"] = decimal.Decimal(round((pedido.total_bruto + pedido.frete - pedido.desconto_retirada - desc_dinheiro - desc_a_vista), 2))

        context["total_credito"] = decimal.Decimal(round((pedido.total_bruto + pedido.frete - pedido.desconto_retirada - desconto_credito), 2))

        context["total_eletronico"] = decimal.Decimal(round((pedido.total_bruto + pedido.frete - pedido.desconto_retirada - desc_a_vista), 2))

        context["total_desc_pagamento"] = str(round((pedido.total_bruto + pedido.frete - pedido.desconto_retirada - desc_dinheiro - desc_a_vista), 2)).replace(",", ".")

        return context

    # TODO: Acho que pode tirar
    # def form_valid(self,form):
    #     carro_id = self.request.session.get("carro_id")
    #     if carro_id:
    #         carro_obj = Carro.objects.get(id=carro_id)
    #         form.instance.carro = carro_obj
    #         form.instance.subtotal = carro_obj.total
    #         form.instance.desconto = 0
    #         form.instance.total = carro_obj.total
    #         form.instance.pedido_status = "Pedido Recebido"
    #         del self.request.session['carro_id']
    #     else:
    #         return redirect("lojaapp:home")
    #     return super().form_valid(form)

def pedido_carro_pagamento(request):
    if request.method == 'POST':
        try:
            # print(request.POST)
            # usuario = User.objects.get(username=request.user.username)
            if request.POST["botaoStatus"] == "abled":
                # Termina de preencher os dados de pagamento
                pedido = PedidoOrder.objects.get(id=request.POST["pedido_id"])
                carro = pedido.carro
                produtos = CarroProduto.objects.filter(carro=carro)
                desc = 0
                desc_credito_list = [0.07, 0.04, 0.04, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

                pedido.total_final = decimal.Decimal(request.POST["total_final"])

                pedido.desconto_forma_pagamento = decimal.Decimal(request.POST["desconto_pagamento"])

                pedido.total_desconto = pedido.desconto_forma_pagamento + pedido.desconto_retirada

                pedido.local_de_pagamento = request.POST["local_pagamento"]
                if ("metodo_pagamento" in request.POST) and (request.POST["local_pagamento"] != "dinheiro"):
                    pedido.forma_de_pagamento = request.POST["metodo_pagamento"]

                    if "parcelas" in request.POST:
                        pedido.parcelas = request.POST["parcelas"]
                        pedido.valor_parcela = pedido.total_final / decimal.Decimal(request.POST["parcelas"])
                    else:
                        pedido.parcelas = 1
                        pedido.valor_parcela = pedido.total_final

                    if pedido.forma_de_pagamento == "DEBIT_CARD" or pedido.forma_de_pagamento == "BOLETO" or pedido.forma_de_pagamento == "PIX":
                        for prod in produtos:
                            desc = 0.15                                             # Desconto à vista
                            if pedido.desconto_retirada:
                                desc += float(prod.produto.desconto_retira) / 100   # Desconto retirada em loja

                            prod.subtotal = prod.preco_unitario * prod.quantidade * decimal.Decimal(1 - desc)
                            prod.save()

                            desc = 0
                    elif pedido.forma_de_pagamento == "CREDIT_CARD":
                        for prod in produtos:
                            desc = desc_credito_list[int(pedido.parcelas) - 1]
                            if pedido.desconto_retirada:
                                desc += float(prod.produto.desconto_retira) / 100   # Desconto retirada em loja

                            prod.subtotal = prod.preco_unitario * prod.quantidade * decimal.Decimal(1 - desc)
                            prod.save()

                            desc = 0
                else:
                    pedido.local_de_pagamento = "loja"
                    pedido.forma_de_pagamento = "dinheiro"
                    pedido.parcelas = 1
                    pedido.valor_parcela = pedido.total_final

                    for prod in produtos:
                        desc = float(prod.produto.desconto_dinheiro) / 100          # Desconto dinheiro
                        desc += 0.15                                                # Desconto à vista
                        if pedido.desconto_retirada:
                            desc += float(prod.produto.desconto_retira) / 100       # Desconto retirada em loja

                        prod.subtotal = prod.preco_unitario * prod.quantidade * decimal.Decimal(1 - desc)
                        prod.save()

                        desc = 0

                pedido.pedido_status = "Pedido Recebido"

                pedido.save()

                # Cria os PedidoProduto
                for produtosCarro in CarroProduto.objects.filter(carro=pedido.carro):
                    produto = Produto.objects.get(id=produtosCarro.produto.id)
                    PedidoProduto.objects.create(pedido=pedido, produto=produto, nome_produto=produto.titulo, codigo=produto.codigo, 
                                                descricao=produto.descricao, codigo_GTIN=produto.codigo_GTIN, preco_unitario_bruto=produto.preco_unitario_bruto, 
                                                desconto_dinheiro=produto.desconto_dinheiro, desconto_retira=produto.desconto_retira, unidade=produto.unidade, 
                                                quantidade=produtosCarro.quantidade, total_bruto=produtosCarro.subtotal_bruto, 
                                                desconto_total=(produtosCarro.subtotal_bruto - produtosCarro.subtotal), 
                                                desconto_unitario=(produtosCarro.subtotal_bruto - produtosCarro.subtotal) / produtosCarro.quantidade, 
                                                total_final=produtosCarro.subtotal)

                # Direciona pro pagamento
                if pedido.local_de_pagamento == "online":
                    pedido.pedido_status = "Pagamento Processando"
                    pedido.save()

                    # TODO: Mudar quando liberar pagamento online com cartão de credito
                    if pedido.forma_de_pagamento == "CREDIT_CARD":
                        messages.success(request, 'Pagamento online utilizando cartão de credito indisponivel no momento')
                        return redirect(request.POST['path'])
                    
                    return create_payment(request)
                else:
                    # pedido.pedido_status = "Pagamento Pendente"
                    # pedido.save()
                            
                    # return redirect(request.POST["path"])
                    return redirect(f"{reverse_lazy('lojaapp:pedidoconfirmado')}?id={pedido.id}")
            else:
                messages.success(request, 'Por favor ler e concordar com os termos e condições da compra.')
                return redirect(request.POST['path'])
            
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

def create_payment(request):
    pedido = PedidoOrder.objects.get(id=request.POST["pedido_id"])
    carro = pedido.carro
    produtos = CarroProduto.objects.filter(carro=carro)

    telefone_numeros = pedido.telefone.replace("-", "")
    cpf_cnpj_numeros = pedido.cpf_cnpj.replace(".", "").replace("-", "")
    cep_numeros = pedido.endereco_envio.cep.replace("-", "")

    url = "https://api.pagseguro.com/checkouts"
    
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
                # "complement": pedido.endereco_envio.complemento,
                "locality": pedido.endereco_envio.bairro,
                "city": pedido.endereco_envio.cidade,
                "region_code": pedido.endereco_envio.estado,
                "country": "BRA",
                "postal_code": cep_numeros
            },
            "type": "FREE",
            "address_modifiable": False
        },
        "reference_id": request.POST["pedido_id"],
        "customer_modifiable": False,
        "items": [],
        "payment_methods": [
            { 
                "type": pedido.forma_de_pagamento 
            }
        ],
        "payment_methods_configs": [
            {
                "type": "CREDIT_CARD",
                "config_options": [
                    {
                        "value": "1",
                        "option": "INSTALLMENTS_LIMIT"
                    }
                ] 
            # },
            # {
            #     "type": "DEBIT_CARD",
            #     "config_options": [
            #         {
            #             "value": "1",
            #             "option": "INSTALLMENTS_LIMIT"
            #         }
            #     ]
            }
        ],
        # "payment_methods_configs": [
        #     {
        #         "type": "CREDIT_CARD",
        #         "config_options": [
        #             {
        #                 "option": "INTEREST_FREE_INSTALLMENTS",
        #                 "value": pedido.parcelas
        #             },
        #             {
        #                 "option": "INSTALLMENTS_LIMIT",
        #                 "value": pedido.parcelas
        #             }
        #         ]
        #     }
        # ],
        "redirect_url": f"https://www.loja-casahg.com.br/pedido-cofirmado/?id={pedido.id}", # f"http://127.0.0.1:8000/pedido-cofirmado/?id={pedido.id}&status=Pagamento_Confirmado",
        # f"{reverse_lazy('lojaapp:pedidoconfirmado')}?id={pedido.id}&status=Pagamento_Confirmado"
        # "notification_urls": ["https://www.loja-casahg.com.br/test_atualizacao_pag/"],
        # "payment_notification_urls": ["https://www.loja-casahg.com.br/test_atualizacao_pag/"]
    }

    # if pedido.frete:
    #     payload["shipping"]["type"] = "FIXED"
    #     payload["shipping"]["service_type"] = "SEDEX"
    #     payload["shipping"]["address_modifiable"] = False
    #     payload["shipping"]["amount"] = int(pedido.frete * 100)
    # else:
    #     payload["shipping"]["type"] = "FREE"
    #     payload["shipping"]["address_modifiable"] = False

    if pedido.endereco_envio.complemento:
        payload["shipping"]["address"]["complement"] =  pedido.endereco_envio.complemento

    for prod in produtos:
        payload["items"].append(
            {
                "reference_id": prod.produto.codigo,
                "name": prod.produto.descricao,
                "description": prod.produto.descricao,
                "quantity": prod.quantidade,
                "unit_amount": int((prod.subtotal / prod.quantidade) * 100),
                "image_url": f"https://www.loja-casahg.com.br{prod.produto.image.url}"
            }
        )

        # print(f"https://www.loja-casahg.com.br{prod.produto.image.url}")

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN,
        "Content-type": "application/json"
    }
    
    # print(payload)
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

        # print(f"Request: {payload}")
        # print(f"Response: {response.json()}")

        return redirect(payment_url)
    else:
        # TODO: Melhorar essa tela de erro pra versão final
        return HttpResponse(f"Error: {response.status_code} - {response.text}")

class PedidoConfirmadoView(LogedMixin, BaseContextMixin, TemplateView):
    template_name = "pedidoConfirmado.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        pedido_id = self.request.GET.get("id")
        # pedido_status = self.request.GET.get("status")

        # Muda status do pedido
        pedido = PedidoOrder.objects.get(id=pedido_id)

        EmailPedidoRealizado(pedido)

        if pedido.local_de_pagamento == "online":
            if ta_pago(pedido):
                pedido.pedido_status = "Pagamento Confirmado"
                EmailPedidoPagamentoConfirmado(pedido)
        else:
            pedido.pedido_status = "Pagamento Pendente"

        # pedido.pedido_status = pedido_status.replace("_", " ")
        pedido.save()

        # Aumenta a quantidade de venda de cada produto
        pedidoProduto = PedidoProduto.objects.filter(pedido=pedido)
        for pp in pedidoProduto:
            produto = Produto.objects.get(id=pp.produto.id)
            produto.quantidade_vendas += 1
            produto.save()

        # Cria carro novo
        carro_obj = Carro.objects.create(total=0)
        carro_obj.cliente = self.request.user.cliente
        carro_obj.save()
        self.request.session['carro_id'] = carro_obj.id
        context["numProdCarro"] = 0

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

        # Thread(target=EmailClienteRegistrado, args=user).start()
        EmailClienteRegistrado(user)

        # Retorne a resposta de sucesso
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            messages.success(self.request, 'Email de verificação enviado')
            return next_url
        else:
            messages.success(self.request, 'Email de verificação enviado')
            return self.success_url

def verifica_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (user.DoesNotExist, ValueError, TypeError):
        messages.success(request, 'Link de verificação inválido')
        return redirect("lojaapp:home")

    if default_token_generator.check_token(user, token):
        user.cliente.verificado = True
        user.cliente.save()
        messages.success(request, 'Conta verificada com sucesso')
        return redirect("lojaapp:home")
    else:
        messages.success(request, 'Link de verificação ou token inválido')
        return redirect("lojaapp:home")

class ClienteReverificaContaView(LojaMixin, View):
    def dispatch(self, request, *args, **kwargs):
        usuario = request.user

        if not usuario.cliente.verificado:
            EmailVerificaCliente(usuario)

            messages.success(request, 'Email de verificação enviado novamente')
            return redirect("lojaapp:clienteperfil")

        return super().dispatch(request, *args, **kwargs)

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
        # print(perfil_select)

        cliente = self.request.user.cliente
        context['cliente'] = cliente

        
        pedidos = PedidoOrder.objects.filter(carro__cliente=cliente).order_by("-id")
        paginator = Paginator(pedidos, 6)
        page_number = self.request.GET.get('page', '1')
        context['pedidos'] = paginator.get_page(page_number)
        # context['pedidos'] = pedidos
        if paginator.num_pages > 2:
            context['duasFrente'] = int(page_number) + 2
            context['duasAtras'] = int(page_number) - 2
        else:
            context['duasFrente'] = False
            context['duasAtras'] = False
        # print(type(page_number))

        enderecos = Endereco.objects.filter(cliente=cliente).order_by("-id")
        context['enderecos'] = enderecos
        return context

class ClientePerfilViewEditarNome(LogedMixin, LojaMixin, BaseContextMixin, TemplateView, FormView):
    template_name = "clienteperfil_editar_nome.html"
    form_class = ClienteEditarNome
    success_url = reverse_lazy("lojaapp:clienteperfil")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        cliente = self.request.user.cliente

        kwargs['initial'] = {
            'nome': cliente.nome,
            'sobrenome': cliente.sobrenome
        }

        return kwargs

    def form_valid(self, form):
        nome = form.cleaned_data.get("nome")
        sobrenome = form.cleaned_data.get("sobrenome")

        user = self.request.user
        
        user.first_name = nome
        user.last_name = sobrenome
        user.save()

        cliente = user.cliente
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.save()  # Salva as alterações no banco de dados

        return super().form_valid(form)

    def get_success_url(self):
            return f"{self.success_url}?perfil=ClienteInfo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user.cliente
        context['cliente'] = cliente

        return context

class ClientePerfilViewEditarEmail(LogedMixin, LojaMixin, BaseContextMixin, TemplateView, FormView):
    template_name = "clienteperfil_editar_email.html"
    form_class = ClienteEditarEmail
    success_url = reverse_lazy("lojaapp:clienteperfil")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        cliente = self.request.user.cliente

        kwargs['initial'] = {
            'email': cliente.email
        }

        return kwargs

    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        user = self.request.user
        user.email = email
        user.username = email
        user.save()

        cliente = user.cliente
        cliente.email = email
        cliente.save()  # Salva as alterações no banco de dados

        return super().form_valid(form)

    def get_success_url(self):
            return f"{self.success_url}?perfil=ClienteInfo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user.cliente
        context['cliente'] = cliente
        
        return context

class ClientePerfilViewEditarCPF(LogedMixin, LojaMixin, BaseContextMixin, TemplateView, FormView):
    template_name = "clienteperfil_editar_CPF.html"
    form_class = ClienteEditarCPF
    success_url = reverse_lazy("lojaapp:clienteperfil")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        cliente = self.request.user.cliente

        kwargs['initial'] = {
            'cpf_ou_cnpj': cliente.cpf_ou_cnpj
        }

        return kwargs

    def form_valid(self, form):
        cpf_ou_cnpj = form.cleaned_data.get("cpf_ou_cnpj")

        user = self.request.user

        cliente = user.cliente
        cliente.cpf_ou_cnpj = cpf_ou_cnpj
        cliente.save()  # Salva as alterações no banco de dados

        return super().form_valid(form)

    def get_success_url(self):
            return f"{self.success_url}?perfil=ClienteInfo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user.cliente
        context['cliente'] = cliente
        
        return context

class ClientePerfilViewEditarTelefone(LogedMixin, LojaMixin, BaseContextMixin, TemplateView, FormView):
    template_name = "clienteperfil_editar_telefone.html"
    form_class = ClienteEditarTelefone
    success_url = reverse_lazy("lojaapp:clienteperfil")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        cliente = self.request.user.cliente

        telefoneOG = cliente.telefone
        telefoneOG = telefoneOG.replace('+55 ', '')

        kwargs['initial'] = {
            'telefone': telefoneOG
        }

        return kwargs

    def form_valid(self, form):
        # Alva
        # telefone = form.cleaned_data.get("telefone")
        telefone = form.cleaned_data.get("telefone")

        user = self.request.user
        user.save()

        cliente = user.cliente
        # cliente.telefone = telefone
        cliente.telefone = telefone
        cliente.save()  # Salva as alterações no banco de dados

        return super().form_valid(form)

    def get_success_url(self):
            return f"{self.success_url}?perfil=ClienteInfo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user.cliente
        context['cliente'] = cliente
        
        return context
    
class ClientePerfilViewAlterarSenha(LogedMixin, LojaMixin, BaseContextMixin, FormView):
    template_name = "cliente_alterar_senha.html"
    form_class = ClienteAlterarSenhaForms
    success_url = reverse_lazy("lojaapp:clienteperfil")


    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("senha_antiga")
        user = authenticate(username=email, password=password)

        senha_nova1 = form.cleaned_data.get("senha_nova")
        senha_nova2 = form.cleaned_data.get("repita_a_senha_nova")

        if user is not None:
            if Cliente.objects.filter(user=user).exists():
                if senha_nova1==senha_nova2:
                    user.set_password(senha_nova1)
                    user.save()

                    # Relogue o usuário após mudar a senha
                    login(self.request, user)

                else:
                    return render(self.request, self.template_name,
                                    {"form": form, "error": "campos de senha nova não batem"})
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        

        return context

class DeletarPerfilView(LoginRequiredMixin, LojaMixin, BaseContextMixin, DeleteView):
    model = User
    template_name = 'confirmar_deletar_perfil.html'
    success_url = reverse_lazy('lojaapp:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        

        return context

    def get_object(self):
        return self.request.user

class ClientePedidoDetalheView(LogedMixin, BaseContextMixin, DetailView):
    template_name = "clientepedidodetalhe.html"
    model = PedidoOrder
    context_object_name = "pedido_obj"

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated and request.user.cliente:
        order_id = self.kwargs["pk"]
        pedido = PedidoOrder.objects.get(id=order_id)
        if request.user.cliente != pedido.carro.cliente:
            return redirect("lojaapp:clienteperfil")

        # else:
        #     return redirect("/entrar/?next=/perfil/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pedido = PedidoOrder.objects.get(id=self.kwargs["pk"])

        context["progresso"] = 0
        if pedido.pedido_status == "Pedido Recebido" or pedido.pedido_status == "Pagamento Pendente"  or pedido.pedido_status == "Pagamento Processando":
            context["progresso"] = 25
        elif pedido.pedido_status == "Pagamento Confirmado" or pedido.pedido_status == "Pedido Processando":
            context["progresso"] = 50
        elif pedido.pedido_status == "Pedido Caminho" or pedido.pedido_status == "Pedido Pronta Retirada":
            context["progresso"] = 75
        elif pedido.pedido_status == "Pedido Completado":
            context["progresso"] = 100

        return context

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
            if request.POST["botaoStatus"] == "abled":
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
                if not next_url:
                    next_url = (f"{reverse_lazy('lojaapp:clienteperfil')}?perfil=Endereco")
                return redirect(next_url)
            else:
                if request.POST.get('next', None):
                    next_url = f"{request.POST['path']}?next={request.POST.get('next')}"
                else:
                    next_url = request.POST['path']
                return redirect(next_url)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

class ClientePerfilViewEditarEndereco(LogedMixin, LojaMixin, BaseContextMixin, TemplateView, FormView):
    template_name = "clienteperfil_editar_endereco.html"
    form_class = ClienteEditarEndereco
    success_url = reverse_lazy("lojaapp:clienteperfil")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        endereco_id = self.kwargs['endereco_id']
        endereco = Endereco.objects.get(id=endereco_id)

        kwargs['initial'] = {
            'titulo': endereco.titulo,
            'cep': endereco.cep,
            'cidade': endereco.cidade,
            'estado': endereco.estado,
            'bairro': endereco.bairro,
            'rua': endereco.rua,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
        }

        return kwargs
    
    def form_valid(self, form):
        endereco_id = self.kwargs['endereco_id']
        endereco = Endereco.objects.get(id=endereco_id)

        endereco.titulo = form.cleaned_data.get("titulo")
        endereco.cep = form.cleaned_data.get("cep")
        endereco.estado = form.cleaned_data.get("estado")
        endereco.cidade = form.cleaned_data.get("cidade")
        endereco.bairro = form.cleaned_data.get("bairro")
        endereco.rua = form.cleaned_data.get("rua")
        endereco.numero = form.cleaned_data.get("numero")
        endereco.complemento = form.cleaned_data.get("complemento")
        
        
        cidade_param = unicodedata.normalize('NFKD', form.cleaned_data.get("cidade")).encode('ascii', 'ignore').decode('utf-8').lower()
        if cidade_param == "teresopolis":
            endereco.save()

        return super().form_valid(form)

    def get_success_url(self):
            return f"{self.success_url}?perfil=Endereco"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cliente = self.request.user.cliente
        context['enderecos'] = Endereco.objects.filter(cliente=cliente).order_by("-id")

        endereco_id = self.kwargs['endereco_id']
        context['endereco_edit'] = Endereco.objects.get(id=endereco_id)

        return context

class deletarEnderecoView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):
        endereco_id = self.kwargs['endereco_id']
        Endereco.objects.filter(id=endereco_id).delete()

        return redirect(f"{reverse_lazy('lojaapp:clienteperfil')}?perfil=Endereco")

class PesquisarView(BaseContextMixin, TemplateView):
    template_name = "pesquisar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        kw = self.request.GET.get("query")

        # Ordenação (barra_macro_classificar.html)
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

        # Metodo pra conseguir pegar produtos atraves da label dos choices em charfields
        classe_tecnica_absorcao_pisos_field = Produto._meta.get_field('classe_tecnica_absorcao_pisos')
        variacao_faces_field = Produto._meta.get_field('variacao_faces')
        indicacao_uso_field = Produto._meta.get_field('indicacao_uso')

        display_to_value = {label.lower(): value for value, label in classe_tecnica_absorcao_pisos_field.choices}
        display_to_value.update({label.lower(): value for value, label in variacao_faces_field.choices})
        display_to_value.update({label.lower(): value for value, label in indicacao_uso_field.choices})

        query_lower = kw.lower()

        match = display_to_value.get(query_lower)
        
        filters = (
            Q(titulo__icontains=kw) | Q(descricao__icontains = kw) | Q(codigo__iexact = kw) | Q(codigo_GTIN__iexact = kw) | Q(Categoria__titulo__icontains = kw)
            | Q(slug__iexact = kw) | Q(marca__icontains = kw) | Q(acabamento_superficial__icontains = kw) | Q(indicacao_uso__icontains = kw)
            | Q(classe_tecnica_absorcao_pisos__icontains = kw) | Q(variacao_faces__icontains = kw) # TODO: To na duvida se deixa essa linha
        )

        if match:
            filters |= (Q(classe_tecnica_absorcao_pisos__iexact = match) | Q(variacao_faces__iexact = match) | Q(indicacao_uso__iexact = match))
        
        resultado = Produto.objects.filter(filters, em_estoque=True).order_by(order)
        # resultado = Produto.objects.filter(Q(titulo__icontains=kw) | Q(descricao__icontains = kw) | Q(codigo__iexact = kw) | Q(codigo_GTIN__iexact = kw)
        #                                     | Q(Categoria__titulo__icontains = kw) | Q(slug__iexact = kw) | Q(marca__icontains = kw) | Q(acabamento_superficial__icontains = kw)
        #                                     | Q(classe_tecnica_absorcao_pisos__iexact = kw) | Q(variacao_faces__iexact = kw) | Q(indicacao_uso__icontains = kw)).order_by(order)
        
        # Filtro (filtro_coluna_maco_produtos.html)
        precoMax = self.request.GET.get("precoMax")
        context['Caract_precoMax'] = precoMax

        try:
            cat_slug = unicodedata.normalize('NFKD', kw).encode('ascii', 'ignore').decode('utf-8').lower().replace(" ", "_")
            categoria = Categoria.objects.get(slug=cat_slug)
            context['categoria'] = categoria

            if categoria.slug == "porcelanatos" or categoria.slug == "ceramicas":
                context['acabamento_superficial_pisos'] = ACABAMENTO_SUPERFICIAL_PISOS
                context['classe_tecnica_absorcao_pisos'] = CLASSE_TECNICA_ABSORCAO_PISOS
                context['variacao_faces_pisos'] = VARIACAO_FACES_PISOS
                context['indicacao_uso_pisos'] = INDICACAO_DE_USO_PISOS

                Caract_acabamento_superficial_pisos = self.request.GET.getlist("acabamento_superficial_pisos")
                context['Caract_acabamento_superficial_pisos'] = Caract_acabamento_superficial_pisos

                Caract_classe_tecnica_absorcao_pisos = self.request.GET.getlist("classe_tecnica_absorcao_pisos")
                context['Caract_classe_tecnica_absorcao_pisos'] = Caract_classe_tecnica_absorcao_pisos

                Caract_variacao_faces_pisos = self.request.GET.getlist("variacao_faces_pisos")
                context['Caract_variacao_faces_pisos'] = Caract_variacao_faces_pisos
                
                Caract_indicacao_uso_pisos = self.request.GET.getlist("indicacao_uso_pisos")
                context['Caract_indicacao_uso_pisos'] = Caract_indicacao_uso_pisos
            else:
                Caract_acabamento_superficial_pisos = None
                Caract_classe_tecnica_absorcao_pisos = None
                Caract_variacao_faces_pisos = None
                Caract_indicacao_uso_pisos = None
        except:
            context['categoria'] = None
            # Caract_acabamento_superficial_pisos = None
            # Caract_classe_tecnica_absorcao_pisos = None
            # Caract_variacao_faces_pisos = None
            # Caract_indicacao_uso_pisos = None

            if resultado.filter((Q(Categoria__slug__iexact="porcelanatos") | Q(Categoria__slug__iexact="ceramicas"))):
                context['acabamento_superficial_pisos'] = ACABAMENTO_SUPERFICIAL_PISOS
                context['classe_tecnica_absorcao_pisos'] = CLASSE_TECNICA_ABSORCAO_PISOS
                context['variacao_faces_pisos'] = VARIACAO_FACES_PISOS
                context['indicacao_uso_pisos'] = INDICACAO_DE_USO_PISOS

                Caract_acabamento_superficial_pisos = self.request.GET.getlist("acabamento_superficial_pisos")
                context['Caract_acabamento_superficial_pisos'] = Caract_acabamento_superficial_pisos

                Caract_classe_tecnica_absorcao_pisos = self.request.GET.getlist("classe_tecnica_absorcao_pisos")
                context['Caract_classe_tecnica_absorcao_pisos'] = Caract_classe_tecnica_absorcao_pisos

                Caract_variacao_faces_pisos = self.request.GET.getlist("variacao_faces_pisos")
                context['Caract_variacao_faces_pisos'] = Caract_variacao_faces_pisos
                
                Caract_indicacao_uso_pisos = self.request.GET.getlist("indicacao_uso_pisos")
                context['Caract_indicacao_uso_pisos'] = Caract_indicacao_uso_pisos
            else:
                Caract_acabamento_superficial_pisos = None
                Caract_classe_tecnica_absorcao_pisos = None
                Caract_variacao_faces_pisos = None
                Caract_indicacao_uso_pisos = None

        context["marcas"] = Produto.objects.filter(filters, em_estoque=True).exclude(marca__isnull=True).values_list("marca", flat=True).distinct()
        Caract_marcas = self.request.GET.getlist("marcas")
        context['Caract_marcas'] = Caract_marcas
        
        # Coleta produtos dos filtros
        if precoMax or Caract_marcas or Caract_acabamento_superficial_pisos or Caract_classe_tecnica_absorcao_pisos or Caract_variacao_faces_pisos or Caract_indicacao_uso_pisos:
            urlGet = ""
            if precoMax:
                filters &= (Q(preco_unitario_bruto__lte=decimal.Decimal(precoMax.replace("R$", "").replace(" ", "").replace('.', '').replace(',', '.'))))

                urlGet += f"&precoMax={precoMax}"

            if Caract_acabamento_superficial_pisos:
                filters &= (Q(acabamento_superficial__in=Caract_acabamento_superficial_pisos))

                for n in Caract_acabamento_superficial_pisos:
                    urlGet += f"&acabamento_superficial_pisos={n}"

            if Caract_classe_tecnica_absorcao_pisos:
                display_to_value = {label: value for value, label in CLASSE_TECNICA_ABSORCAO_PISOS}

                match = []
                for cta in Caract_classe_tecnica_absorcao_pisos:
                    match.append(display_to_value.get(cta))

                filters &= (Q(classe_tecnica_absorcao_pisos__in=match))

                for n in Caract_classe_tecnica_absorcao_pisos:
                    urlGet += f"&classe_tecnica_absorcao_pisos={n}"

            if Caract_variacao_faces_pisos:
                display_to_value = {label: value for value, label in VARIACAO_FACES_PISOS}

                match = []
                for vf in Caract_variacao_faces_pisos:
                    match.append(display_to_value.get(vf))

                filters &= (Q(variacao_faces__in=match))

                for n in Caract_variacao_faces_pisos:
                    urlGet += f"&variacao_faces_pisos={n}"

            if Caract_indicacao_uso_pisos:
                display_to_value = {label: value for value, label in INDICACAO_DE_USO_PISOS}

                match = []
                for iu in Caract_indicacao_uso_pisos:
                    match.append(display_to_value.get(iu))

                filters &= (Q(indicacao_uso__in=match))

                for n in Caract_indicacao_uso_pisos:
                    urlGet += f"&indicacao_uso_pisos={n}"

            if Caract_marcas:
                filters &= (Q(marca__in=Caract_marcas))

                for n in Caract_marcas:
                    urlGet += f"&marcas={n}"

            context["urlGet"] = urlGet
                
        resultado = Produto.objects.filter(filters, em_estoque=True).order_by(order)

        resultadoList = preprocessar_precos(resultado)

        resultadoPag = Paginator(resultadoList, 20)
        page_number = self.request.GET.get('page', 1)

        context["resultado"] = resultadoPag.get_page(page_number)

        # Não sei se tem uma forma mais eficiente de fazer essa merda
        if resultadoPag.num_pages > 4:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = int(page_number) + 4
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == 2:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = False
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == (resultadoPag.num_pages - 1):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = False
            elif int(page_number) == (resultadoPag.num_pages):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = int(page_number) - 4
            else:
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = int(page_number) + 2
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = False
                context['quatroAtras'] = False
        elif resultadoPag.num_pages > 2:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
            elif int(page_number) == (resultadoPag.num_pages):
                context['duasAtras'] = int(page_number) - 2
            else:
                context['duasFrente'] = False
                context['duasAtras'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False
        else:
            context['duasFrente'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['duasAtras'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False

        return context

class CategoriaView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "categoria.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url_slug = self.kwargs['slug']

        categoria = Categoria.objects.get(slug=url_slug)
        context['categoria'] = categoria

        if categoria.slug == "porcelanatos" or categoria.slug == "ceramicas":
            context['acabamento_superficial_pisos'] = ACABAMENTO_SUPERFICIAL_PISOS
            context['classe_tecnica_absorcao_pisos'] = CLASSE_TECNICA_ABSORCAO_PISOS
            context['variacao_faces_pisos'] = VARIACAO_FACES_PISOS
            context['indicacao_uso_pisos'] = INDICACAO_DE_USO_PISOS

        # Ordenação (barra_macro_classificar.html)
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

        # Filtro (filtro_coluna_maco_produtos.html)
        precoMax = self.request.GET.get("precoMax")
        context['Caract_precoMax'] = precoMax

        Caract_acabamento_superficial_pisos = self.request.GET.getlist("acabamento_superficial_pisos")
        context['Caract_acabamento_superficial_pisos'] = Caract_acabamento_superficial_pisos

        Caract_classe_tecnica_absorcao_pisos = self.request.GET.getlist("classe_tecnica_absorcao_pisos")
        context['Caract_classe_tecnica_absorcao_pisos'] = Caract_classe_tecnica_absorcao_pisos

        Caract_variacao_faces_pisos = self.request.GET.getlist("variacao_faces_pisos")
        context['Caract_variacao_faces_pisos'] = Caract_variacao_faces_pisos
        
        Caract_indicacao_uso_pisos = self.request.GET.getlist("indicacao_uso_pisos")
        context['Caract_indicacao_uso_pisos'] = Caract_indicacao_uso_pisos

        ## Coleta marcas pro filtro
        context["marcas"] = Produto.objects.filter(Categoria=categoria, em_estoque=True).exclude(marca__isnull=True).values_list("marca", flat=True).distinct()
        Caract_marcas = self.request.GET.getlist("marcas")
        context['Caract_marcas'] = Caract_marcas
        
        # Coleta produtos
        if precoMax or Caract_marcas or Caract_acabamento_superficial_pisos or Caract_classe_tecnica_absorcao_pisos or Caract_variacao_faces_pisos or Caract_indicacao_uso_pisos:
            filters = (Q(Categoria__slug__iexact = categoria.slug))
            urlGet = ""
            if precoMax:
                filters &= (Q(preco_unitario_bruto__lte=decimal.Decimal(precoMax.replace("R$", "").replace(" ", "").replace('.', '').replace(',', '.'))))

                urlGet += f"&precoMax={precoMax}"

            if Caract_acabamento_superficial_pisos:
                filters &= (Q(acabamento_superficial__in=Caract_acabamento_superficial_pisos))

                for n in Caract_acabamento_superficial_pisos:
                    urlGet += f"&acabamento_superficial_pisos={n}"

            if Caract_classe_tecnica_absorcao_pisos:
                display_to_value = {label: value for value, label in CLASSE_TECNICA_ABSORCAO_PISOS}

                match = []
                for cta in Caract_classe_tecnica_absorcao_pisos:
                    match.append(display_to_value.get(cta))

                filters &= (Q(classe_tecnica_absorcao_pisos__in=match))

                for n in Caract_classe_tecnica_absorcao_pisos:
                    urlGet += f"&classe_tecnica_absorcao_pisos={n}"

            if Caract_variacao_faces_pisos:
                display_to_value = {label: value for value, label in VARIACAO_FACES_PISOS}

                match = []
                for vf in Caract_variacao_faces_pisos:
                    match.append(display_to_value.get(vf))

                filters &= (Q(variacao_faces__in=match))

                for n in Caract_variacao_faces_pisos:
                    urlGet += f"&variacao_faces_pisos={n}"

            if Caract_indicacao_uso_pisos:
                display_to_value = {label: value for value, label in INDICACAO_DE_USO_PISOS}

                match = []
                for iu in Caract_indicacao_uso_pisos:
                    match.append(display_to_value.get(iu))

                filters &= (Q(indicacao_uso__in=match))

                for n in Caract_indicacao_uso_pisos:
                    urlGet += f"&indicacao_uso_pisos={n}"

            if Caract_marcas:
                filters &= (Q(marca__in=Caract_marcas))

                for n in Caract_marcas:
                    urlGet += f"&marcas={n}"

            all_produtos = Produto.objects.filter(filters, em_estoque=True).order_by(order)
            context["urlGet"] = urlGet
        else:
            all_produtos = Produto.objects.filter(Categoria=categoria, em_estoque=True).order_by(order)

        produto_list = preprocessar_precos(all_produtos)

        # Paginação
        paginator = Paginator(produto_list, 20)
        page_number = self.request.GET.get('page', 1)
        context['page_obj'] = paginator.get_page(page_number)

        ## Não sei se tem uma forma mais eficiente de fazer essa merda
        if paginator.num_pages > 4:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = int(page_number) + 4
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == 2:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = False
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == (paginator.num_pages - 1):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = False
            elif int(page_number) == (paginator.num_pages):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = int(page_number) - 4
            else:
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = int(page_number) + 2
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = False
                context['quatroAtras'] = False
        elif paginator.num_pages > 2:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
            elif int(page_number) == (paginator.num_pages):
                context['duasAtras'] = int(page_number) - 2
            else:
                context['duasFrente'] = False
                context['duasAtras'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False
        else:
            context['duasFrente'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['duasAtras'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False
        
        return context

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

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

class AdminHomeView(AdminRequireMixin, BaseContextMixin, GeraHistoricoProdutosMixin, TemplateView):
    template_name = "admin_paginas/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ProdutosMaisVendido"] = Produto.objects.all().order_by("-quantidade_vendas")[:21]
        context["ProdutosMaisVistos"] = Produto.objects.all().order_by("-visualizacao")[:21]
        context["Pedidos"] = PedidoOrder.objects.all().order_by("-id")[:21]

        return context

class AdminPedidoView(AdminRequireMixin, BaseContextMixin, DetailView):
    template_name = "admin_paginas/adminpedidodetalhe.html"

    model = PedidoOrder

    context_object_name = "pedido_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PEDIDO_STATUS"] = PEDIDO_STATUS
        return context

class AdminTodosPedidoView(AdminRequireMixin, BaseContextMixin, TemplateView):
    template_name = "admin_paginas/admintodospedido.html"

    queryset = PedidoOrder.objects.all().order_by("-id")
    # context_object_name = "todospedido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pedidoType_select = self.request.GET.get('pedidos', 'Todos')

        context = {
            'PedidosAndamento' : PedidoOrder.objects.filter(pedido_status="Pedido  em Andamento").order_by("-id"),
            'PedidosRecebido' : PedidoOrder.objects.filter(pedido_status="Pedido Recebido").order_by("-id"),
            'PagamentoPendente' : PedidoOrder.objects.filter(pedido_status="Pagamento Pendente").order_by("-id"),
            'PagamentoProcessando' : PedidoOrder.objects.filter(pedido_status="Pagamento Processando").order_by("-id"),
            'PagamentoConfirmado' : PedidoOrder.objects.filter(pedido_status="Pagamento Confirmado").order_by("-id"),
            'PedidosProcessando' : PedidoOrder.objects.filter(pedido_status="Pedido Processando").order_by("-id"),
            'PedidosCaminho' : PedidoOrder.objects.filter(pedido_status="Pedido Caminho").order_by("-id"),
            'PedidosProntaRetirada' : PedidoOrder.objects.filter(pedido_status="Pedido Pronta Retirada").order_by("-id"),
            'PedidosCompletado' : PedidoOrder.objects.filter(pedido_status="Pedido Completado").order_by("-id"),
            'PedidosCancelado' : PedidoOrder.objects.filter(pedido_status="Pedido Cancelado").order_by("-id"),
        }
        
        statusList = []
        for i,j in PEDIDO_STATUS:
            statusList.append((i, j.replace(" ", "_")))
        context["pedidoType"] = statusList

        return context

class AdminPedidoMudarView(AdminRequireMixin, BaseContextMixin, ListView):
    def post(self,request,*args,**kwargs):
        pedido_id = self.kwargs["pk"]
        pedido_obj = PedidoOrder.objects.get(id=pedido_id)
        novo_status = request.POST.get("status")
        pedido_obj.pedido_status = novo_status
        pedido_obj.save()

        if novo_status == "Pedido Recebido":
                EmailPedidoRealizado(pedido_obj)
        elif novo_status == "Pagamento Confirmado":
                EmailPedidoPagamentoConfirmado(pedido_obj)
        elif novo_status == "Pedido Caminho":
                EmailPedidoEnviado(pedido_obj)
        elif novo_status == "Pedido Pronta Retirada":
                EmailPedidoProntoRetirada(pedido_obj)
        elif novo_status == "Pedido Cancelado":
                EmailPedidoCancelado(pedido_obj)
        elif novo_status == "Pagamento Completado":
                EmailPedidoCompleto(pedido_obj)

        return redirect(reverse_lazy("lojaapp:adminpedido", kwargs={"pk" : pedido_id}))

class AdminTodosProdutoView(AdminRequireMixin, BaseContextMixin, TemplateView):
    template_name = "admin_paginas/admintodosproduto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        produtos = Produto.objects.all().order_by("-id")

        paginator = Paginator(produtos, 20)
        page_number = self.request.GET.get('page', 1)

        context['produtos'] = paginator.get_page(page_number)
        
        if paginator.num_pages > 4:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = int(page_number) + 4
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == 2:
                context['duasFrente'] = int(page_number) + 2
                context['tresFrente'] = int(page_number) + 3
                context['quatroFrente'] = False
                context['duasAtras'] = False
                context['tresAtras'] = False
                context['quatroAtras'] = False
            elif int(page_number) == (paginator.num_pages - 1):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = False
            elif int(page_number) == (paginator.num_pages):
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = False
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = int(page_number) - 3
                context['quatroAtras'] = int(page_number) - 4
            else:
                context['duasFrente'] = False
                context['tresFrente'] = False
                context['quatroFrente'] = int(page_number) + 2
                context['duasAtras'] = int(page_number) - 2
                context['tresAtras'] = False
                context['quatroAtras'] = False
        elif paginator.num_pages > 2:
            if int(page_number) == 1:
                context['duasFrente'] = int(page_number) + 2
            elif int(page_number) == (paginator.num_pages):
                context['duasAtras'] = int(page_number) - 2
            else:
                context['duasFrente'] = False
                context['duasAtras'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False
        else:
            context['duasFrente'] = False
            context['tresFrente'] = False
            context['quatroFrente'] = False
            context['duasAtras'] = False
            context['tresAtras'] = False
            context['quatroAtras'] = False

        return context

class AdminProdutoView(AdminRequireMixin, BaseContextMixin, TemplateView):
    template_name = "admin_paginas/adminprodutodetalhe.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        context['produto'] = produto

        context['preco_embalagem'] = round((produto.preco_unitario_bruto * produto.fechamento_embalagem), 2)
        context['preco_retirada_dinheiro'] = round((produto.preco_unitario_bruto * ((100 - produto.desconto_dinheiro - produto.desconto_retira) / 100)), 2)

        context['estoque_total'] = sum(produto.estoque_lojas.values())

        pathCodigo = f"{settings.MEDIA_ROOT}/produtos/{produto.codigo}.webp"
        # TODO: Mudar pro nome do site
        if os.path.exists(pathCodigo):
            pathCodigo = f"http://127.0.0.1:8000/media/produtos/{produto.codigo}.webp"
        else:
            pathCodigo = f"http://127.0.0.1:8000/media/produtos/NoImgAvailable.webp"
        context['foto_produto_codigo'] = pathCodigo

        context['fotos_produtos'] = produto.images.all()

        context['categorias'] = Categoria.objects.all()

        if produto.Categoria.slug == "porcelanatos" or produto.Categoria.slug == "ceramicas":
            context['acabamento_superficial_pisos'] = ACABAMENTO_SUPERFICIAL_PISOS
            context['classe_tecnica_absorcao'] = CLASSE_TECNICA_ABSORCAO_PISOS
            context['variacao_faces_pisos'] = VARIACAO_FACES_PISOS
            context['indicacao_uso_pisos'] = INDICACAO_DE_USO_PISOS

        file_path_vendas = os.path.join(settings.MEDIA_ROOT, "data", "vendas.json")
        file_path_visuli = os.path.join(settings.MEDIA_ROOT, "data", "visualizacao.json")
        try:
            with open(file_path_vendas, "r") as file:
                context['grafico_vendas_data'] = json.dumps((json.load(file)))
            with open(file_path_visuli, "r") as file:
                context['grafico_visuli_data'] = json.dumps((json.load(file)))
        except:
            context['grafico_vendas_data'] = {}
            context['grafico_visuli_data'] = {}

        return context
    
def atualiza_produto(request):
    if request.method == 'POST':
        if request.POST["salvar"] == "True":
            produto = Produto.objects.get(codigo=request.POST["produto"])

            produto.descricao = request.POST["descricao"]
            produto.codigo_GTIN = request.POST["codigo_GTIN"]
            produto.Categoria = Categoria.objects.get(slug=request.POST["categoria"])
            produto.em_estoque = (request.POST["em_estoque"] == "True")
            produto.estoque_lojas = {
                                        "Casa HG - Várzea": request.POST["varzea_disponivel"],
                                        "Casa HG - Magé/Guapimirim": request.POST["guapi_disponivel"],
                                        "Casa HG - Atacadão Dos Pisos": request.POST["prata_disponivel"]
                                    }
            produto.preco_unitario_bruto = decimal.Decimal(request.POST["preco_unitario_bruto"].replace(",", "."))
            produto.fechamento_embalagem = decimal.Decimal(request.POST["fechamento_embalagem"].replace(",", "."))
            produto.desconto_dinheiro = decimal.Decimal(request.POST["desconto_dinheiro"].replace(",", "."))
            produto.desconto_retira = decimal.Decimal(request.POST["desconto_retira"].replace(",", "."))

            produto.save()

        return redirect(request.POST["path"])

    return HttpResponse("Invalid request.")

def atualiza_ficha_produto(request):
    if request.method == 'POST':
        if request.POST["salvar"] == "True":
            produto = Produto.objects.get(codigo=request.POST["produto"])

            requestCopy = request.POST.copy()
            for key, value in requestCopy.items():
                if value == 'None' or value == '':
                    requestCopy[key] = None

            produto.marca = requestCopy["marca"]
            produto.formato = requestCopy["formato"]
            
            if requestCopy["espessura"]:
                produto.espessura = int(requestCopy["espessura"])
            else:
                produto.espessura = requestCopy["espessura"]

            if requestCopy["junta_minima"]:
                produto.junta_minima = int(requestCopy["junta_minima"])
            else:
                produto.junta_minima = requestCopy["junta_minima"]

            produto.relevo = requestCopy["relevo"]
            produto.acabamento_superficial = requestCopy["acabamento_superficial"]
            produto.variacao_faces = requestCopy["variacao_faces"]
            produto.classe_tecnica_absorcao_pisos = requestCopy["classe_tecnica_absorcao_pisos"]
            produto.indicacao_uso = requestCopy["indicacao_uso"]
            

            if requestCopy["pecas_caixa"]:
                produto.pecas_caixa = int(requestCopy["pecas_caixa"])
            else:
                produto.pecas_caixa = requestCopy["pecas_caixa"]

            if requestCopy["peso_bruto_caixa"]:
                produto.peso_bruto_caixa = decimal.Decimal(requestCopy["peso_bruto_caixa"].replace(",", "."))
            else:
                produto.peso_bruto_caixa = requestCopy["peso_bruto_caixa"]

            if requestCopy["palet"]:
                produto.palet = decimal.Decimal(requestCopy["palet"].replace(",", "."))
            else:
                produto.palet = requestCopy["palet"]

            produto.save()
            
        return redirect(request.POST["path"])

    return HttpResponse("Invalid request.")

class AdminCategoriasView(AdminRequireMixin, BaseContextMixin, TemplateView):
    template_name = "admin_paginas/admincategoria.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categoria_select = self.request.GET.get('categoria', 'Todas')
        context['Categorias'] = Categoria.objects.all()

        if categoria_select == 'Todas':
            context["ProdutosMaisVendido"] = Produto.objects.all().order_by("-quantidade_vendas")
            context["ProdutosMaisVistos"] = Produto.objects.all().order_by("-visualizacao")
        else:
            categoria_id = Categoria.objects.get(titulo=categoria_select).id
            context["ProdutosMaisVendido"] = Produto.objects.filter(Categoria=categoria_id).order_by("-quantidade_vendas")
            context["ProdutosMaisVistos"] = Produto.objects.filter(Categoria=categoria_id).order_by("-visualizacao")

        return context

class PesquisarAdminView(AdminRequireMixin, BaseContextMixin, TemplateView):
    template_name = "admin_paginas/PesquisarAdmin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        kw = self.request.GET.get("query")
        desamb = self.request.GET.get("desambiguidade")
        pedido = PedidoOrder.objects.filter(Q(nome_cliente__icontains = kw) | Q(email__icontains = kw) | Q(id__iexact = kw)).order_by("-id")
        produto = Produto.objects.filter(Q(codigo__iexact = kw) | Q(codigo_GTIN__iexact = kw) | Q(slug__iexact = kw) | Q(descricao__icontains = kw) | Q(titulo__icontains = kw) | Q(Categoria__titulo__icontains = kw))
        
        if produto.exists() and not pedido.exists():
            context['produto'] = True
            context['pedido'] = False

            paginator = Paginator(produto, 20)
            page_number = self.request.GET.get('page')
            result = paginator.get_page(page_number)
        elif pedido.exists() and not produto.exists():
            context['produto'] = False
            context['pedido'] = True
            result = pedido
        elif pedido.exists() and produto.exists():
            if desamb == "produto":
                context['produto'] = True
                context['pedido'] = False

                paginator = Paginator(produto, 20)
                page_number = self.request.GET.get('page')
                result = paginator.get_page(page_number)
            elif desamb == "pedido":
                context['produto'] = False
                context['pedido'] = True
                result = pedido
            else:
                context['produto'] = True
                context['pedido'] = True
                result = None
        else:
            result = None

        context['resultados'] = result

        return context
    
def consultar_checkout_pag(request):
    if request.method == 'POST':
        # print(request.POST)
        if request.POST["checkout_id"]:
            pedido = PedidoOrder.objects.get(id=request.POST["pedido_id"])

            url = "https://api.pagseguro.com/checkouts/" + request.POST["checkout_id"] + "?offset=0&limit=10"

            headers = {
                "accept": "*/*",
                "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN,
            }

            consulta_response = requests.get(url, headers=headers)
                    
            if consulta_response.status_code >= 200 and consulta_response.status_code < 300:
                respJson = consulta_response.json()
                # print(respJson)
                try:
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
                        # print(charges)
                        return render(request, "admin_paginas/adminpedidodetalhe.html", {"pedido_obj":pedido,"PEDIDO_STATUS":PEDIDO_STATUS, "data_Pag":charges, "pagseguro_display":True})
                        # return JsonResponse(charges)
                    else:
                        # TODO: Melhorar essa tela de erro pra versão final
                        return HttpResponse(f"Error: {order_response.status_code} - {order_response.text}")
                except:
                    # messages.success(request, 'Pagamento não finalizado')
                    messages.success(request, f"Error: {order_response.status_code} - {order_response.text}")
                    print((f"Error: {order_response.status_code} - {order_response.text}"))
                    return render(request, "admin_paginas/adminpedidodetalhe.html", {"pedido_obj":pedido,"PEDIDO_STATUS":PEDIDO_STATUS})
            else:
                # TODO: Melhorar essa tela de erro pra versão final
                return HttpResponse(f"Error: {consulta_response.status_code} - {consulta_response.text}")
        
    return HttpResponse("Invalid request.")

def cancelar_checkout_pag(request):
    if request.method == 'POST':
        # print(request.POST)
        # pedido = PedidoOrder.objects.get(id=request.POST["pedido_id"])
        url = "https://internal.api.pagseguro.com/charges/" + request.POST["id_cancel"] + "/cancel"
        # internal.

        payload = { "amount": { "value": request.POST["valor_pago"] } }

        headers = {
            "accept": "*/*",
            "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN,
            "Content-type": "application/json"
        }

        cancelar_response = requests.get(url, json=payload, headers=headers)

        if cancelar_response.status_code >= 200 and cancelar_response.status_code < 300:
            print(cancelar_response.text)

            pedido = PedidoOrder.objects.get(id=request.POST["pedido_id"])
            EmailPedidoCancelado(pedido)
        else:
            # TODO: Melhorar essa tela de erro pra versão final
            return HttpResponse(f"Error: {cancelar_response.status_code} - {cancelar_response.text}")
        
    return HttpResponse("Invalid request.")

def test_atualizacao_pag(request):
    # if request.method == 'POST':
    #     pedido_id = "52"
    #     pedido = PedidoOrder.objects.get(id=pedido_id)

    #     notification_code = request.POST.get("notificationCode")
    #     notification_type = request.POST.get("notificationType")

    #     if notification_type == "transaction":
    #         pedido.status_test = notification_code
    #         pedido.save()

    #     return JsonResponse({"status": "success"}, status=200)

    # return HttpResponse("Invalid request.")
    if request.method == 'POST':
        t = TestStatus.objects.create(status="POST")
    elif request.method == 'GET':
        t = TestStatus.objects.create(status="GET")
    else:
        t = TestStatus.objects.create(status="cu")
    t.save()

    tt = TestStatus.objects.create(status="cucu")
    tt.save()

    return True

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

# API
## Test
### List all products or create a new one
class TestListCreateView(generics.ListCreateAPIView):
    queryset = TestStatus.objects.all()
    serializer_class = TestSerializer

    permission_classes = [HasAPIKey]
    # permission_classes = [HasAPIKey | IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.AllowAny]  # Allows all users

### Retrieve, update, or delete a specific product
class TestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestStatus.objects.all()
    serializer_class = TestSerializer

    permission_classes = [HasAPIKey]

## Categoria
class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    permission_classes = [HasAPIKey]

class CategoriaDetailView(generics.RetrieveAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = "slug"

    permission_classes = [HasAPIKey]

## Produto
class ProdutoListCreateView(generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [HasAPIKey]

    def perform_create(self, serializer):
        produto = serializer.save()  # Save the initial model instance
        
        image_field = produto.image
        
        if image_field:
            temp_file_path = image_field.path

            # Converte pra webp
            file, ext = os.path.splitext(temp_file_path)
            image = Image.open(temp_file_path).convert("RGB")
            new_path = f"{file}.webp"
            image.save(new_path, "webp")

            # Remove o original
            if ext != ".webp":
                os.remove(temp_file_path)

            # Update the model with the new WebP image
            produto.image.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
            produto.save()

class ProdutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "codigo"

    permission_classes = [HasAPIKey]

    def perform_update(self, serializer):
        produto = serializer.save()  # Save the updated model instance
        
        # Check if an image was updated
        if "image" in self.request.FILES:
            image_field = produto.image  # Get the updated image
            
            if image_field:
                temp_file_path = image_field.path  # Get the file path

                # Converte pra webp
                file, ext = os.path.splitext(temp_file_path) 
                image = Image.open(temp_file_path).convert("RGB")
                new_path = f"{file}.webp"
                image.save(new_path, "webp")

                # Remove o original
                if ext != ".webp":
                    os.remove(temp_file_path)

                # Update the model with the new WebP image
                produto.image.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
                produto.save()

    def perform_destroy(self, instance):
        if instance.image:
            image_path = instance.image.path

            if os.path.exists(image_path):
                os.remove(image_path)  # Delete the file from storage

        instance.delete()

class ChunkedProdutoJsonUploadView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        file_id = request.data.get("file_id")
        chunk_index = request.data.get("chunk_index")
        total_chunks = request.data.get("total_chunks")
        json_chunk = request.data.get("chunk_data")     # JSON chunk as string

        cache_key = f"json_upload_{file_id}_{chunk_index}"
        cache.set(cache_key, json_chunk)

        if int(chunk_index) + 1 == int(total_chunks):
            full_json = ""
            for i in range(int(total_chunks)):
                chunk = cache.get(f"json_upload_{file_id}_{i}")
                if chunk:
                    full_json += chunk
                    cache.delete(f"json_upload_{file_id}_{i}")

            try:
                data_str = json.loads(full_json)
                data = json.loads(data_str)             # Convert JSON string to Python object

                for i in range(len(data["codigo"])):
                    cat_slug = unicodedata.normalize('NFKD', data["categoria"][str(i)]).encode('ascii', 'ignore').decode('utf-8').lower().replace(" ", "_")
                    categoria_id = Categoria.objects.get(slug=cat_slug)

                    img = "produtos/" + data["codigo"][str(i)] + ".webp"

                    # if data["em_estoque"][str(i)]:
                    #     emEst = True
                    # else:
                    #     emEst = False
                        
                    Produto.objects.create(codigo=data["codigo"][str(i)],descricao=data["descricao"][str(i)],codigo_GTIN=data["codigo_GTIN"][str(i)],
                                           preco_unitario_bruto=data["preco_unitario_bruto"][str(i)],desconto_dinheiro=data["desconto_dinheiro"][str(i)],
                                           desconto_retira=data["desconto_retira"][str(i)],unidade=data["unidade"][str(i)],titulo=data["titulo"][str(i)],
                                           fechamento_embalagem=data["fechamento_embalagem"][str(i)],slug=data["slug"][str(i)],
                                           Categoria=categoria_id,image=img,)#em_estoque=emEst,)
                    
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON"}, status=400)
            
            return Response({"message": "JSON Upload Complete"})

        return Response({"message": "Chunk received"})

class ChunkedProdutoJsonUpdateView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        file_id = request.data.get("file_id")
        chunk_index = request.data.get("chunk_index")
        total_chunks = request.data.get("total_chunks")
        json_chunk = request.data.get("chunk_data")     # JSON chunk as string

        cache_key = f"json_upload_{file_id}_{chunk_index}"
        cache.set(cache_key, json_chunk)

        if int(chunk_index) + 1 == int(total_chunks):
            full_json = ""
            for i in range(int(total_chunks)):
                chunk = cache.get(f"json_upload_{file_id}_{i}")
                if chunk:
                    full_json += chunk
                    cache.delete(f"json_upload_{file_id}_{i}")

            try:
                data_str = json.loads(full_json)
                data = json.loads(data_str)             # Convert JSON string to Python object

                for i in range(len(data["codigo"])):
                    try:
                        prod = Produto.objects.get(codigo=data["codigo"][str(i)])
                        cat_slug = unicodedata.normalize('NFKD', data["categoria"][str(i)]).encode('ascii', 'ignore').decode('utf-8').lower().replace(" ", "_")

                        # print(cat_slug)
                        categoria_id = Categoria.objects.get(slug=cat_slug)

                        # if data["em_estoque"][str(i)]:
                        #     emEst = True
                        # else:
                        #     emEst = False

                        prod.descricao = data["descricao"][str(i)]
                        prod.codigo_GTIN = data["codigo_GTIN"][str(i)]
                        prod.preco_unitario_bruto = data["preco_unitario_bruto"][str(i)]
                        prod.desconto_dinheiro = data["desconto_dinheiro"][str(i)]
                        prod.desconto_retira = data["desconto_retira"][str(i)]
                        prod.unidade = data["unidade"][str(i)]
                        prod.fechamento_embalagem = data["fechamento_embalagem"][str(i)]
                        # prod.em_estoque = emEst
                        prod.slug = data["slug"][str(i)]
                        prod.Categoria = categoria_id
                        prod.titulo = data["titulo"][str(i)]

                        prod.save()

                    except Produto.DoesNotExist:
                        cat_slug = unicodedata.normalize('NFKD', data["categoria"][str(i)]).encode('ascii', 'ignore').decode('utf-8').lower().replace(" ", "_")
                        categoria_id = Categoria.objects.get(slug=cat_slug)

                        img = "produtos/" + data["codigo"][str(i)] + ".webp"

                        # if data["em_estoque"][str(i)]:
                        #     emEst = True
                        # else:
                        #     emEst = False

                        Produto.objects.create(codigo=data["codigo"][str(i)],descricao=data["descricao"][str(i)],codigo_GTIN=data["codigo_GTIN"][str(i)],
                                               preco_unitario_bruto=data["preco_unitario_bruto"][str(i)],desconto_dinheiro=data["desconto_dinheiro"][str(i)],
                                               desconto_retira=data["desconto_retira"][str(i)],unidade=data["unidade"][str(i)],titulo=data["titulo"][str(i)],
                                               fechamento_embalagem=data["fechamento_embalagem"][str(i)],slug=data["codigo"][str(i)],
                                               Categoria=categoria_id,image=img,)#em_estoque=emEst,)
                        
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON"}, status=400)
            
            return Response({"message": "JSON Upload Complete"})

        return Response({"message": "Chunk received"})

class ChunkedEstoqueJsonUploadView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        file_id = request.data.get("file_id")
        chunk_index = request.data.get("chunk_index")
        total_chunks = request.data.get("total_chunks")
        json_chunk = request.data.get("chunk_data")     # JSON chunk as string

        cache_key = f"json_upload_{file_id}_{chunk_index}"
        cache.set(cache_key, json_chunk)

        if int(chunk_index) + 1 == int(total_chunks):
            full_json = ""
            for i in range(int(total_chunks)):
                chunk = cache.get(f"json_upload_{file_id}_{i}")
                if chunk:
                    full_json += chunk
                    cache.delete(f"json_upload_{file_id}_{i}")

            try:
                data_str = json.loads(full_json)
                data = json.loads(data_str)             # Convert JSON string to Python object
                
                for i in range(len(data["codigo"])):
                    try:
                        produto = Produto.objects.get(codigo=data["codigo"][str(i)])
                    except Produto.DoesNotExist:
                        continue
                    
                    estoque_lojas_json = {
                                    "Casa HG - Várzea": data["varzea_disponivel"][str(i)],
                                    "Casa HG - Magé/Guapimirim": data["guapi_disponivel"][str(i)],
                                    "Casa HG - Atacadão Dos Pisos": data["prata_disponivel"][str(i)]
                                   }
                    
                    produto.estoque_lojas = estoque_lojas_json
                    
                    produto.save()
                    
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON"}, status=400)
            
            return Response({"message": "JSON Upload Complete"})

        return Response({"message": "Chunk received"})

class ChunkedProdutoPisoFichaTecJsonUploadView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        file_id = request.data.get("file_id")
        chunk_index = request.data.get("chunk_index")
        total_chunks = request.data.get("total_chunks")
        json_chunk = request.data.get("chunk_data")     # JSON chunk as string

        cache_key = f"json_upload_{file_id}_{chunk_index}"
        cache.set(cache_key, json_chunk)

        if int(chunk_index) + 1 == int(total_chunks):
            full_json = ""
            for i in range(int(total_chunks)):
                chunk = cache.get(f"json_upload_{file_id}_{i}")
                if chunk:
                    full_json += chunk
                    cache.delete(f"json_upload_{file_id}_{i}")

            try:
                data_str = json.loads(full_json)
                data = json.loads(data_str)             # Convert JSON string to Python object

                for i in range(len(data["codigo"])):
                    try:
                        prod = Produto.objects.get(codigo=data["codigo"][str(i)])
                    except Produto.DoesNotExist:
                        continue
                    # Pega os tuples com todas as opções, transforma eles em dicionarios e faz o match pro valor lido pelo django
                    if data["Classe tecnica (absorcao)"][str(i)]:
                        dataCTA = unicodedata.normalize('NFKD', data["Classe tecnica (absorcao)"][str(i)]).encode('ascii', 'ignore').decode('utf-8').lower().replace(" ", "_")
                        classe_tecnica_absorcao_pisos_field = Produto._meta.get_field('classe_tecnica_absorcao_pisos')
                        display_to_value_cta = {unicodedata.normalize('NFKD', label).encode('ascii', 'ignore').decode('utf-8').lower().replace(" ", "_"): value 
                                                for value, label in classe_tecnica_absorcao_pisos_field.choices}
                        cta = display_to_value_cta.get(dataCTA)
                    else:
                        cta = None
                    
                    if data["Variacao de faces"][str(i)]:
                        variacao_faces_field = Produto._meta.get_field('variacao_faces')
                        display_to_value_va = {label.lower(): value for value, label in variacao_faces_field.choices}
                        vf = display_to_value_va.get(data["Variacao de faces"][str(i)].lower())
                    else:
                        vf = None
                    
                    if data["Indicacao de uso"][str(i)]:
                        indicacao_uso_field = Produto._meta.get_field('indicacao_uso')
                        display_to_value_iu = {label.lower(): value for value, label in indicacao_uso_field.choices}
                        iu = display_to_value_iu.get(data["Indicacao de uso"][str(i)].lower())
                    else:
                        iu = None

                    prod.marca = data["Marca"][str(i)]
                    prod.formato = data["Formato"][str(i)]
                    prod.espessura = data["Espessura"][str(i)]
                    prod.junta_minima = data["Junta Minima"][str(i)]
                    prod.relevo = data["Relevo"][str(i)]
                    prod.acabamento_superficial = data["Acabamento superficial"][str(i)]
                    prod.classe_tecnica_absorcao_pisos = cta
                    prod.variacao_faces = vf
                    prod.indicacao_uso = iu
                    prod.pecas_caixa = data["Pecas Caixa"][str(i)]
                    prod.peso_bruto_caixa = data["Peso Bruto Caixa"][str(i)]
                    prod.palet = data["Palet"][str(i)]

                    prod.save()
                    
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON"}, status=400)
            
            return Response({"message": "JSON Upload Complete"})

        return Response({"message": "Chunk received"})

class ChunkedProdutoImgUploadView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        file_name = request.POST.get("file_name")  # Name of the image file
        chunk_index = int(request.POST.get("chunk_index", 0))  # Current chunk index
        total_chunks = int(request.POST.get("total_chunks", 1))  # Total chunks expected

        # Define the target directory
        upload_dir = os.path.join(settings.MEDIA_ROOT, "produtos")
        os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists

        # Define the temporary file path
        temp_file_path = os.path.join(upload_dir, file_name)

        # Append the chunk to the file
        with open(temp_file_path, "ab") as f:
            f.write(request.FILES["file"].read())

        # If this is the last chunk, return the final file path
        if chunk_index + 1 == total_chunks:
            # Converte pra webp
            file, ext = os.path.splitext(temp_file_path)
            image = Image.open(temp_file_path).convert("RGB")
            image.save(file + ".webp", "webp")
            converted_file_path = file + ".webp"

            # Remove o original
            if ext != ".webp":
                os.remove(temp_file_path)
            
            file_url = os.path.join(settings.MEDIA_URL, "produtos", os.path.basename(converted_file_path))
            return JsonResponse({"message": "Upload complete", "file_url": file_url})

        return JsonResponse({"message": "Chunk received", "chunk_index": chunk_index})

class ProdutoStatsView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        file_path_vendas = os.path.join(settings.MEDIA_ROOT, "data", "vendas.json")
        file_path_visuli = os.path.join(settings.MEDIA_ROOT, "data", "visualizacao.json")
        try:
            with open(file_path_vendas, "r") as file:
                vendas_dic = json.load(file)
            with open(file_path_visuli, "r") as file:
                visuli_dic = json.load(file)
        except:
            return Response({"error": "Files don't exist"}, status=400)
        
        return Response({'Vendas_json': vendas_dic, 'Visualizacao_json': visuli_dic})

## Fotos Produto
class FotosProdutoListCreateView(generics.ListCreateAPIView):
    queryset = FotosProduto.objects.all()
    serializer_class = FotosProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [HasAPIKey]

    def perform_create(self, serializer):
        prod_cod = self.request.data.get('codigo')
        # produto = Produto.objects.get(codigo=prod_cod)
        prod = get_object_or_404(Produto, codigo=prod_cod)

        fotoProduto = serializer.save(produto=prod)  # Save the initial model instance
        
        image_field = fotoProduto.image
        
        if image_field:
            temp_file_path = image_field.path

            # Converte pra webp
            file, ext = os.path.splitext(temp_file_path)
            image = Image.open(temp_file_path).convert("RGB")
            new_path = f"{file}.webp"
            image.save(new_path, "webp")

            # Remove o original
            if ext != ".webp":
                os.remove(temp_file_path)

            # Update the model with the new WebP image
            fotoProduto.image.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
            fotoProduto.produto.num_fotos -= 1
            fotoProduto.save()

class FotosProdutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FotosProduto.objects.all()
    serializer_class = FotosProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [HasAPIKey]

    def perform_update(self, serializer):
        fotoProduto = serializer.save()  # Save the updated model instance
        
        # Check if an image was updated
        if "image" in self.request.FILES:
            image_field = fotoProduto.image  # Get the updated image
            
            if image_field:
                temp_file_path = image_field.path  # Get the file path

                # Converte pra webp
                file, ext = os.path.splitext(temp_file_path) 
                image = Image.open(temp_file_path).convert("RGB")
                new_path = f"{file}.webp"
                image.save(new_path, "webp")

                # Remove o original
                if ext != ".webp":
                    os.remove(temp_file_path)

                # Update the model with the new WebP image
                fotoProduto.image.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
                fotoProduto.produto.num_fotos -= 1
                fotoProduto.save()

class FotosProdutoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [HasAPIKey]

    def post(self, request):
        prod_cod = request.data.get('codigo')
        prod = get_object_or_404(Produto, codigo=prod_cod)
        img = request.FILES.get('image')

        fotosExistentes = FotosProduto.objects.filter(produto=prod)
        image_field = None
        # Verificação se a foto já existe
        if fotosExistentes:
            for fotoObj in fotosExistentes:
                # Se a foto já existe
                if os.path.splitext(os.path.basename(fotoObj.image.url))[0] == os.path.splitext(os.path.basename(img.name))[0]:
                    upload_dir = fotoObj.image.path
                    upload_dir = upload_dir.replace(os.path.basename(fotoObj.image.url), "")
                    file_name = img.name

                    temp_file_path = os.path.join(upload_dir, file_name)

                    # Remove o original
                    os.remove(fotoObj.image.path)

                    # Converte pra webp
                    image = Image.open(img).convert("RGB")
                    new_path = f"{os.path.splitext(temp_file_path)[0]}.webp"

                    # Salva o novo
                    image.save(new_path, "webp")

                    return JsonResponse({"message": "Foto atualizada", "Produto": fotoObj.produto.codigo, "file_url": fotoObj.image.url})

        # Se a foto for nova
        if not image_field:
            fotoProduto = FotosProduto.objects.create(produto=prod, image=img)
            
            image_field = fotoProduto.image
        
            if image_field:
                temp_file_path = image_field.path

                # Converte pra webp
                file, ext = os.path.splitext(temp_file_path)
                image = Image.open(temp_file_path).convert("RGB")
                new_path = f"{file}.webp"
                image.save(new_path, "webp")

                # Remove o original
                if ext != ".webp":
                    os.remove(temp_file_path)

                # Update the model with the new WebP image
                fotoProduto.image.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
                # fotoProduto.produto.num_fotos -= 1
                fotoProduto.save()

            return JsonResponse({"message": "Nova foto criada", "Produto": fotoProduto.produto.codigo, "file_url": fotoProduto.image.url})

## Pedido Order
class PedidoOrderListCreateView(generics.ListCreateAPIView):
    queryset = PedidoOrder.objects.prefetch_related("pedidoProduto")
    serializer_class = PedidoOrderSerializer

    permission_classes = [HasAPIKey]

class PedidoOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PedidoOrder.objects.prefetch_related("pedidoProduto")
    serializer_class = PedidoOrderSerializer

    permission_classes = [HasAPIKey]

    def perform_update(self, serializer):
        pedido_obj = serializer.save()
        
        # Check if an image was updated
        if "pedido_status" in self.request.data:
            novo_status = pedido_obj.pedido_status

            if novo_status == "Pedido Recebido":
                    EmailPedidoRealizado(pedido_obj)
            elif novo_status == "Pagamento Confirmado":
                    EmailPedidoPagamentoConfirmado(pedido_obj)
            elif novo_status == "Pedido Caminho":
                    EmailPedidoEnviado(pedido_obj)
            elif novo_status == "Pedido Pronta Retirada":
                    EmailPedidoProntoRetirada(pedido_obj)
            elif novo_status == "Pagamento Cancelado":
                    EmailPedidoCancelado(pedido_obj)
            elif novo_status == "Pagamento Completado":
                    EmailPedidoCompleto(pedido_obj)

## Pedido Produto
class PedidoProdutoListCreateView(generics.ListCreateAPIView):
    queryset = PedidoProduto.objects.all()
    serializer_class = PedidoProdutoSerializer

    permission_classes = [HasAPIKey]

class PedidoProdutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PedidoProduto.objects.all()
    serializer_class = PedidoProdutoSerializer

    permission_classes = [HasAPIKey]

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ #

# verifica se todos os produtos tem fotos
def ChecaFotosProdutos(request):
    for prod in Produto.objects.all():
        path = (settings.MEDIA_ROOT + prod.image.url).replace("media/media", "media")

        if os.path.exists(path):
            if prod.image.url == "/media/produtos/NoImgAvailable.webp":
                pathCodigo = f"{settings.MEDIA_ROOT}/produtos/{prod.codigo}.webp"

                if prod.num_fotos == 1:
                    if os.path.exists(pathCodigo):
                        new_path = f"/produtos/{prod.codigo}.webp"
                        prod.image.name = new_path#os.path.relpath(new_path, settings.MEDIA_ROOT)
                        prod.save()
                else:
                    try:
                        newFotoObjeto = FotosProduto.objects.get(produto=prod, img_num=2)
                        new_path = newFotoObjeto.image.name
                        prod.image.name = new_path
                        prod.save()
                    except FotosProduto.DoesNotExist:
                        prod.num_fotos = 1

                        if os.path.exists(pathCodigo):
                            new_path = f"/produtos/{prod.codigo}.webp"
                            prod.image.name = new_path

                        prod.save()
        else:
            pathCodigo = f"{settings.MEDIA_ROOT}/produtos/{prod.codigo}.webp"
            if os.path.exists(pathCodigo):
                new_path = f"/produtos/{prod.codigo}.webp"
            else:
                new_path = "/produtos/NoImgAvailable.webp"
            prod.image.name = new_path#os.path.relpath(new_path, settings.MEDIA_ROOT)
            prod.save()

    if request.method == 'POST':
        return redirect(request.POST["path"])
    
# Reseta o numero de fotos de todos os produtos
def ResetaFotosProdutos(request):
    for prod in Produto.objects.all():
        prod.num_fotos = 1

        if os.path.exists(f"{settings.MEDIA_ROOT}/produtos/{prod.codigo}.webp"):
            new_path = f"/produtos/{prod.codigo}.webp"            
        else:
            new_path = "/produtos/NoImgAvailable.webp"
        prod.image.name = new_path

        prod.save()

    if request.method == 'POST':
        return redirect(request.POST["path"])
    
# Fotos extras pros produtos
## Lança fotos
def upload_imagem_extra_produtos(request):
    if request.method == 'POST':
        form = ProdutosImagemExtraForm(request.POST, request.FILES)
        if form.is_valid():
            produto = Produto.objects.get(codigo=request.POST['produto'])
            fotoProduto = form.save(commit=False)
            fotoProduto.produto = produto
            fotoProduto.save()

            foto = form.cleaned_data.get('image')

            path = (settings.MEDIA_ROOT + fotoProduto.image.url).replace("media/media", "media")

            # meu codigo
            temp_file_path = path

            # Converte pra webp
            file, ext = os.path.splitext(temp_file_path)
            image = Image.open(temp_file_path).convert("RGB")
            new_path = f"{file}.webp"
            image.save(new_path, "webp")

            # Remove o original
            if ext != ".webp":
                os.remove(temp_file_path)

            # Update the model with the new WebP image
            fotoProduto.image.name = os.path.relpath(new_path, settings.MEDIA_ROOT)
            # produto.num_fotos -= 1
            fotoProduto.save()

            return redirect(request.POST["path"])
        else:
            print("Form Errors:", form.errors)
    else:
        form = ProdutosImagemExtraForm()
    return redirect(request.POST["path"])

## Deleta fotos
def delete_imagem_extra_produtos(request):
    if request.method == 'POST':
        try:
            foto = FotosProduto.objects.get(id=request.POST['foto'])

            foto.delete()

            return redirect(request.POST["path"])
        except foto.DoesNotExist:
            return Response({'error': 'foto não encontrada'}, status=status.HTTP_400_BAD_REQUEST)
        
    return redirect(request.POST["path"])

# Verifica que o pedido online ta pago
def ta_pago(_pedido):
    url = "https://api.pagseguro.com/checkouts/" + _pedido.id_PagBank + "?offset=0&limit=10"

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN,
    }

    consulta_response = requests.get(url, headers=headers)
    
    try:
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
    except:
        return False
            
    return False

# Formata o valor do preço dos produtos para mostrar de forma mais interessante no site
def preprocessar_precos(_produtos):
        for produto in _produtos:
            venda_parts = str(produto.preco_unitario_bruto).split('.')
            precoDesc = round((produto.preco_unitario_bruto * (1 - ((produto.desconto_dinheiro + produto.desconto_retira) / 100))), 2)
            venda_parts_desc = str(precoDesc).split('.')
            precoCaixa = round((produto.preco_unitario_bruto * produto.fechamento_embalagem), 2)
            venda_parts_caixa = str(precoCaixa).split('.')
            # Preço unitario
            produto.integer_part_uni = venda_parts[0]
            produto.decimal_part_uni = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
            # Preço caixa
            produto.integer_part_caixa = venda_parts_caixa[0]
            produto.decimal_part_caixa = venda_parts_caixa[1] if len(venda_parts_caixa) > 1 else '00'  # Adiciona '00' se não houver parte decimal
            # Preço unitario com desconto de dinheiro retirada
            produto.integer_part_desc = venda_parts_desc[0]
            produto.decimal_part_desc = venda_parts_desc[1] if len(venda_parts_desc) > 1 else '00'  # Adiciona '00' se não houver parte decimal

        return _produtos

# Gera json com historico de vendas e visualizações de cada produto
def geraHistoricoProdutos(_produtos):
    data = datetime.datetime.now()    
    mes = f"{data.year}-{data.month - 1}"

    file_path_vendas = os.path.join(settings.MEDIA_ROOT, "data", "vendas.json")
    file_path_visuli = os.path.join(settings.MEDIA_ROOT, "data", "visualizacao.json")

    try:
        with open(file_path_vendas, "r") as file:
            vendas_dic = json.load(file)
        with open(file_path_visuli, "r") as file:
            visuli_dic = json.load(file)
    except:
        vendas_dic = {}
        visuli_dic = {}

    if mes not in vendas_dic and mes not in visuli_dic:
        vendas_dic_mes = {mes: {}}
        visuli_dic_mes = {mes: {}}

        for produto in _produtos:
            vendas_dic_mes[mes].update({produto.codigo: produto.quantidade_vendas})
            visuli_dic_mes[mes].update({produto.codigo: produto.visualizacao})

        vendas_dic.update(vendas_dic_mes)
        visuli_dic.update(visuli_dic_mes)

        with open(file_path_vendas, "w") as file:
            json.dump(vendas_dic, file, indent=4)
        with open(file_path_visuli, "w") as file:
            json.dump(visuli_dic, file, indent=4)

# Função para tokens de verificação da conta
def generate_verification_token(user):
    return default_token_generator.make_token(user)

def encode_user_id(user):
    return urlsafe_base64_encode(force_bytes(user.pk))

# Funções de email
## Email enviado ao cliente ao criar sua conta
def EmailClienteRegistrado(_cliente):
    token = generate_verification_token(_cliente)
    uid = encode_user_id(_cliente)

    assunto = "Boas-vindas à CasaHG"
    text_content = "Obrigado por se cadastrar!"
    html_content = render_to_string(
                        "emails/emailClienteRegistrado.html",
                        context={
                            "cliente": _cliente,
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                            "linkVerif": f"https://www.loja-casahg.com.br{reverse('lojaapp:verifica_user', kwargs={'uidb64': uid, 'token': token})}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_cliente.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
def EmailVerificaCliente(_cliente):
    token = generate_verification_token(_cliente)
    uid = encode_user_id(_cliente)

    assunto = "Verificação de conta CasaHG"
    text_content = "Verificação de conta."
    html_content = render_to_string(
                        "emails/emailVerificaCLiente.html",
                        context={
                            "cliente": _cliente,
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                            "linkVerif": f"https://www.loja-casahg.com.br{reverse('lojaapp:verifica_user', kwargs={'uidb64': uid, 'token': token})}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_cliente.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

## Emails de status do pedido
def EmailPedidoRealizado(_pedido):
    assunto = f"Pedido da CasaHG #{_pedido.id} - {_pedido.pedido_status}"
    text_content = f"Pedido #{_pedido.id} realizado"
    html_content = render_to_string(
                        "emails/emailPedidoRealizado.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": f"https://www.loja-casahg.com.br/perfil/pedido-{_pedido.id}",
                            "statusImg": "http://www.loja-casahg.com.br/media/progressoPedido/Pedido_Recebido.png",
                            # TODO: Verificar esse link da imagem
                            # https://www.loja-casahg.com.br/media/empresas/hg-teste_jXgRLs3.png
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_pedido.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def EmailPedidoPagamentoConfirmado(_pedido):
    assunto = f"Pedido da CasaHG #{_pedido.id} - {_pedido.pedido_status}"
    text_content = f"Pedido #{_pedido.id} pagamento confirmado"
    html_content = render_to_string(
                        "emails/emailPedidoPagamentoConfirmado.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": f"https://www.loja-casahg.com.br/perfil/pedido-{_pedido.id}",
                            "statusImg": "http://www.loja-casahg.com.br/media/progressoPedido/Pagamento_Confirmado.png",
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_pedido.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def EmailPedidoEnviado(_pedido):
    assunto = f"Pedido da CasaHG #{_pedido.id} - {_pedido.pedido_status}"
    text_content = f"Pedido #{_pedido.id} enviado"
    html_content = render_to_string(
                        "emails/emailPedidoEnviado.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": f"https://www.loja-casahg.com.br/perfil/pedido-{_pedido.id}",
                            "statusImg": "http://www.loja-casahg.com.br/media/progressoPedido/Pedido_Caminho.png",
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_pedido.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def EmailPedidoProntoRetirada(_pedido):
    assunto = f"Pedido da CasaHG #{_pedido.id} - {_pedido.pedido_status}"
    text_content = f"Pedido #{_pedido.id} pronto para retirada"
    html_content = render_to_string(
                        "emails/emailPedidoProntoRetirada.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": f"https://www.loja-casahg.com.br/perfil/pedido-{_pedido.id}",
                            "statusImg": "http://www.loja-casahg.com.br/media/progressoPedido/Pedido_Caminho.png",
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_pedido.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def EmailPedidoCancelado(_pedido):
    assunto = f"Pedido da CasaHG #{_pedido.id} - {_pedido.pedido_status}"
    text_content = f"Pedido #{_pedido.id} cancelado"
    html_content = render_to_string(
                        "emails/emailPedidoCancelado.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": f"https://www.loja-casahg.com.br/perfil/pedido-{_pedido.id}",
                            "statusImg": "http://www.loja-casahg.com.br/media/progressoPedido/Pedido_Cancelado.png",
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_pedido.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def EmailPedidoCompleto(_pedido):
    assunto = f"Pedido da CasaHG #{_pedido.id} - {_pedido.pedido_status}"
    text_content = f"Pedido #{_pedido.id} completado"
    html_content = render_to_string(
                        "emails/emailPedidoCompleto.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": f"https://www.loja-casahg.com.br/perfil/pedido-{_pedido.id}",
                            "statusImg": "http://www.loja-casahg.com.br/media/progressoPedido/Pedido_Completado.png",
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_pedido.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

## Email de teste
def testEmail(_emailCliente, _cliente, _pedido):
    # assunto = "Boas-vindas à CasaHG"
    # text_content = "Obrigado por se cadastrar!"
    # html_content = render_to_string(
    #                     "emails/emailClienteRegistrado.html",
    #                     context={
    #                         "cliente": _cliente,
    #                         "logo": "https://www.loja-casahg.com.br" + Empresa.objects.get(titulo="Casa HG").image.url,
    #                     },
    #                 )
    
    assunto = f"Pedido da CasaHG #{_pedido.id} - {_pedido.pedido_status}"
    text_content = f"Pedido #{_pedido.id} pagamento confirmado"
    html_content = render_to_string(
                        "emails/emailPedidoPagamentoConfirmado.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": f"https://www.loja-casahg.com.br/perfil/pedido-{_pedido.id}",
                            "statusImg": "http://www.loja-casahg.com.br/media/progressoPedido/Pagamento_Confirmado.png",
                            "logo": f"https://www.loja-casahg.com.br{Empresa.objects.get(titulo='Casa HG').image.url}",
                        },
                    )

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, [_emailCliente]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    # send_mail(
    #     "Assunto do email de test",
    #     "Corpo do email de teste",
    #     settings.EMAIL_HOST_USER,
    #     [_emailCliente],
    #     fail_silently=False,
    # )

# Função para testar requests de POST vindos do site
def testPOST(request):
    if request.method == 'POST':
        print(request.POST)

        return redirect(request.POST["path"])

    return HttpResponse("Invalid request.")