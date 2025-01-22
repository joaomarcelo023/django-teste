const quantidadeValor = document.getElementById("quantValue");
const imgButtons = document.querySelectorAll(".imgWrapper > button");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > button > img");
const imgMain = document.getElementById("mainImg");

function takeUnit() {
    if (parseInt(quantidadeValor.value) > 1) {
        quant = parseInt(quantidadeValor.value) - 1;

        quantidadeValor.value = quant;
    }
}

function addUnit() {
    quant = parseInt(quantidadeValor.value) + 1;

    quantidadeValor.value = quant;
}

imgButtons.forEach(e => {
    e.addEventListener("click", function(event) {
        imgMain.src = event.target.src;

        imgButtonsImgs.forEach(t => {
            t.style.borderBottom = "none";
        })

        event.target.style.borderBottom = "5px solid #ff9900";
    });
});