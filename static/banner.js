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

control.forEach(control => {
control.addEventListener("click",() => {
    const isLeft = control.classList.contains('arrow-left')
    console.log('control clicked')

    if(isLeft){
    currentItem -= 1;
    } else {
    currentItem += 1;
    }

    if(currentItem >= maxItems){
        currentItem = 0;
    }

    if(currentItem < 0){
        currentItem = maxItems -1;
    }

    item.forEach(item => item.classList.remove('current-item'));

    item[currentItem].scrollIntoView({
        inline: "center",
        behavior: "smooth",
        block: "nearest"
    });

    item[currentItem].classList.add("current-item");
    console.log("control", isLeft, currentItem, maxItems);
});
});