const addToCart = document.querySelector('.addtocart');
const addToCartQuantity = document.querySelector('.addtocart-quantity');

addToCart.addEventListener('click', (e) => {
    let item = e.target.dataset.product;
    let quantity = addToCartQuantity.value;

    fetch('/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ item: item, quantity: quantity }),
    })
        .then((res) => res.json())
        .then((data) => location.reload());
});
