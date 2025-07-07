// let telNewKeys = "";
// let telOGKeys = "";
// let tel = "";
// let telPos = 0;
// let telComp = false;

$(document).ready(function() {
    $('.phone-number').inputmask({
        mask: "(99) 99999-9999" + "9{0,}",    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true,      // Optional: show mask on focus only
        greedy: false
        // oncomplete: function() {
        //     telComp = true;
        //     telOGKeys = this.value.replace("(", "").replace(")", "").replace(" ", "").replace("-", "");
        //     tel = telOGKeys;
        // }
    // }).on('keydown', function(e) {
    //     if (telComp) {
    //         console.log(e.key);
    //         if ((e.key === "Backspace") || (e.key === "Delete")) {
    //             telNewKeys = "";
    //             telPos = 0;
    //             telComp = false;
    //         }
    //         else {
    //             telNewKeys += e.key;
    //             telPos += 1;

    //             if (tel[0] === "5") {
    //                 tel = tel.slice(1) + telNewKeys[telPos - 1];
    //             }

    //             this.value = tel;
    //         }
    //     }
    }).on('keyup', function(e) {
        if (this.value.length > 15){
            $(this).css({
                'border': '2px solid red',
                'background-color': '#ffe6e6'
            });

            document.querySelector(".phone_number_possible_error").style.display = "block";
        }
        else {
            $(this).css({
                'border': '',
                'background-color': ''
            });

            document.querySelector(".phone_number_possible_error").style.display = "none";
        }
    });

    $('.cpf-cnpj').inputmask({
        mask: ["99999999999", "99999999999999"],    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true       // Optional: show mask on focus only
    });
});

if (document.querySelector(".phone-number").value.length > 15) {
    document.querySelector(".phone-number").style.border = "2px solid red";
    document.querySelector(".phone-number").style.backgroundColor = "#ffe6e6";
}
else {
    document.querySelector(".phone-number").style.border = "";
    document.querySelector(".phone-number").style.backgroundcolor = "";
}

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