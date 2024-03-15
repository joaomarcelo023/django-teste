document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.getElementById('menuButton');
    const popupMenu = document.getElementById('popupMenu');
    const closeButton = document.getElementById('closeButton');
    let interruptor = 0;

    menuButton.addEventListener('click', function () {

        if (interruptor ==0){

        popupMenu.style.display = 'grid';
        setTimeout(function () {
        popupMenu.style.opacity = 1;
        }, 100);
        interruptor = 1;

        }else{

        popupMenu.style.opacity = 0;
        setTimeout(function () {
            popupMenu.style.display = 'none';
            menuButton.style.display = 'block'
        }, 500);
        interruptor = 0;

        }
    });

    closeButton.addEventListener('click', function () {
        popupMenu.style.opacity = 0;
        setTimeout(function () {
            popupMenu.style.display = 'none';
            menuButton.style.display = 'block'
        }, 500);
        interruptor = 0;
    });


});