var cepWarning = document.getElementById('cepWarning');

document.getElementById("addressForm").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
    }
});

$(document).ready(function() {
    $('.cep-input').inputmask({
        mask: "99999-999",          // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: false,      // Optional: show mask on focus only
        oncomplete: function() {
            var cep = this.value.trim(); // Remove espaços em branco

            if (cep.length === 9 && /^\d{5}-\d{3}$/.test(cep)) {
                fetchAddress(cep); // Se sim, busca o endereço
            }
        }
    });
});

// Adicionando um event listener para o evento 'change' do campo de CEP - a mask interfere então precisa desse e do oncomplete no inputmask
document.getElementById('cep').addEventListener('change', function() {
    var cep = this.value.trim(); // Remove espaços em branco

    if (cep.length === 9 && /^\d{5}-\d{3}$/.test(cep)) {
        fetchAddress(cep); // Se sim, busca o endereço
    }
});

function fetchAddress(cep) {
    // var cep = document.getElementById('cep').value.trim(); // Remove espaços em branco
    cep = cep.replace(/\D/g, '');

    // Verifica se o campo contém apenas números
    if (/^\d{8}$/.test(cep)) {
        fetch('https://viacep.com.br/ws/' + cep + '/json/')
            .then(response => response.json())
            .then(data => {
                console.log('CEP:', data.cep);
                console.log('Logradouro:', data.logradouro);
                console.log('Bairro:', data.bairro);
                console.log('Cidade:', data.localidade);
                console.log('Estado:', data.uf);

                if (data.localidade === "Teresópolis") {
                    document.getElementById('estado').value = data.uf;
                    document.getElementById('cidade').value = data.localidade;
                    document.getElementById('bairro').value = data.bairro;
                    document.getElementById('rua').value = data.logradouro;

                    document.getElementById("cidadeWarning").style.display = 'none';
                    document.querySelector(".buttonCadastrar").disabled = false;
                }
                else {
                    document.getElementById("cidadeWarning").style.display = 'block';

                    document.getElementById('estado').value = "";
                    document.getElementById('cidade').value = "";
                    document.getElementById('bairro').value = "";
                    document.getElementById('rua').value = "";
                    document.getElementById('numero').value = "";
                    document.getElementById('complemento').value = "";

                    document.querySelector(".buttonCadastrar").disabled = true;
                }
            })
            .catch(error => console.error('Erro ao buscar endereço:', error));
    } else {
        cepWarning.style.display = 'block'; // Exibe o aviso
        document.querySelector(".buttonCadastrar").disabled = true;
    }
}