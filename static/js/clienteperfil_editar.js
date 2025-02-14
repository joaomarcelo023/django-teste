$(document).ready(function() {
    $('.phone-number').inputmask({
        mask: "(99) 99999-9999",    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true       // Optional: show mask on focus only
    });

    $('.cpf-cnpj').inputmask({
        mask: ["99999999999", "99999999999999"],    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true       // Optional: show mask on focus only
    });
});