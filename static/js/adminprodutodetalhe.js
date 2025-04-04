const imgButtons = document.querySelectorAll(".imgWrapper > .imgButton");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > .imgButton > img");
const imgMain = document.querySelectorAll(".mainImg");

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

const botao = document.getElementById('fotoExtraProdutoInputButton')
if (botao) {
    botao.addEventListener('click', function () {
        document.getElementById('fotoExtraProdutoInputFile').click();
    });
}

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

// Vendas
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

// Visualização
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