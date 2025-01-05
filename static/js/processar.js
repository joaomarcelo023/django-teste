const optionLabel = document.querySelectorAll('.option');
const optionTitleLabel = document.querySelector('.option_title');

optionLabel.forEach(e => {        
    e.addEventListener('click', function () {
        optionLabel.forEach(t => {
            t.classList.remove("selected");

            t.querySelector('.option_title').classList.remove("selected");
            if (t.querySelector('.methods')) {
                t.querySelector('.methods').style.display = "none";
                t.querySelector('.methods > .option_parcelas select').name = "";
                // t.querySelector('.methods > .option_parcelas select').value = "";
            }
            
        });
        e.classList.add("selected");
        
        e.querySelector('.option_title').classList.add("selected");
        if (e.querySelector('.methods')) {
            // if (window.getComputedStyle(e.querySelector('.methods')).display === "none") {
            //     e.querySelector('.methods > .option_method input').checked = true;
            // }
            // else {
            //     e.querySelector('.methods > .option_method input').checked = false;
            // }
            e.querySelector('.methods').style.display = "block";

            if (e.querySelector('.methods > .credito  input').checked) {
                e.querySelector('.methods > .option_parcelas').style.display = "block";
                e.querySelector('.methods > .option_parcelas select').name = "parcelas";
                // e.querySelector('.methods > .option_parcelas select').value = "1";
                e.querySelector('.methods > .option_parcelas .total_normal').textContent = e.querySelector('.methods > .option_parcelas select').value + "x R$" +  ((parseFloat(e.querySelector('.methods > .credito .total_normal').innerText.replace("R$", "").replace(",", ".").trim()) / parseFloat(e.querySelector('.methods > .option_parcelas select').value)).toFixed(2)).replace(".", ",");
            }
            else {
                e.querySelector('.methods > .option_parcelas').style.display = "none";
            }
        }
    });
});