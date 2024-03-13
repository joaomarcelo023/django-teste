const control = document.querySelectorAll('.control');
let currentItem = 0;
const item = document.querySelectorAll('.item');
const wrapper = document.getElementById('WrapperId');
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


    currentItem = findCurrentItem();
    console.log(currentItem);

    if (isLeft==1) {
        currentItem -= 1;
    }
    if (isLeft==0)
    {
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

function findCurrentItem() {
    const viewportLeft = window.scrollX;
    const viewportRight = viewportLeft + window.innerWidth;
    let maxVisibleWidth = 0;
    let currentItemIndex = 0;

    item.forEach((item, index) => {
        const bounding = item.getBoundingClientRect();
        const visibleWidth = Math.min(viewportRight, bounding.right) - Math.max(viewportLeft, bounding.left);
        if (visibleWidth > maxVisibleWidth) {
            maxVisibleWidth = visibleWidth;
            currentItemIndex = index;
        }
    });

    return currentItemIndex;
}

function handleTouch(event) {

    setTimeout(() => {
        handleClick(-1);
    }, 100);
    console.log('clicou')
}

// Iterar sobre os controles e adicionar o ouvinte de evento a cada um
control.forEach(control => {
    // Verificar se o controle é uma seta para a esquerda ou para a direita
    const isLeft = control.classList.contains('arrow-left');

    // Adicionar o ouvinte de evento de clique ao controle
    control.addEventListener("click", () => handleClick(isLeft));
});

wrapper.addEventListener('touchend',handleTouch)