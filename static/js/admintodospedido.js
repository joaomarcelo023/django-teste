const tabelas = document.querySelectorAll('.tabela')
let pedidoType = new URLSearchParams(window.location.search).get('pedidos');
if (pedidoType === null){
    pedidoType = "Todos";
}

tabelas.forEach(e => {
    if ((e.id === pedidoType) || (pedidoType === "Todos")) {
        e.style.display = "block"
    }
});