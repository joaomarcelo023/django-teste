const arrowRightProdutos = document.querySelectorAll('.arrow-right-produtos');
const arrowLeftProdutos = document.querySelectorAll('.arrow-left-produtos');
let currentProduto = 0;
const produtos = document.querySelectorAll('.produtos');
const produtosWrapper = document.getElementById('produtos-wrapperId');
const maxProduto = produtos.length;

function handleClickRightProdutos() {
    currentProduto = findCurrentRightItem();

    produtos[currentProduto].scrollIntoView({
        inline: "start",
        behavior: "smooth",
        block: "nearest"
    });
}

function findCurrentRightItem() {
    const viewportLeft = window.scrollX;
    const viewportRight = viewportLeft + window.innerWidth;
    let maxRight = -Infinity;
    let currentItemIndex = -1;

    produtos.forEach((produto, index) => {
        const bounding = produto.getBoundingClientRect();
        const visibleWidth = Math.min(viewportRight, bounding.right) - Math.max(viewportLeft, bounding.left);

        if (bounding.right > maxRight && bounding.left < viewportRight) {
            maxRight = bounding.right;
            currentItemIndex = index;
        }
    });

    return currentItemIndex;
}

function handleClickLeftProdutos() {
    currentProduto = findCurrentLeftItem();

    produtos[currentProduto].scrollIntoView({
        inline: "end",
        behavior: "smooth",
        block: "nearest"
    });
}

function findCurrentLeftItem() {
    const viewportLeft = window.scrollX;
    const viewportRight = viewportLeft + window.innerWidth;
    let minLeft = Infinity;
    let currentItemIndex = -1;

    produtos.forEach((produto, index) => {
        const bounding = produto.getBoundingClientRect();
        const visibleWidth = Math.min(viewportRight, bounding.right) - Math.max(viewportLeft, bounding.left);

        if (bounding.left < minLeft && bounding.right > viewportLeft) {
            minLeft = bounding.left;
            currentItemIndex = index;
        }
    });

    return currentItemIndex;
}

arrowRightProdutos.forEach(arrowRightProduto => {
    arrowRightProduto.addEventListener("click", (event) => {
        event.preventDefault();
        handleClickRightProdutos();
    });
});

arrowLeftProdutos.forEach(arrowLeftProduto => {
    arrowLeftProduto.addEventListener("click", (event) => {
        event.preventDefault();
        handleClickLeftProdutos();
    });
});
