const control = document.querySelectorAll('.control');
let currentItem = 0;
let touchEndtX =0
let touchStartX =0
const item = document.querySelectorAll('.item');
const wrapper = document.getElementById('WrapperId');
const maxItems = item.length;

var containerWidth = wrapper.clientWidth;
    var items = document.querySelectorAll('.item');
    items.forEach(function(item) {
        item.style.width = containerWidth + 'px';
    });

item[currentItem].scrollIntoView({
        inline: "center",
        block: "nearest"
    });

function handleClick(isLeft) {

    //ALETRNATIVA INICIAL
    //currentItem = findCurrentItem();
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

function handleTouchEnd(event) {
    //ALETRNATIVA INICIAL
    //setTimeout(() => {
    //    handleClick(-1);
    //}, 100);

    //ALTERNATIVA SECUNDARIA
    transX = touchEndtX - touchStartX
    console.log(transX)
    if (transX > 0) {
        setTimeout(() => {
        handleClick(1);
    }, 100);}
    else {
        setTimeout(() => {
        handleClick(0);
    }, 100);
    }


    console.log('primeira posição do toque em X:', touchStartX,'Última posição do toque em X:', touchEndtX);

}

function handleTouchStart(event) {

    const touch = event.touches[0];

    touchStartX = touch.clientX;
}

function handleTouchMove(event) {
    const lastTouch = event.touches[event.touches.length - 1];
    touchEndtX = lastTouch.clientX;

}

control.forEach(control => {
    const isLeft = control.classList.contains('arrow-left');

    control.addEventListener("click", () => handleClick(isLeft));
});

wrapper.addEventListener('touchend',handleTouchEnd)

wrapper.addEventListener('touchstart',handleTouchStart)

document.addEventListener('touchmove', handleTouchMove);