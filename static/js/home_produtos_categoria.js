function handleClickRightProdutos2() {
    currentProduto = findCurrentRightItem2();

    document.querySelectorAll('.produtos_' + `{{ cat.slug }}`)[currentProduto].scrollIntoView({
        inline: "start",
        behavior: "smooth",
        block: "nearest"
    });
}

function findCurrentRightItem2() {
    const viewportLeft = window.scrollX;
    const viewportRight = viewportLeft + window.innerWidth;
    let maxRight = -Infinity;
    let currentItemIndex = -1;

    document.querySelectorAll('.produtos_' + `{{ cat.slug }}`).forEach((produto, index) => {
        const bounding = produto.getBoundingClientRect();
        const visibleWidth = Math.min(viewportRight, bounding.right) - Math.max(viewportLeft, bounding.left);

        if (bounding.right > maxRight && bounding.left < viewportRight) {
            maxRight = bounding.right;
            currentItemIndex = index;
        }
    });

    return currentItemIndex;
}

function handleClickLeftProdutos2() {
    currentProduto = findCurrentLeftItem2();

    document.querySelectorAll('.produtos_' + `{{ cat.slug }}`)[currentProduto].scrollIntoView({
        inline: "end",
        behavior: "smooth",
        block: "nearest"
    });
}

function findCurrentLeftItem2() {
    const viewportLeft = window.scrollX;
    const viewportRight = viewportLeft + window.innerWidth;
    let minLeft = Infinity;
    let currentItemIndex = -1;

    document.querySelectorAll('.produtos_' + `{{ cat.slug }}`).forEach((produto, index) => {
        const bounding = produto.getBoundingClientRect();
        const visibleWidth = Math.min(viewportRight, bounding.right) - Math.max(viewportLeft, bounding.left);

        if (bounding.left < minLeft && bounding.right > viewportLeft) {
            minLeft = bounding.left;
            currentItemIndex = index;
        }
    });

    return currentItemIndex;
}

document.querySelector('.arrow_right_' + `{{ cat.slug }}`).addEventListener("click", (event) => {
    event.preventDefault();
    handleClickRightProdutos2();
});

document.querySelector('.arrow_left_' + `{{ cat.slug }}`).addEventListener("click", (event) => {
    event.preventDefault();
    handleClickLeftProdutos2();
});