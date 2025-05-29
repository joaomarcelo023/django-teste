// Controle da imagem
//// Mudança da imagem
const imgButtons = document.querySelectorAll(".imgWrapper > .imgButton");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > .imgButton > img");
const imgButtonsImgsList = [...document.querySelectorAll(".imgWrapper > button > img")];
const imgMain = document.querySelectorAll(".mainImg");

const imgButtonsImgsLim = imgButtonsImgs.length;
const arrowLeftImgs = document.querySelector(".arrow-left-foto");
const arrowRightImgs = document.querySelector(".arrow-right-foto");
var currentImg = 0;

////// Muda a imagem com as setas
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
        
        imgButtonsImgsList[currentImg].style.borderBottom = "5px solid #ff9900";
    });
}

if (arrowRightImgs) {
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

        imgButtonsImgsList[currentImg].style.borderBottom = "5px solid #ff9900";
    });
}

////// Muda imagem com clique
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

        currentImg = imgButtonsImgsList.indexOf(event.target);
        
    });
});

//// Adiciona foto
const botao = document.getElementById('fotoExtraProdutoInputButton')
if (botao) {
    botao.addEventListener('click', function () {
        document.getElementById('fotoExtraProdutoInputFile').click();
    });
}

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

//// Esc sai das janelas popup
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' || event.keyCode === 27 || event.which === 27) {
        if (moreImgsWindow){
            if (moreImgsWindow.style.display === "block") {
                moreImgsWindow.style.display = "none";
            }
        }
    }
});

// Graficos
const codProd = document.getElementById("codigo_produto").getAttribute("data-codigo");
const GraficoVendas = document.getElementById('graficoVendas');
const grafico_vendas_data = JSON.parse(document.getElementById('grafico_vendas_data').textContent);
const GraficoVisuli = document.getElementById('graficoVisuli');
const grafico_visuli_data = JSON.parse(document.getElementById('grafico_visuli_data').textContent);
const GraficoVendasVisuli = document.getElementById('graficoVendasVisuli');
const mesesVendas = Object.keys(grafico_vendas_data).sort();
const mesesVisuli = Object.keys(grafico_visuli_data).sort();

let yVendas = [];
for (let n = 0; n < mesesVendas.length; n++) {
    let vendasInit = 0;
    if (n != 0){
       vendasInit = grafico_vendas_data[mesesVendas[n - 1]]?.[codProd] || 0;
    }
    let vendasFin = grafico_vendas_data[mesesVendas[n]]?.[codProd] || 0;

    yVendas.push(vendasFin - vendasInit);
}
// for (let n of Object.keys(grafico_vendas_data)) {
//     yVendas.push(grafico_vendas_data[n]?.[codProd] || 0);
// }
let yVisuli = [];
for (let n = 0; n < mesesVisuli.length; n++) {
    let visuliInit = 0;
    if (n !== 0){
       visuliInit = grafico_visuli_data[mesesVisuli[n - 1]]?.[codProd] || 0;
    }
    let visuliFin = grafico_visuli_data[mesesVisuli[n]]?.[codProd] || 0;

    yVisuli.push(visuliFin - visuliInit);
}
// for (let n of Object.keys(grafico_visuli_data)) {
//     yVisuli.push(grafico_visuli_data[n]?.[codProd] || 0);
// }

//// Vendas
var vendas = {
    x: Object.keys(grafico_vendas_data),
    y: yVendas,
    mode: 'lines+markers',
    type: 'scatter',
    line: {color: '#ff9900', shape: 'spline'},
    name: 'Vendas'
};

var data_vendas = [vendas];

var layout_vendas = {
    margin: { l: 36, r: 21, t: 21, b: 36 }
};

Plotly.newPlot(GraficoVendas, data_vendas, layout_vendas, {scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displaylogo: false});

//// Visualização
var visuli = {
    x: Object.keys(grafico_visuli_data),
    y: yVisuli,
    mode: 'lines+markers',
    type: 'scatter',
    line: {color: '#151635', shape: 'spline'},
    name: 'Visualizações'
};

var data_visuli = [visuli];

var layout_visuli = {
    margin: { l: 36, r: 21, t: 21, b: 36 }
};

Plotly.newPlot(GraficoVisuli, data_visuli, layout_visuli, {scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displaylogo: false});

var data = [vendas, visuli];

var layout = {
    title: { text: "Vendas x Visualizações" },
    margin: { l: 36, r: 21, t: 36, b: 36 }
};

Plotly.newPlot(GraficoVendasVisuli, data, layout, {scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displaylogo: false});