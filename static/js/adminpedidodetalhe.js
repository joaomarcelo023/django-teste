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