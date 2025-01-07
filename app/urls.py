#TODO-ALVAREZ: tela de entrega leva para a tela de escolher forma de pagamento, nessa tela terão 3 categoria
#   1° dinheiro em espécie (tentativa de chamar atenção pq é o melhor preço),
#   2° Pagar na loja (clique abre 3 de opções (PIX, débito e credito(credito abre opção de prazo 1x-12x))),
#   3° Pagamento online com logo da pagseguro (clique abre 3 opções (PIX, débito e crédito(credito abre opção de prazo 1x-12x))).

#TODO-ALVAREZ: tela de resumo com uma tabela não editável onde se encontram todos os preços e condições selecionadas,
#   para caso a forma de pagamento seja online, botão de pagar com a logo do pagseguro que já leva para o pagamento online,
#   para caso a forma de pagamento não seja online, botão de "criar pedido",
#   após o botão, criar uma instancia de pedido_order e um pedido_produtos,
#   com o status "pagamento pendente" para pagamento não online,
#   com o status "confirmando pagamento" para pagamento online.

#TODO-ALVAREZ: implementar pagamento pagseguro


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
    path("meu-carro/",MeuCarroView.as_view(),name="meucarro"),
    path("manipular-carro/<int:cp_id>/",ManipularCarroView.as_view(),name="manipularcarro"),
    path("limpar-carro/",LimparCarroView.as_view(),name="limparcarro"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("forma-de-entrega/", FormaDeEntregaView.as_view(), name="formadeentrega"),

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
    
    path('retorno/pagseguro/', include('pagseguro.urls')),

    path('endereco_cadastrar/', endereco_cadastrar, name='endereco_cadastrar'),
    path('pedido_carro_endereco/', pedido_carro_endereco, name='pedido_carro_endereco'),
    path('pedido_carro_pagamento/', pedido_carro_pagamento, name='pedido_carro_pagamento'),
    
    path('testPOST/', testPOST, name='testPOST'),
    
]