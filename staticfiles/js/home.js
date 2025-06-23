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