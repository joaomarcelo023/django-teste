const l = document.querySelectorAll('.option');

l.forEach(e => {        
    e.addEventListener('click', function () {
        l.forEach(t => {
            t.classList.remove("selected");
        });
        e.classList.add("selected");
    });
});