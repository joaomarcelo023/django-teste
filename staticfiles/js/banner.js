const control = document.querySelectorAll('.control');
let currentItem = 0;
let touchEndtX = 0;
let touchStartX = 0;
const wrapper = document.getElementById('WrapperId');
const slideshowContainer = document.querySelector('.gallery-wrapper');

function atualiza_item(event) {
    const item = document.querySelectorAll('.item');
    const maxItems = item.length;

    // Garantir que o currentItem ainda esteja no intervalo
    if (currentItem >= maxItems) {
        currentItem = maxItems - 1;
    }

    item.forEach(item => item.classList.remove('current-item'));
    if (item[currentItem]) {
        item[currentItem].classList.add('current-item');
    }

}

function atualiza_item2(event) {

    var containerWidth = wrapper.clientWidth;

    var item_grande = document.querySelectorAll('.item-grande');
    var item_pequeno = document.querySelectorAll('.item-pequeno');

    if (containerWidth > 1000) {
        item_grande.forEach(function(item) {
            item.classList.add('item');
        });
        if (item_grande.length > 0) {
            item_grande[0].classList.add('current-item');
        }

    } else {
        item_pequeno.forEach(function(item) {
            item.classList.add('item');
        });
        if (item_pequeno.length > 0) {
            item_pequeno[0].classList.add('current-item');
        }
    }

    const item = document.querySelectorAll('.item');
    const maxItems = item.length;

    // Garantir que o currentItem ainda esteja no intervalo
    if (currentItem >= maxItems) {
        currentItem = maxItems - 1;
    }

}

atualiza_item2(); // Inicializar

const item = document.querySelectorAll('.item');
let maxItems = item.length;

function handleClick(isLeft) {

    // Altera para o slide à esquerda do atual
    if (isLeft == 1) {
        currentItem -= 1;
    }
    // Altera para o slide à direita do atual
    if (isLeft == 0) {
        currentItem += 1;
    }

    if (currentItem >= maxItems) {
        currentItem = 0;
    }

    if (currentItem < 0) {
        currentItem = maxItems - 1;
    }

    item.forEach(item => item.classList.remove('current-item'));
    item[currentItem].classList.add('current-item');
    // item[currentItem].scrollIntoView({
    //     inline: "center",
    //     behavior: "smooth",
    //     block: "nearest"
    // });
    // const container = document.querySelector('.gallery-wrapper');
    const offsetLeft = item[currentItem].offsetLeft;

    slideshowContainer.scrollTo({
        left: offsetLeft,
        behavior: "smooth"
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

control.forEach(control => {
    const isLeft = control.classList.contains('arrow-left');

    control.addEventListener("click", () => handleClick(isLeft));
});

// Recalcular quando a página for redimensionada
window.addEventListener('resize', () => {
    atualiza_item(); // Recalcula os itens e atualiza
    maxItems = document.querySelectorAll('.item').length;// Atualiza o número de itens após o redimensionamento
});

// -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

// Controle de transição de slide pelo toque em touchscreens e arraste do mouse
// const slideshowContainer = document.querySelector('.gallery-wrapper');
let startX;
let isDragging = false;

// Evento de touch
//// Coleta posição x inicial do toque
slideshowContainer.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
});

//// Coleta posição x final do toque e roda a transição
slideshowContainer.addEventListener('touchend', (e) => {
    let endX = e.changedTouches[0].clientX;
    // if ((((startX - endX) > -lim) || ((startX - endX) < lim)) && (window.getComputedStyle(document.querySelector('.item-grande')).display === "none")){
    //     window.open(document.getElementById("L" + (currentItem + 1)).href, "_blank");
    // }
    handleSwipe(startX, endX);
});
//// Lida com click no caso de touch
if ((window.getComputedStyle(document.querySelector('.item-grande')).display === "none")) {
    slideshowContainer.addEventListener("click", () => {
        window.open(document.getElementById("L" + (currentItem + 1)).href, "_blank");
    });
}

// Evento de mouse
//// Coleta posição x inicial do clique
slideshowContainer.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX;
});

//// Coleta posição x final do clique e roda a transição
slideshowContainer.addEventListener('mouseup', (e) => {
    if (isDragging) {
        handleSwipe(startX, e.clientX);
        isDragging = false;
    }
});

//// Cancela o evento se o mouse sair da região do banner
slideshowContainer.addEventListener('mouseleave', () => {
    isDragging = false;
});

// Controle de transição
function handleSwipe(start, end) {
    const diffX = start - end;
    const lim = 50; // Valor limite em pixels para que ocorra a transição

    // Transição para esquerda / vai para o slide da direita - Final < Inicial
    if (diffX > lim) {
        handleClick(0);
    }
    // Transição para direita / vai para o slide da esquerda - Final > Inicial
    else if (diffX < -lim) {
        handleClick(1);
    }
    else if (((diffX > -lim) || (diffX < lim)) && (window.getComputedStyle(document.querySelector('.item-grande')).display !== "none")) {
        window.open(document.getElementById("L" + (currentItem + 1)).href, "_blank");
    }
}

const t = setInterval(function () {
    handleClick(0);
}, 15000);