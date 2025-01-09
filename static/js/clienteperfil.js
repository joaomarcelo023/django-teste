const caixas = document.querySelectorAll(".perfilCont");
const PC = document.querySelector('.grande');
let caixaVisu = new URLSearchParams(window.location.search).get('perfil');
if (caixaVisu === null){
    caixaVisu = "ClienteInfo";
}

caixas.forEach(e => {
    if ((e.id === caixaVisu) && (window.getComputedStyle(PC).display !== "none")){
        e.style.display = "flex";
    }
    else {
        e.style.display = "none";
    }
});