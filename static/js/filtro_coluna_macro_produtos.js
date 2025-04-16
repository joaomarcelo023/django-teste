// Popup de indicação de uso e variação das faces
const indicUsoButton = document.querySelector(".indicUsoButton");
const indicUsowindow = document.querySelector(".indicUsoWindow");
const indicUsoJanelaClose = document.querySelector(".indicUsoJanelaClose");

const variacaoFacesButton = document.querySelector(".variacaoFacesButton");
const variacaoFacesWindow = document.querySelector(".variacaoFacesWindow");
const variacaoFacesJanelaClose = document.querySelector(".variacaoFacesJanelaClose");

indicUsoButton.addEventListener("click", () => {
    if (indicUsowindow.style.display === "none") {
        indicUsowindow.style.display = "block";
    }
    else {
        indicUsowindow.style.display = "none";
    }

    if (variacaoFacesWindow.style.display === "block") {
        variacaoFacesWindow.style.display = "none";
    }
});

indicUsoJanelaClose.addEventListener("click", () => {
    if (indicUsowindow.style.display === "none") {
        indicUsowindow.style.display = "block";
    }
    else {
        indicUsowindow.style.display = "none";
    }
});

variacaoFacesButton.addEventListener("click", () => {
    if (variacaoFacesWindow.style.display === "none") {
        variacaoFacesWindow.style.display = "block";
    }
    else {
        variacaoFacesWindow.style.display = "none";
    }

    if (indicUsowindow.style.display === "block") {
        indicUsowindow.style.display = "none";
    }
});

variacaoFacesJanelaClose.addEventListener("click", () => {
    if (variacaoFacesWindow.style.display === "none") {
        variacaoFacesWindow.style.display = "block";
    }
    else {
        variacaoFacesWindow.style.display = "none";
    }
});

$(document).ready(function() {
    $('.precoInput').inputmask("currency", {
        prefix: "R$ ",
        radixPoint: ",",
        digits: 2,
        digitsOptional: false,
        placeholder: "0",
        rightAlign: false,
        removeMaskOnSubmit: true,  // Optional: useful when posting the form
        autoUnmask: true,           // Optional: removes formatting on input's .val()
        showMaskOnHover: false,     // Optional: remove mask on hover
        showMaskOnFocus: false,      // Optional: show mask on focus only
    });
});