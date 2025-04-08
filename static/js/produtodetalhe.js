const imgButtons = document.querySelectorAll(".imgWrapper > button");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > button > img");
// const imgMain = document.getElementById("mainImg");
const imgMain = document.querySelectorAll(".mainImg");

const quantidadeValor = document.querySelectorAll(".quantValue");
const quantidadeCaixas = document.querySelectorAll(".quantidade_total_caixas");
const custoCaixas = document.querySelectorAll(".custo_total_caixas");
const quantidadeCaixasConst = quantidadeCaixas[0].textContent.replace(",", ".");
const custoCaixasConst = custoCaixas[0].textContent.replace(",", ".");

function takeUnit() {
    if (parseInt(quantidadeValor[1].value) > 1) {
        quant = parseInt(quantidadeValor[1].value) - 1;

        quantidadeValor.forEach(qv => {
            qv.value = quant;
        });
        
        inputUnit(quant)
    }
}

function addUnit() {
    quant = parseInt(quantidadeValor[1].value) + 1;

    quantidadeValor.forEach(qv => {
        qv.value = quant;
    });

    inputUnit(quant)
}

function inputUnit(quant) {
    if (quantidadeCaixas[0] || quantidadeCaixas[1]) {
        quantidadeCaixas.forEach(qc => {
            qc.textContent = ((parseFloat(quantidadeCaixasConst) * quant).toFixed(2)).replace(".", ",");
        });
    }
    custoCaixas.forEach(cc => {
        cc.textContent = ((parseFloat(custoCaixasConst) * quant).toFixed(2)).replace(".", ",");
    });
}

imgButtons.forEach(e => {
    e.addEventListener("click", function(event) {
        imgMain.forEach(e => {
            e.src = event.target.src;
        });        

        imgButtonsImgs.forEach(t => {
            t.style.borderBottom = "none";
        })

        event.target.style.borderBottom = "5px solid #ff9900";
    });
});


const indicUsoButton = document.querySelector(".indicUsoButton");
const indicUsowindow = document.querySelector(".indicUsoWindow");
const indicUsoJanelaClose = document.querySelector(".indicUsoJanelaClose");
const variacaoFacesButton = document.querySelector(".variacaoFacesButton");
const variacaoFacesWindow = document.querySelector(".variacaoFacesWindow");
const variacaoFacesJanelaClose = document.querySelector(".variacaoFacesJanelaClose");

indicUsoButton.addEventListener("click", () => {
    if (indicUsowindow.style.display === "none") {
        indicUsowindow.style.display = "block";
    }
    else {
        indicUsowindow.style.display = "none";
    }

    if (variacaoFacesWindow.style.display === "block") {
        variacaoFacesWindow.style.display = "none";
    }
});

indicUsoJanelaClose.addEventListener("click", () => {
    if (indicUsowindow.style.display === "none") {
        indicUsowindow.style.display = "block";
    }
    else {
        indicUsowindow.style.display = "none";
    }
});

variacaoFacesButton.addEventListener("click", () => {
    if (variacaoFacesWindow.style.display === "none") {
        variacaoFacesWindow.style.display = "block";
    }
    else {
        variacaoFacesWindow.style.display = "none";
    }

    if (indicUsowindow.style.display === "block") {
        indicUsowindow.style.display = "none";
    }
});

variacaoFacesJanelaClose.addEventListener("click", () => {
    if (variacaoFacesWindow.style.display === "none") {
        variacaoFacesWindow.style.display = "block";
    }
    else {
        variacaoFacesWindow.style.display = "none";
    }
});