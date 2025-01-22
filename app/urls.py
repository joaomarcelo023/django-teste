from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "lojaapp"

urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    path("sobre/",SobreView.as_view(),name="sobre"),
    path("contato/",ContatoView.as_view(),name="contato"),

    path("pesquisar/", PesquisarView.as_view(), name="pesquisar"),
    path("categoria/<slug:slug>/",CategoriaView.as_view(),name="categoria"),
    path("todos-produtos/",TodosProdutosView.as_view(),name="Todosprodutos"),
    path("produtos/<slug:slug>/",ProdutosDetalheView.as_view(),name="produtodetalhe"),

    path("addcarro2-<int:prod_id>/",AddCarroView2.as_view(),name="addcarro"),
    path("addcarro-<int:prod_id>/", AddCarroView.as_view(), name="addcarro"),
    path("addcarroquant/", AddCarroQuantView.as_view(), name="addcarroquant"),
    path("meu-carro/",MeuCarroView.as_view(),name="meucarro"),
    path("manipular-carro/<int:cp_id>/",ManipularCarroView.as_view(),name="manipularcarro"),
    path("limpar-carro/",LimparCarroView.as_view(),name="limparcarro"),
    path("forma-de-entrega/", FormaDeEntregaView.as_view(), name="formadeentrega"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("pedido-cofirmado/", PedidoConfirmadoView.as_view(), name="pedidoconfirmado"),

    path("registrar/", ClienteRegistrarView.as_view(), name="clienteregistrar"),
    path("logout/", ClienteLogoutView.as_view(), name="clientelogout"),
    path("entrar/", ClienteEntrarView.as_view(), name="clienteentrar"),

    path("perfil/", ClientePerfilView.as_view(), name="clienteperfil"),
    path("perfil/pedido-<int:pk>", ClientePedidoDetalheView.as_view(), name="clientepedidodetalhe"),
    path("cadastrar-endereco/",CadastrarEnderecoView.as_view(),name="cadastrarendereco"),
    path('deletar-endereco/<int:endereco_id>/', deletarEnderecoView.as_view(), name='deletarendereco'),

    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-pedido-<int:pk>/", AdminPedidoView.as_view(), name="adminpedido"),
    path("admin-todos-pedido/", AdminTodosPedidoView.as_view(), name="admintodospedido"),
    path("admin-pedido-mudar/<int:pk>/", AdminPedidoMudarView.as_view(), name="adminpedidomudar"),
    path('admin-pesquisar/', PesquisarAdminView.as_view(), name="adminpesquisar"),

    path('endereco_cadastrar/', endereco_cadastrar, name='endereco_cadastrar'),
    path('pedido_carro_endereco/', pedido_carro_endereco, name='pedido_carro_endereco'),
    path('pedido_carro_pagamento/', pedido_carro_pagamento, name='pedido_carro_pagamento'),
    path('consultar_checkout_pag/', consultar_checkout_pag, name='consultar_checkout_pag'),
    path('cancelar_checkout_pag/', cancelar_checkout_pag, name='cancelar_checkout_pag'),

    path('test_atualizacao_pag/', test_atualizacao_pag, name='test_atualizacao_pag'),
    
    path('testPOST/', testPOST, name='testPOST'),
    
]