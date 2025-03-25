let pedidoType = new URLSearchParams(window.location.search).get('categoria');

if (pedidoType === null){
    pedidoType = "Todas";
}