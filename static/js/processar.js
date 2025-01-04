const optionLabel = document.querySelectorAll('.option');
const optionTitleLabel = document.querySelector('.option_title');

optionLabel.forEach(e => {        
    e.addEventListener('click', function () {
        optionLabel.forEach(t => {
            t.classList.remove("selected");

            t.querySelector('.option_title').classList.remove("selected");
            if (t.querySelector('.methods')) {
                t.querySelector('.methods').style.display = "none";
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
        }
    });
});