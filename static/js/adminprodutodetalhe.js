const imgButtons = document.querySelectorAll(".imgWrapper > button");
const imgButtonsImgs = document.querySelectorAll(".imgWrapper > button > img");
const imgMain = document.querySelectorAll(".mainImg");

imgButtons.forEach(e => {
    e.addEventListener("click", function(event) {
        imgMain.forEach(e => {
            e.src = event.target.src;
        });        

        imgButtonsImgs.forEach(t => {
            t.style.borderBottom = "none";
        })

        event.target.style.borderBottom = "5px solid #ff9900";
    });
});