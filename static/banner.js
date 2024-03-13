const control = document.querySelectorAll('.control');
let currentItem = 0;
const item = document.querySelectorAll('.item');
const maxItems = item.length;

var containerWidth = document.querySelector('.container-custom').clientWidth;
    var items = document.querySelectorAll('.item');
    items.forEach(function(item) {
        item.style.width = containerWidth + 'px';
    });

item[currentItem].scrollIntoView({
        inline: "center",
        block: "nearest"
    });

function handleClick(isLeft) {
    console.log('control clicked');

    if (isLeft) {
        currentItem -= 1;
    } else {
        currentItem += 1;
    }

    if (currentItem >= maxItems) {
        currentItem = 0;
    }

    if (currentItem < 0) {
        currentItem = maxItems - 1;
    }

    item.forEach(item => item.classList.remove('current-item'));
    item[currentItem].classList.add('current-item')
    item[currentItem].scrollIntoView({
        inline: "center",
        behavior: "smooth",
        block: "nearest"
    });
}

// Iterar sobre os controles e adicionar o ouvinte de evento a cada um
control.forEach(control => {
    // Verificar se o controle é uma seta para a esquerda ou para a direita
    const isLeft = control.classList.contains('arrow-left');

    // Adicionar o ouvinte de evento de clique ao controle
    control.addEventListener("click", () => handleClick(isLeft));
});


const imageContainers  = document.getElementsByClassName('container-custom');
const image = document.getElementById('image');
const arrowLeftButton = document.getElementsByClassName('arrow-left');
const arrowRightButton = document.getElementsByClassName('arrow-right');
console.log(arrowRightButton);

let isDragging = false;
let startX = 0;
let currentX = 0;
let translateX = 0;

if (imageContainers.length > 0) {
    // Iterar sobre a coleção de elementos
    for (let i = 0; i < imageContainers.length; i++) {
        const imageContainer = imageContainers[i];

        // Adicionar o ouvinte de evento a cada elemento individualmente
        imageContainer.addEventListener('mousedown', startDrag);
        imageContainer.addEventListener('touchstart', startDrag);
    }
} else {
    console.error('Nenhum elemento com a classe "container-custom" encontrado.');
}

function startDrag(event) {
    event.preventDefault();

    if (event.touches) {
        startX = event.touches[0].clientX;
    } else {
        startX = event.clientX;
    }

    isDragging = true;

    document.addEventListener('mousemove', drag);
    document.addEventListener('touchmove', drag);
    document.addEventListener('mouseup', stopDrag);
    document.addEventListener('touchend', stopDrag);
}

function drag(event) {
    if (!isDragging) return;

    event.preventDefault();

    if (event.touches) {
        currentX = event.touches[0].clientX;
    } else {
        currentX = event.clientX;
    }

}

function stopDrag() {
        translateX = currentX - startX;
        console.log(translateX);

        if (translateX > 0) {
        handleClick(0)
    } else {
        handleClick(1)
    }

    isDragging = false;
    document.removeEventListener('mousemove', drag);
    document.removeEventListener('touchmove', drag);
    document.removeEventListener('mouseup', stopDrag);
    document.removeEventListener('touchend', stopDrag);
}