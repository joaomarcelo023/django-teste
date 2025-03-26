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
const grafico_vendas_data = document.getElementById('grafico_vendas_data').textContent;
const GraficoVisuli = document.getElementById('graficoVisuli');
const grafico_visuli_data = document.getElementById('grafico_visuli_data').textContent;

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
    line: {color: '#ff9900', shape: 'spline'}
};

var data_vendas = [vendas];

var layout_vendas = {
    xaxis: { title: 'Mês' },
    margin: { l: 21, r: 21, t: 21, b: 50 }
};

Plotly.newPlot(GraficoVendas, data_vendas, layout_vendas, {scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displaylogo: false});

// Visualização
var visuli = {
    x: Object.keys(grafico_visuli_data),
    y: yVisuli,
    mode: 'lines+markers',
    type: 'scatter',
    line: {color: '#ff9900', shape: 'spline'}
};

var data_visuli = [visuli];

var layout_visuli = {
    xaxis: { title: 'Mês' },
    margin: { l: 21, r: 21, t: 21, b: 50 }
};

Plotly.newPlot(GraficoVisuli, data_visuli, layout_visuli, {scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displaylogo: false});
