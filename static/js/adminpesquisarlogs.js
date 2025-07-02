const GraficoPesquisasTop = document.getElementById('graficoPesquisasTop');
const grafico_top_data_x = JSON.parse(document.getElementById('grafico_top_data_x').textContent);
const grafico_top_data_y = JSON.parse(document.getElementById('grafico_top_data_y').textContent);

var data = [
  {
    x: grafico_top_data_x,
    y: grafico_top_data_y,
    type: 'bar'
  }
];

var layout = {
    title: { text: "Top pesquisas" },
    margin: { l: 36, r: 21, t: 36, b: 225 }
};

Plotly.newPlot(GraficoPesquisasTop, data, layout, {scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displaylogo: false});

const GraficoPesquisasTopDias = document.getElementById('graficoPesquisasTopDias');
const grafico_top_dias_data_x = JSON.parse(document.getElementById('grafico_top_dias_data_x').textContent);
const grafico_top_dias_data_y = JSON.parse(document.getElementById('grafico_top_dias_data_y').textContent);

var data = [
  {
    x: grafico_top_dias_data_x,
    y: grafico_top_dias_data_y,
    type: 'bar'
  }
];

var layout = {
    title: { text: "Top pesquisas dos ultimos 30 dias" },
    margin: { l: 36, r: 21, t: 36, b: 225 }
};

Plotly.newPlot(GraficoPesquisasTopDias, data, layout, {scrollZoom: true, modeBarButtonsToRemove: ['lasso2d'], displaylogo: false});