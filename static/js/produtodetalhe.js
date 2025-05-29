// Esc sai das janelas popup
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' || event.keyCode === 27 || event.which === 27) {  // Prefer this (standard)
        if (indicUsowindow){
            if (indicUsowindow.style.display === "block") {
                indicUsowindow.style.display = "none";
            }
        }

        if (variacaoFacesWindow){
            if (variacaoFacesWindow.style.display === "block") {
                variacaoFacesWindow.style.display = "none";
            }
        }

        if (moreImgsWindow){
            if (moreImgsWindow.style.display === "block") {
                moreImgsWindow.style.display = "none";
            }
        }
    }
});

// Controle de quantidade
const quantidadeValor = document.querySelectorAll(".quantValue");
const quantidadeCaixas = document.querySelectorAll(".quantidade_total_caixas");
// const quantidadeCaixasConst = quantidadeCaixas[0].textContent.replace(",", ".");
const quantidadeCaixasConst = document.getElementById("quantidadePorCaixa").getAttribute("data-quantidadePorCaixa").replace(",", ".");
const custoCaixas = document.querySelectorAll(".custo_total_caixas");
const custoCaixasConst = custoCaixas[0].textContent.replace(",", ".");

function takeUnit() {
    if (parseInt(quantidadeValor[1].value) > parseInt(quantidadeValor[1].min)) {
        quant = parseInt(quantidadeValor[1].value) - 1;

        quantidadeValor.forEach(qv => {
            qv.value = quant;
        });
        
        inputUnit(quant)
    }
}

function addUnit() {
    // if (parseInt(quantidadeValor[1].value) < parseInt(quantidadeValor[1].max)) {
    if (parseFloat(quantidadeCaixas[0].textContent.replace(",", ".")) < (parseFloat(quantidadeValor[1].max.replace(",", ".")))) {
        quant = parseInt(quantidadeValor[1].value) + 1;

        quantidadeValor.forEach(qv => {
            qv.value = quant;
        });

        inputUnit(quant)
    }
}

function inputUnit(quant) {
    if (!Number.isInteger(Number(quant))) {
        quantidadeValor.forEach(qv => {
            qv.value = Math.round(quant);
        });

        inputUnit(Math.round(quant))
    }
    else {
        // if (quant >= parseInt(quantidadeValor[0].min) && quant <= parseInt(quantidadeValor[0].max)){
        if (quant >= parseInt(quantidadeValor[0].min) && (parseFloat(quantidadeCaixasConst) * quant).toFixed(2) <= (parseFloat(quantidadeValor[1].max.replace(",", ".")))){
            if (quantidadeCaixas[0] || quantidadeCaixas[1]) {
                quantidadeCaixas.forEach(qc => {
                    qc.textContent = ((parseFloat(quantidadeCaixasConst) * quant).toFixed(2)).replace(".", ",");
                });
            }
            custoCaixas.forEach(cc => {
                cc.textContent = ((parseFloat(custoCaixasConst) * quant).toFixed(2)).replace(".", ",");
            });
        }
        else if (quant < parseInt(quantidadeValor[0].min)) {
            quantidadeValor.forEach(qv => {
                qv.value = 1;
            });

            inputUnit(1)
        }
        else if ((parseFloat(quantidadeCaixasConst) * quant).toFixed(2) > (parseFloat(quantidadeValor[1].max.replace(",", ".")))) {
            quantidadeValor.forEach(qv => {
                qv.value = parseFloat(quantidadeValor[0].max.replace(",", ".")) / parseFloat(quantidadeCaixasConst);
            });

            inputUnit(parseFloat(quantidadeValor[0].max.replace(",", ".")) / parseFloat(quantidadeCaixasConst))
        }
    }
}

// Controle da imagem
//// Mudança da imagem
const imgButtons = document.querySelectorAll(".imgWrapper > button");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > button > img");
const imgButtonsImgsList = [...document.querySelectorAll(".imgWrapper > button > img")];
const imgMain = document.querySelectorAll(".mainImg");

const imgButtonsImgsLim = (imgButtonsImgs.length / 2);
const arrowLeftImgs = document.querySelector(".arrow-left-foto");
const arrowRightImgs = document.querySelector(".arrow-right-foto");
var currentImg = 0;

if (arrowLeftImgs) {
    arrowLeftImgs.addEventListener("click", () => {
        currentImg = currentImg - 1;
        if (currentImg < 0) {
            currentImg = imgButtonsImgsLim - 1;
        }

        imgMain.forEach(im => {
            im.src = imgButtonsImgsList[currentImg].src;
        });

        
        imgButtonsImgs.forEach(t => {
            t.style.borderBottom = "none";
        });
        imgButtonsImgsList[(imgButtonsImgsLim + currentImg)].style.borderBottom = "5px solid #ff9900";
    });
}

if (arrowRightImgs){
    arrowRightImgs.addEventListener("click", () => {
        currentImg = currentImg + 1;
        if (currentImg >= imgButtonsImgsLim) {
            currentImg = 0;
        }

        imgMain.forEach(im => {
            im.src = imgButtonsImgsList[currentImg].src;
        });

        
        imgButtonsImgs.forEach(t => {
            t.style.borderBottom = "none";
        });
        imgButtonsImgsList[(imgButtonsImgsLim + currentImg)].style.borderBottom = "5px solid #ff9900";
    });
}

imgButtons.forEach(e => {
    e.addEventListener("click", function(event) {
        if (imgButtonsImgsList.includes(event.target)) {
            imgMain.forEach(im => {
                im.src = event.target.src;
            });
    
            imgButtonsImgs.forEach(t => {
                t.style.borderBottom = "none";
            });
    
            event.target.style.borderBottom = "5px solid #ff9900";
        }

        if (imgButtonsImgsList.indexOf(event.target) >= imgButtonsImgsLim) {
            currentImg = imgButtonsImgsList.indexOf(event.target) - imgButtonsImgsLim;
        } else {
            currentImg = imgButtonsImgsList.indexOf(event.target);
        }
        
    });
});

//// Tela das imagens extra que não cabem na pagina
const moreImgsButton = document.querySelectorAll(".imgWrapper > .moreImgsButton");
const moreImgsWindow = document.querySelector(".moreImgsWindow");
const moreImgsJanelaClose = document.querySelector(".moreImgsJanelaClose");

if (moreImgsButton) {
    moreImgsButton.forEach(mib => {
        mib.addEventListener("click", () => {
            if (moreImgsWindow.style.display === "none") {
                moreImgsWindow.style.display = "block";
            }
            else {
                moreImgsWindow.style.display = "none";
            }
        });
    });

    if (moreImgsJanelaClose) {
        moreImgsJanelaClose.addEventListener("click", () => {
            if (moreImgsWindow.style.display === "none") {
                moreImgsWindow.style.display = "block";
            }
            else {
                moreImgsWindow.style.display = "none";
            }
        });
    }
}

const imgButtons_moreImgs = document.querySelectorAll(".imgWrapper_moreImgs > button");
const imgButtonsImgs_moreImgs = document.querySelectorAll(".imgWrapper_moreImgs > button > img");
const imgButtonsImgsList_moreImgs = [...document.querySelectorAll(".imgWrapper_moreImgs > button > img")];
const imgMain_moreImgs = document.querySelectorAll(".mainImg_moreImgs");

imgButtons_moreImgs.forEach(e => {
    e.addEventListener("click", function(event) {
        if (imgButtonsImgsList_moreImgs.includes(event.target)) {
            imgMain_moreImgs.forEach(im => {
                im.src = event.target.src;
            });
    
            imgButtonsImgs_moreImgs.forEach(t => {
                t.style.borderBottom = "none";
            });
    
            event.target.style.borderBottom = "5px solid #ff9900";
        }
        
    });
});

// Pop-up windows
const indicUsoButton = document.querySelector(".indicUsoButton");
const indicUsowindow = document.querySelector(".indicUsoWindow");
const indicUsoJanelaClose = document.querySelector(".indicUsoJanelaClose");
const variacaoFacesButton = document.querySelector(".variacaoFacesButton");
const variacaoFacesWindow = document.querySelector(".variacaoFacesWindow");
const variacaoFacesJanelaClose = document.querySelector(".variacaoFacesJanelaClose");

if (indicUsoButton) {
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
}

if (variacaoFacesButton) {
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
}

// Tamanho do produto_pequenos e moreImgsWindow
const mobile = document.querySelector(".pequeno");
const divPreco = document.querySelectorAll(".divPreco");
const imgCol_moreImgs_main = document.querySelector(".imgCol_moreImgs_main");
const imgCol_moreImgs_sub = document.querySelector(".imgCol_moreImgs_sub");

if (window.getComputedStyle(mobile).display === "none") {
    // produto_pequenos
    divPreco.forEach(div => {
        div.classList.remove("col-8");
        div.classList.add("col-9");
    });

    // moreImgsWindow
    imgCol_moreImgs_main.classList.remove("col-12");
    imgCol_moreImgs_main.classList.add("col-5");

    imgCol_moreImgs_sub.classList.remove("col-12");
    imgCol_moreImgs_sub.classList.add("col-7");
} else {
    // produto_pequenos
    divPreco.forEach(div => {
        div.classList.add("col-8");
        div.classList.remove("col-9");
    });

    // moreImgsWindow
    imgCol_moreImgs_main.classList.remove("col-5");
    imgCol_moreImgs_main.classList.add("col-12");

    imgCol_moreImgs_sub.classList.remove("col-7");
    imgCol_moreImgs_sub.classList.add("col-12");
}