document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.getElementById('menuButton');
    const popupMenu = document.getElementById('popupMenu');
    const closeButton = document.getElementById('closeButton');

    menuButton.addEventListener('click', function () {
        popupMenu.style.display = 'block';
        setTimeout(function () {
        popupMenu.style.opacity = 1;
        }, 100);
    });

    closeButton.addEventListener('click', function () {
        popupMenu.style.opacity = 0;
        setTimeout(function () {
            popupMenu.style.display = 'none';
            menuButton.style.display = 'block'
        }, 500);

    });


});