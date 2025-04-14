const mobile = document.querySelector(".pequeno");
const divPreco = document.querySelectorAll(".divPreco");

if (window.getComputedStyle(mobile).display === "none") {
    divPreco.forEach(div => {
        div.classList.remove("col-8");
        div.classList.add("col-9");
    });
} else {
    divPreco.forEach(div => {
        div.classList.add("col-8");
        div.classList.remove("col-9");
    });
}