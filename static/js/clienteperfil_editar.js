let telNewKeys = "";
let telOGKeys = "";
let tel = "";
let telPos = 0;
let telComp = false;

$(document).ready(function() {
    $('.phone-number').inputmask({
        mask: "(99) 99999-9999",    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true,      // Optional: show mask on focus only
        oncomplete: function() {
            telComp = true;
            telOGKeys = this.value.replace("(", "").replace(")", "").replace(" ", "").replace("-", "");
            tel = telOGKeys;
        }
    }).on('keydown', function(e) {
        if (telComp) {
            console.log(e.key);
            if ((e.key === "Backspace") || (e.key === "Delete")) {
                telNewKeys = "";
                telPos = 0;
                telComp = false;
            }
            else {
                telNewKeys += e.key;
                telPos += 1;

                if (tel[0] === "5") {
                    tel = tel.slice(1) + telNewKeys[telPos - 1];
                }

                this.value = tel;
            }
        }
    });

    $('.cpf-cnpj').inputmask({
        mask: ["99999999999", "99999999999999"],    // Specify the format here
        placeholder: "_",           // Placeholder character
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: true       // Optional: show mask on focus only
    });
});