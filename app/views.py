import os
from .forms import *
from .models import *
from .serializers import *
from django_teste import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, DetailView, ListView
from django.views.generic.edit import DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.cache import cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import serializers, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.template.loader import render_to_string
from PIL import Image
from io import BytesIO
from random import randint
import requests
import decimal
import json

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
        
        carro_id = self.request.session.get("carro_id")
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            produtos = list(CarroProduto.objects.filter(carro=carro_obj))
            if produtos:
                context["numProdCarro"] = len(produtos)
        context['todoscategorias'] = Categoria.objects.all()
        context['footer'] = Empresa.objects.all()

        return context

class CrazyAlvaPaymentCheckMixin(object):
    def dispatch(self,request,*args,**kwargs):
        pedidos = list(Pedido_order.objects.filter(pedido_status="Pagamento Processando", local_de_pagamento="online"))
        # print(len(pedidos))
        if len(pedidos):
            pedido_aleatorio = pedidos[randint(0, len(pedidos))]

            if ta_pago(pedido_aleatorio):
                pedido_aleatorio.pedido_status = "Pagamento Confirmado"

        return super().dispatch(request,*args,**kwargs)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class HomeView(LojaMixin, BaseContextMixin, CrazyAlvaPaymentCheckMixin, TemplateView):
    template_name = "home.html"

    # def preprocessar_precos(self, produtos):
    #     for produto in produtos:
    #         precoCaixa = round((produto.preco_unitario_bruto * produto.fechamento_embalagem), 2)
    #         venda_parts_caixa = str(precoCaixa).split('.')
    #         venda_parts = str(produto.preco_unitario_bruto).split('.')
    #         produto.integer_part_uni = venda_parts[0]
    #         produto.decimal_part_uni = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #         produto.integer_part_caixa = venda_parts_caixa[0]
    #         produto.decimal_part_caixa = venda_parts_caixa[1] if len(venda_parts_caixa) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #     return produtos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_produtos = Produto.objects.all().order_by("-id")
        produto_list = preprocessar_precos(all_produtos)

        paginator = Paginator(produto_list, 20)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        context['mais_vendidos'] = preprocessar_precos(Produto.objects.all().order_by("-quantidade_vendas")[:7])

        context['banners'] = Banner.objects.all()

        # TODO: Apagar esse teste
        # testEmail("jggenio@gmail.com", User.objects.get(username="Alva"), Pedido_order.objects.get(id=96))

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
        context['API'] = list(TestStatus.objects.all())[-1]

        return context

class TodosProdutosView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "todos-produtos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class ProdutosDetalheView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "produtodetalhe.html"

    # def preprocessar_precos(self, produtos):
    #     for produto in produtos:
    #         precoCaixa = round((produto.preco_unitario_bruto * produto.fechamento_embalagem), 2)
    #         venda_parts_caixa = str(precoCaixa).split('.')
    #         venda_parts = str(produto.preco_unitario_bruto).split('.')
    #         produto.integer_part_uni = venda_parts[0]
    #         produto.decimal_part_uni = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #         produto.integer_part_caixa = venda_parts_caixa[0]
    #         produto.decimal_part_caixa = venda_parts_caixa[1] if len(venda_parts_caixa) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #     return produtos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']

        produto = Produto.objects.get(slug=url_slug)
        context['produto'] = produto

        produto.visualizacao += 1
        produto.save()

        context['preco_dinheiro'] = round((produto.preco_unitario_bruto * (1 - ((produto.desconto_dinheiro + produto.desconto_retira) / 100))), 2)
        
        context['preco_caixa'] = round(produto.preco_unitario_bruto * produto.fechamento_embalagem, 2)

        context['fotos_produtos'] = produto.images.all() #FotosProduto.objects.filter(produto=produto)

        produtos_similares_list = list(Produto.objects.filter(Categoria=produto.Categoria).order_by("-quantidade_vendas")[:12])
        if produto in produtos_similares_list:
            produtos_similares_list = list(Produto.objects.filter(Categoria=produto.Categoria).order_by("-quantidade_vendas")[:13])
            produtos_similares_list.pop(produtos_similares_list.index(produto))

        produtos_similares = preprocessar_precos(produtos_similares_list)
        context['produtos_similares'] = produtos_similares

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

        # return context
        return redirect("lojaapp:meucarro")

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

            order = Pedido_order.objects.filter(carro=carro_obj)
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

            order = Pedido_order.objects.filter(carro=carro)
            if order:
                order.delete()

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

        # desconto retirada
        desc_retirada = 0
        for prod in CarroProduto.objects.filter(carro=carro_obj):
            desc_retirada += prod.preco_unitario * prod.quantidade * (prod.produto.desconto_retira / 100)
        
        context["desconto_retirada"] = str(round(desc_retirada, 2))

        context["enderecos"] = Endereco.objects.filter(cliente=self.request.user.cliente).order_by("-id")
        context["enderecosLojas"] = Endereco.objects.filter(cliente=Cliente.objects.get(nome="Casa", sobrenome="HG"))

        return context
    
def pedido_carro_endereco(request):
    if request.method == 'POST':
        try:
            # if Pedido_order.objects.filter(carro=request.POST["carro_id"]):
                # print(request.POST)
                # Pedido_order.objects.get(carro=request.POST["carro_id"]).delete()
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

            
            if Pedido_order.objects.filter(carro=request.POST["carro_id"]):
                pedido = Pedido_order.objects.get(carro=request.POST["carro_id"])
                pedido.endereco_envio = endereco_envio
                pedido.endereco_envio_formatado = endereco_envio_formatado
                pedido.total_bruto = total_bruto
                pedido.frete = frete
                pedido.desconto_retirada = desconto_retirada
                pedido.total_final = total_final
            else:
                pedido = Pedido_order.objects.create(cliente=cliente, nome_cliente=nome_cliente, cpf_cnpj=cpf_cnpj, telefone=telefone, email=email, carro=carro, pedido_status=pedido_status, total_bruto=total_bruto, total_final=total_final, frete=frete, desconto_retirada=desconto_retirada, endereco_envio=endereco_envio, endereco_envio_formatado=endereco_envio_formatado)
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

        pedido = Pedido_order.objects.get(carro=carro_obj)
        context["pedido"] = pedido
    
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
            carro = pedido.carro
            produtos = CarroProduto.objects.filter(carro=carro)
            desc = 0
            desc_credito_list = [0.07, 0.04, 0.04, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            pedido.total_final = decimal.Decimal(request.POST["total_final"])

            pedido.desconto_forma_pagamento = decimal.Decimal(request.POST["desconto_pagamento"])

            pedido.total_desconto = pedido.desconto_forma_pagamento + pedido.desconto_retirada

            pedido.local_de_pagamento = request.POST["local_pagamento"]
            if "metodo_pagamento" in request.POST:
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

            # Cria os Pedido_Produto
            for produtosCarro in CarroProduto.objects.filter(carro=pedido.carro):
                produto = Produto.objects.get(id=produtosCarro.produto.id)
                Pedido_Produto.objects.create(pedido=pedido, produto=produto, codigo=produto.codigo, 
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

                return create_payment(request)
            else:
                # pedido.pedido_status = "Pagamento Pendente"
                # pedido.save()
                         
                # return redirect(request.POST["path"])
                return redirect(f"{reverse_lazy('lojaapp:pedidoconfirmado')}?id={pedido.id}")
            
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
                        "option": "INTEREST_FREE_INSTALLMENTS",
                        "value": pedido.parcelas
                    },
                    {
                        "option": "INSTALLMENTS_LIMIT",
                        "value": pedido.parcelas
                    }
                ]
            }
        ],
        "redirect_url": f"https://vendashg.pythonanywhere.com/pedido-cofirmado/?id={pedido.id}", # f"http://127.0.0.1:8000/pedido-cofirmado/?id={pedido.id}&status=Pagamento_Confirmado",
        # f"{reverse_lazy('lojaapp:pedidoconfirmado')}?id={pedido.id}&status=Pagamento_Confirmado"
        # "notification_urls": ["https://vendashg.pythonanywhere.com/test_atualizacao_pag/"],
        # "payment_notification_urls": ["https://vendashg.pythonanywhere.com/test_atualizacao_pag/"]
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
                "name": prod.produto.descricao,
                "description": prod.produto.descricao,
                "quantity": prod.quantidade,
                "unit_amount": int((prod.subtotal / prod.quantidade) * 100),
                "image_url": "https://vendashg.pythonanywhere.com" + prod.produto.image.url
            }
        )

    headers = {
        "accept": "*/*",
        "Authorization": "Bearer " + settings.PAGSEGURO_TOKEN_SANDBOX,
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

        # TODO: Acho que só funfa automaticamente pra cartão de credito
        # Muda status do pedido
        pedido = Pedido_order.objects.get(id=pedido_id)

        EmailPedidoRealizado(pedido)

        if pedido.local_de_pagamento == "online":
            if ta_pago(pedido):
                pedido.pedido_status = "Pagamento Confirmado"
        else:
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

        EmailClienteRegistrado(user)

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
        # print(perfil_select)

        cliente = self.request.user.cliente
        context['cliente'] = cliente

        
        pedidos = Pedido_order.objects.filter(carro__cliente=cliente).order_by("-id")
        paginator = Paginator(pedidos, 6)
        page_number = self.request.GET.get('page')
        context['pedidos'] = paginator.get_page(page_number)
        # context['pedidos'] = pedidos

        enderecos = Endereco.objects.filter(cliente=cliente).order_by("-id")
        context['enderecos'] = enderecos
        return context
    
class ClientePerfilViewEditarNome(LogedMixin, LojaMixin, BaseContextMixin, TemplateView, FormView):
    template_name = "clienteperfil_editar_nome.html"
    form_class = ClienteEditarNome
    success_url = reverse_lazy("lojaapp:clienteperfil")

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
                next_url = reverse(f"{reverse_lazy('lojaapp:clienteperfil')}?perfil=Endereco")
            return redirect(next_url)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    return HttpResponse("Invalid request.")

class deletarEnderecoView(LojaMixin, View):
    def get(self,request,*arg,**kwargs):
        endereco_id = self.kwargs['endereco_id']
        Endereco.objects.filter(id=endereco_id).delete()

        return redirect(f"{reverse_lazy('lojaapp:clienteperfil')}?perfil=Endereco")

class PesquisarView(BaseContextMixin, TemplateView):
    template_name = "pesquisar.html"

    # def preprocessar_precos(self, produtos):
    #     for produto in produtos:
    #         precoCaixa = round((produto.preco_unitario_bruto * produto.fechamento_embalagem), 2)
    #         venda_parts_caixa = str(precoCaixa).split('.')
    #         venda_parts = str(produto.preco_unitario_bruto).split('.')
    #         produto.integer_part_uni = venda_parts[0]
    #         produto.decimal_part_uni = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #         produto.integer_part_caixa = venda_parts_caixa[0]
    #         produto.decimal_part_caixa = venda_parts_caixa[1] if len(venda_parts_caixa) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #     return produtos

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
        resultadoList = preprocessar_precos(resultado)

        resultadoPag = Paginator(resultadoList, 20)
        page_number = self.request.GET.get('page')

        context["resultado"] = resultadoPag.get_page(page_number)
        return context

class CategoriaView(LojaMixin, BaseContextMixin, TemplateView):
    template_name = "categoria.html"

    # def preprocessar_precos(self, produtos):
    #     for produto in produtos:
    #         precoCaixa = round((produto.preco_unitario_bruto * produto.fechamento_embalagem), 2)
    #         venda_parts_caixa = str(precoCaixa).split('.')
    #         venda_parts = str(produto.preco_unitario_bruto).split('.')
    #         produto.integer_part_uni = venda_parts[0]
    #         produto.decimal_part_uni = venda_parts[1] if len(venda_parts) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #         produto.integer_part_caixa = venda_parts_caixa[0]
    #         produto.decimal_part_caixa = venda_parts_caixa[1] if len(venda_parts_caixa) > 1 else '00'  # Adiciona '00' se não houver parte decimal
    #     return produtos

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
        produto_list = preprocessar_precos(all_produtos)
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
            'PedidosProntaRetirada' : Pedido_order.objects.filter(pedido_status="Pedido Pronta Retirada").order_by("-id"),
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
    # if request.method == 'POST':
    #     pedido_id = "52"
    #     pedido = Pedido_order.objects.get(id=pedido_id)

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

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

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

## Produto
class ProdutoListCreateView(generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [HasAPIKey]

    def perform_create(self, serializer):
        produto = serializer.save()  # Save the initial model instance
        
        # Get the uploaded image
        image_field = produto.image  # Assuming the image field is named 'image'
        
        if image_field:
            temp_file_path = image_field.path  # Get the file path

            # Converte pra webp
            file, ext = os.path.splitext(temp_file_path) 
            image = Image.open(temp_file_path).convert("RGB")
            new_path = f"{file}.webp"
            image.save(new_path, "webp")

            # Remove o original
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
                    categoria_id = Categoria.objects.get(titulo=data["Categoria"][str(i)])
                    img = "produtos/" + data["codigo"][str(i)] + ".webp"
                    Produto.objects.create(codigo=data["codigo"][str(i)],descricao=data["descricao"][str(i)],codigo_GTIN=data["codigo_GTIN"][str(i)],
                                           preco_unitario_bruto=data["preco_unitario_bruto"][str(i)],desconto_dinheiro=data["desconto_dinheiro"][str(i)],
                                           desconto_retira=data["desconto_retira"][str(i)],unidade=data["unidade"][str(i)],fechamento_embalagem=data["fechamento_embalagem"][str(i)],
                                           em_estoque=data["em_estoque"][str(i)],slug=data["slug"][str(i)],Categoria=categoria_id,titulo=data["titulo"][str(i)],image=img,)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON"}, status=400)
            
            return Response({"message": "JSON Upload Complete"}) #, "data_len": len(data["ACENAN"])})

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
                        categoria_id = Categoria.objects.get(titulo=data["Categoria"][str(i)])
                        
                        API_URL_PRODUTO = "http://127.0.0.1:8000/api_produtos/" + str(prod.codigo) + "/"
                        # API_URL_PRODUTO = "https://vendashg.pythonanywhere.com/api_produtos/" + str(prod.codigo) + "/"

                        headers = {
                            "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG,
                            # "Authorization": "Api-Key " + settings.TESTKEY_API_CASAHG_PYTHONANYWHERE,
                        }

                        update_data = {
                            "descricao": data["descricao"][str(i)],
                            "codigo_GTIN": data["codigo_GTIN"][str(i)],
                            "preco_unitario_bruto": data["preco_unitario_bruto"][str(i)],
                            "desconto_dinheiro": data["desconto_dinheiro"][str(i)],
                            "desconto_retira": data["desconto_retira"][str(i)],
                            "unidade": data["unidade"][str(i)],
                            "fechamento_embalagem": data["fechamento_embalagem"][str(i)],
                            "em_estoque": data["em_estoque"][str(i)],
                            "slug": data["slug"][str(i)],
                            "Categoria": categoria_id.id,
                            "titulo": data["titulo"][str(i)]
                        }

                        response = requests.patch(API_URL_PRODUTO, data=update_data, headers=headers)

                    except Produto.DoesNotExist:
                        categoria_id = Categoria.objects.get(titulo=data["Categoria"][str(i)])
                        img = "produtos/" + data["codigo"][str(i)] + ".webp"
                        Produto.objects.create(codigo=data["codigo"][str(i)],descricao=data["descricao"][str(i)],codigo_GTIN=data["codigo_GTIN"][str(i)],
                                            preco_unitario_bruto=data["preco_unitario_bruto"][str(i)],desconto_dinheiro=data["desconto_dinheiro"][str(i)],
                                            desconto_retira=data["desconto_retira"][str(i)],unidade=data["unidade"][str(i)],fechamento_embalagem=data["fechamento_embalagem"][str(i)],
                                            em_estoque=data["em_estoque"][str(i)],slug=data["slug"][str(i)],Categoria=categoria_id,titulo=data["titulo"][str(i)],image=img,)
                        
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
            os.remove(temp_file_path)
            
            file_url = os.path.join(settings.MEDIA_URL, "produtos", os.path.basename(converted_file_path))
            return JsonResponse({"message": "Upload complete", "file_url": file_url})

        return JsonResponse({"message": "Chunk received", "chunk_index": chunk_index})
    
## Fotos Produto
class FotosProdutoListCreateView(generics.ListCreateAPIView):
    queryset = FotosProduto.objects.all()
    serializer_class = FotosProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [HasAPIKey]

class FotosProdutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FotosProduto.objects.all()
    serializer_class = FotosProdutoSerializer
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [HasAPIKey]

## Pedido Order
class PedidoOrderListCreateView(generics.ListCreateAPIView):
    queryset = Pedido_order.objects.prefetch_related("pedidoProduto")
    serializer_class = PedidoOrderSerializer

    permission_classes = [HasAPIKey]

class PedidoOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido_order.objects.prefetch_related("pedidoProduto")
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
    queryset = Pedido_Produto.objects.all()
    serializer_class = PedidoProdutoSerializer

    permission_classes = [HasAPIKey]

class PedidoProdutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido_Produto.objects.all()
    serializer_class = PedidoProdutoSerializer

    permission_classes = [HasAPIKey]

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Verifica que o pedido online ta pago
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

# Formata o valor do preço dos produtos para mostrar de forma mais interessante no site
def preprocessar_precos(produtos):
        for produto in produtos:
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

        return produtos

# Funções de email
## Email enviado ao cliente ao criar sua conta
def EmailClienteRegistrado(_cliente):
    assunto = "Boas-vindas à CasaHG"
    text_content = "Obrigado por se cadastrar!"
    html_content = render_to_string(
                        "emails/emailClienteRegistrado.html",
                        context={
                            "cliente": _cliente,
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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
                            "urlDetalhePedido": "https://vendashg.pythonanywhere.com/perfil/pedido-" + str(_pedido.id),
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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
                            "urlDetalhePedido": "https://vendashg.pythonanywhere.com/perfil/pedido-" + str(_pedido.id),
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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
                            "urlDetalhePedido": "https://vendashg.pythonanywhere.com/perfil/pedido-" + str(_pedido.id),
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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
                            "urlDetalhePedido": "https://vendashg.pythonanywhere.com/perfil/pedido-" + str(_pedido.id),
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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
                            "urlDetalhePedido": "https://vendashg.pythonanywhere.com/perfil/pedido-" + str(_pedido.id),
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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
                            "urlDetalhePedido": "https://vendashg.pythonanywhere.com/perfil/pedido-" + str(_pedido.id),
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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
    #                         "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
    #                     },
    #                 )
    
    assunto = f"Pedido da CasaHG #{_pedido.id}"
    text_content = f"Pedido #{_pedido.id} realizado"
    html_content = render_to_string(
                        "emails/emailPedidoRealizado.html",
                        context={
                            "pedido": _pedido,
                            "urlDetalhePedido": "https://vendashg.pythonanywhere.com/perfil/pedido-" + str(_pedido.id),
                            "logo": "https://vendashg.pythonanywhere.com" + Empresa.objects.get(titulo="Casa HG").image.url,
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