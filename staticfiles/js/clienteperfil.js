const caixas = document.querySelectorAll(".perfilCont");
const PC = document.querySelector('.grande');
let caixaVisu = new URLSearchParams(window.location.search).get('perfil');
if (caixaVisu === null){
    caixaVisu = "ClienteInfo";
}

caixas.forEach(e => {
    if ((e.id === caixaVisu) && (window.getComputedStyle(PC).display !== "none")){
        e.style.display = "flex";
    }
    else if (window.getComputedStyle(PC).display === "none") {
        e.style.display = "flex";
    }
    else {
        e.style.display = "none";
    }
});

window.onload = function () {
    let messageDiv = document.getElementById("messages");
    let messages = messageDiv.getAttribute("data-messages");

    if (messages) {
        try {
            let parsedMessages = JSON.parse(messages);
            parsedMessages.forEach(msg => {
                alert(msg.text);
            });
        } catch (error) {
            console.error("Error parsing messages:", error);
        }
    }
};