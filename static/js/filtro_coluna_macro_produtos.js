document.addEventListener("DOMContentLoaded", function() {
// Popup de indicação de uso e variação das faces
const indicUsoButton = document.querySelectorAll(".indicUsoButton");
const indicUsowindow = document.querySelectorAll(".indicUsoWindow");
const indicUsoJanelaClose = document.querySelectorAll(".indicUsoJanelaClose");

const variacaoFacesButton = document.querySelectorAll(".variacaoFacesButton");
const variacaoFacesWindow = document.querySelectorAll(".variacaoFacesWindow");
const variacaoFacesJanelaClose = document.querySelectorAll(".variacaoFacesJanelaClose");

console.log(indicUsoButton)
indicUsoButton.forEach((iub, i) => {
    iub.addEventListener("click", () => {
        if (indicUsowindow[i].style.display === "none") {
            indicUsowindow[i].style.display = "block";
        }
        else {
            indicUsowindow[i].style.display = "none";
        }

        if (variacaoFacesWindow[i].style.display === "block") {
            variacaoFacesWindow[i].style.display = "none";
        }
    });
});


indicUsoJanelaClose.forEach((iujc, i) => {
    iujc.addEventListener("click", () => {
        if (indicUsowindow[i].style.display === "none") {
            indicUsowindow[i].style.display = "block";
        }
        else {
            indicUsowindow[i].style.display = "none";
        }
    });
});

variacaoFacesButton.forEach((vfb, i) => {
    vfb.addEventListener("click", () => {
        if (variacaoFacesWindow[i].style.display === "none") {
            variacaoFacesWindow[i].style.display = "block";
        }
        else {
            variacaoFacesWindow[i].style.display = "none";
        }

        if (indicUsowindow[i].style.display === "block") {
            indicUsowindow[i].style.display = "none";
        }
    });
});

variacaoFacesJanelaClose.forEach((vfjc, i) => {
    vfjc.addEventListener("click", () => {
        if (variacaoFacesWindow[i].style.display === "none") {
            variacaoFacesWindow[i].style.display = "block";
        }
        else {
            variacaoFacesWindow[i].style.display = "none";
        }
    });
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
});