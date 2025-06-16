// Adiciona foto
//// Banner Grande
const botaoG = document.getElementById('img_big')
const inputG = document.getElementById('img_big_input')
const textG = document.getElementById('img_big_name')
if (botaoG) {
    // Conecta imagem ao input
    botaoG.addEventListener('click', function () {
        inputG.click();
    });

    // Muda a imagem no preview
    inputG.addEventListener('change', function() {
        const reader = new FileReader();
        reader.onload = function(event) {
            botaoG.src = event.target.result;
        };
        reader.readAsDataURL(this.files[0]);

        // Escreve o nome do arquivo
        textG.textContent = this.files[0].name
    });
}

//// Banner Pequena
const botaoP = document.getElementById('img_small')
const inputP = document.getElementById('img_small_input')
const textP = document.getElementById('img_small_name')
if (botaoP) {
    // Conecta imagem ao input
    botaoP.addEventListener('click', function () {
        inputP.click();
    });

    // Muda a imagem no preview
    inputP.addEventListener('change', function() {
        const reader = new FileReader();
        reader.onload = function(event) {
            botaoP.src = event.target.result;
        };
        reader.readAsDataURL(this.files[0]);

        // Escreve o nome do arquivo
        textP.textContent = this.files[0].name
    });
}