const l = document.querySelectorAll('.option');

l.forEach(e => {        
    e.addEventListener('click', function () {
        l.forEach(t => {
            t.classList.remove("selected");
        });
        e.classList.add("selected");
    });
});

function updateFreteValue(radio) {
    const hiddenInput = document.getElementById('freteInput');
    const extraValue = radio.dataset.frete;
    hiddenInput.value = `${extraValue}`;
}