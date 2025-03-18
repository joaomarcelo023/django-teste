$(document).ready(function() {
    $('.phone-number').inputmask({
        mask: "(99) 99999-9999",    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true       // Optional: show mask on focus only
    });

    $('.cpf-cnpj').inputmask({
        mask: ["99999999999", "99999999999999"],    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true       // Optional: show mask on focus only
    });
});

const termosCondBtn = document.getElementById("termos_condicoes_btn");
const termosCondJanela = document.querySelector(".termos_condicoes_janela");
const termosCondJanelaClose = document.querySelector(".termos_condicoes_janela_close");
const termosCondCheck = document.getElementById("termos_condicoes");

termosCondCheck.addEventListener("click", () => {
    if (termosCondCheck.checked) {
        document.getElementById("btnComprar").disabled = false;
    }
    else {
        document.getElementById("btnComprar").disabled = true;
    }
});

termosCondBtn.addEventListener("click", () => {
    if (termosCondJanela.style.display === "none") {
        termosCondJanela.style.display = "block";
    }
    else {
        termosCondJanela.style.display = "none";
    }
});

termosCondJanelaClose.addEventListener("click", () => {
    if (termosCondJanela.style.display === "none") {
        termosCondJanela.style.display = "block";
    }
    else {
        termosCondJanela.style.display = "none";
    }
});