const l = document.querySelectorAll('.option');

l.forEach(e => {        
    e.addEventListener('click', function () {
        l.forEach(t => {
            t.classList.remove("selected");
        });
        e.classList.add("selected");
    });
});

function updateFreteRetiradaValue(radio) {
    const hiddenInputFrete = document.getElementById('freteInput');
    const extraValueFrete = radio.dataset.frete;
    hiddenInputFrete.value = `${extraValueFrete}`;
    
    const hiddenInputRetirada = document.getElementById('DescontoRetiradaInput');
    const extraValueRetirada = radio.dataset.retirada;
    hiddenInputRetirada.value = `${extraValueRetirada}`;
}