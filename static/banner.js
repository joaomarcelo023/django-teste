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
