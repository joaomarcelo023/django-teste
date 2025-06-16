from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "lojaapp"

urlpatterns = [
    # Base
    path("",HomeView.as_view(),name="home"),
    path("sobre/",SobreView.as_view(),name="sobre"),
    path("contato/",ContatoView.as_view(),name="contato"),

    # Produtos
    path("pesquisar/", PesquisarView.as_view(), name="pesquisar"),
    path("categoria/<slug:slug>/",CategoriaView.as_view(),name="categoria"),
    path("produtos/<slug:slug>/",ProdutosDetalheView.as_view(),name="produtodetalhe"),

    # Compra
    path("addcarro2-<int:prod_id>/",AddCarroView2.as_view(),name="addcarro2"),
    path("addcarro-<int:prod_id>/", AddCarroView.as_view(), name="addcarro"),
    path("addcarroquant/", AddCarroQuantView.as_view(), name="addcarroquant"),
    path("meu-carro/",MeuCarroView.as_view(),name="meucarro"),
    path("manipular-carro/<int:cp_id>/",ManipularCarroView.as_view(),name="manipularcarro"),
    path("limpar-carro/",LimparCarroView.as_view(),name="limparcarro"),
    path("forma-de-entrega/", FormaDeEntregaView.as_view(), name="formadeentrega"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("pedido-cofirmado/", PedidoConfirmadoView.as_view(), name="pedidoconfirmado"),
    path("pedido-erro/", PedidoErroView.as_view(), name="pedidoerro"),

    # Login
    path("registrar/", ClienteRegistrarView.as_view(), name="clienteregistrar"),
    path("logout/", ClienteLogoutView.as_view(), name="clientelogout"),
    path("entrar/", ClienteEntrarView.as_view(), name="clienteentrar"),
    path("clientereverificaconta/", ClienteReverificaContaView.as_view(), name="clientereverificaconta"),
    path('verifica_user/<str:uidb64>/<str:token>/', verifica_user, name="verifica_user"),

    # Perfil cliente
    path("perfil/", ClientePerfilView.as_view(), name="clienteperfil"),
    path("perfil/pedido-<int:pk>", ClientePedidoDetalheView.as_view(), name="clientepedidodetalhe"),
    path("cadastrar-endereco/",CadastrarEnderecoView.as_view(),name="cadastrarendereco"),
    path("editar-endereco/<int:endereco_id>/", ClientePerfilViewEditarEndereco.as_view(), name="editarendereco"),
    path("deletar-endereco/<int:endereco_id>/", deletarEnderecoView.as_view(), name='deletarendereco'),
    path("perfil/editar-nome", ClientePerfilViewEditarNome.as_view(), name="clienteperfil_editar_nome"),
    path("perfil/editar-email", ClientePerfilViewEditarEmail.as_view(), name="clienteperfil_editar_email"),
    path("perfil/editar-cpf", ClientePerfilViewEditarCPF.as_view(), name="clienteperfil_editar_cpf"),
    path("perfil/editar-telefone", ClientePerfilViewEditarTelefone.as_view(), name="clienteperfil_editar_telefone"),
    path("perfil/alterar-senha", ClientePerfilViewAlterarSenha.as_view(), name="clienteperfil_alterar_senha"),
    path("deletar-perfil/", DeletarPerfilView.as_view(), name="deletar_perfil"),

    # Admin
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-pedido-<int:pk>/", AdminPedidoView.as_view(), name="adminpedido"),
    path("admin-todos-pedido/", AdminTodosPedidoView.as_view(), name="admintodospedido"),
    path("admin-pedido-mudar/<int:pk>/", AdminPedidoMudarView.as_view(), name="adminpedidomudar"),
    path("admin-todos-produto/", AdminTodosProdutoView.as_view(), name="admintodosprodutos"),
    path("admin-produto/<slug:slug>/", AdminProdutoView.as_view(), name="adminprodutodetalhe"),
    path('admin-categoria/', AdminCategoriasView.as_view(), name="admincategoria"),
    path('admin-pesquisar/', PesquisarAdminView.as_view(), name="adminpesquisar"),
    path('admin-logs/', AdminLogsView.as_view(), name="adminlogs"),
    path('admin-banners/', AdminBannersView.as_view(), name="adminbanners"),

    # POST
    path('endereco_cadastrar/', endereco_cadastrar, name='endereco_cadastrar'),
    path('pedido_carro_endereco/', pedido_carro_endereco, name='pedido_carro_endereco'),
    path('pedido_carro_pagamento/', pedido_carro_pagamento, name='pedido_carro_pagamento'),
    path('consultar_checkout_pag/', consultar_checkout_pag, name='consultar_checkout_pag'),
    path('cancelar_checkout_pag/', cancelar_checkout_pag, name='cancelar_checkout_pag'),
    path('download_order/', download_order, name='download_order'),
    path('atualiza_produto/', atualiza_produto, name='atualiza_produto'),
    path('atualiza_ficha_produto/', atualiza_ficha_produto, name='atualiza_ficha_produto'),
    path('ChecaFotosProdutos/', ChecaFotosProdutos, name='ChecaFotosProdutos'),
    path('ResetaFotosProdutos/', ResetaFotosProdutos, name='ResetaFotosProdutos'),
    path('upload_imagem_extra_produtos/', upload_imagem_extra_produtos, name='upload_imagem_extra_produtos'),
    path('delete_imagem_extra_produtos/', delete_imagem_extra_produtos, name='delete_imagem_extra_produtos'),
    path('notifica_pag_pedido/', notifica_pag_pedido, name='notifica_pag_pedido'),
    path('notifica_pagamento_pag_pedido/', notifica_pagamento_pag_pedido, name='notifica_pagamento_pag_pedido'),
    path('banner_status/', banner_status, name='banner_status'),
    path('banner_create/', banner_create, name='banner_create'),
    path('banner_deletar/', banner_deletar, name='banner_deletar'),
    path('banner_position/', banner_position, name='banner_position'),

    # Tests
    path('test_atualizacao_pag/', test_atualizacao_pag, name='test_atualizacao_pag'),
    
    path('testPOST/', testPOST, name='testPOST'),

    # API
    ## Teste
    path('api_test/', TestListCreateView.as_view(), name='test_list'),
    path('api_test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    
    ## Categoria
    path('api_categorias/', CategoriaListView.as_view(), name='categorias_list'),
    path('api_categorias/<str:slug>/', CategoriaDetailView.as_view(), name='categorias_detail'),

    ## Produto
    path('api_produtos/', ProdutoListCreateView.as_view(), name='produto_list'),
    path('api_produtos/<str:slug>/', ProdutoDetailView.as_view(), name='produto_detail'),
    path('chunked_json_upload/', ChunkedProdutoJsonUploadView.as_view(), name='chunked_produto_json_upload'),
    path('chunked_json_update/', ChunkedProdutoJsonUpdateView.as_view(), name='chunked_produto_json_update'),
    path('chunked_estoque_json_upload/', ChunkedEstoqueJsonUploadView.as_view(), name='chunked_estoque_json_upload'),
    path('chunked_piso_ficha_tec_json_upload/', ChunkedProdutoPisoFichaTecJsonUploadView.as_view(), name='chunked_piso_ficha_tec_json_upload'),    
    path('chunked_img_upload/', ChunkedProdutoImgUploadView.as_view(), name='chunked_produto_img_upload'),
    path('produto_stats/', ProdutoStatsView.as_view(), name='produto_stats'),

    ## Fotos Produto
    path('api_fotos_produtos/', FotosProdutoListCreateView.as_view(), name='fotos_produto_list'),
    path('api_fotos_produtos/<int:pk>/', FotosProdutoDetailView.as_view(), name='fotos_produto_detail'),
    path('api_fotos_produtos_upload/', FotosProdutoUploadView.as_view(), name='fotos_produto_list_upload'),

    ## Pedido Order
    path('api_pedido_order/', PedidoOrderListCreateView.as_view(), name='pedido_order_list'),
    path('api_pedido_order/<int:pk>/', PedidoOrderDetailView.as_view(), name='pedido_order_detail'),

    ## Pedido Produto
    path('api_pedido_produto/', PedidoProdutoListCreateView.as_view(), name='pedido_produto_list'),
    path('api_pedido_produto/<int:pk>/', PedidoProdutoDetailView.as_view(), name='pedido_produto_detail'),
    
]