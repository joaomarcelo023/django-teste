const quantidadeValor = document.getElementById("quantValue");
const imgButtons = document.querySelectorAll(".imgWrapper > button");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > button > img");
// const imgMain = document.getElementById("mainImg");
const imgMain = document.querySelectorAll(".mainImg");
const quantidadeCaixas = document.querySelector(".quantidade_total_caixas");
const custoCaixas = document.querySelector(".custo_total_caixas");
const quantidadeCaixasConst = quantidadeCaixas.textContent.replace(",", ".");
const custoCaixasConst = custoCaixas.textContent.replace(",", ".");

function takeUnit() {
    if (parseInt(quantidadeValor.value) > 1) {
        quant = parseInt(quantidadeValor.value) - 1;

        quantidadeValor.value = quant;
        
        if (quantidadeCaixas) {
            quantidadeCaixas.textContent = ((parseFloat(quantidadeCaixasConst) * quant).toFixed(2)).replace(".", ",");
        }
        custoCaixas.textContent = ((parseFloat(custoCaixasConst) * quant).toFixed(2)).replace(".", ",");
    }
}

function addUnit() {
    quant = parseInt(quantidadeValor.value) + 1;

    quantidadeValor.value = quant;

    if (quantidadeCaixas) {
        quantidadeCaixas.textContent = ((parseFloat(quantidadeCaixasConst) * quant).toFixed(2)).replace(".", ",");
    }
    custoCaixas.textContent = ((parseFloat(custoCaixasConst) * quant).toFixed(2)).replace(".", ",");
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