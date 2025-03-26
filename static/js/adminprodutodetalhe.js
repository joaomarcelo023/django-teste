const imgButtons = document.querySelectorAll(".imgWrapper > button");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > button > img");
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

// Graficos
const codProd = document.getElementById("codigo_produto").getAttribute("data-codigo");
const GraficoVendas = document.getElementById('graficoVendas');
const grafico_vendas_data = JSON.parse(document.getElementById('grafico_vendas_data').textContent);
const GraficoVisuli = document.getElementById('graficoVisuli');
const grafico_visuli_data = JSON.parse(document.getElementById('grafico_visuli_data').textContent);
const GraficoVendasVisuli = document.getElementById('graficoVendasVisuli');

let yVendas = [];
for (let n of Object.keys(grafico_vendas_data)) {
    yVendas.push(grafico_vendas_data[n]?.[codProd] || 0);
}
let yVisuli = [];
for (let n of Object.keys(grafico_visuli_data)) {
    yVisuli.push(grafico_visuli_data[n]?.[codProd] || 0);
}

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