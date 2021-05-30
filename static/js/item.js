const addToCart = document.querySelector('.addtocart');
const addToCartQuantity = document.querySelector('.addtocart-quantity');

addToCart.addEventListener('click', (e) => {
    e.preventDefault()
    let item = e.target.dataset.product;
    let quantity = addToCartQuantity.value;
    if (quantity > 0) {
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
    } 
    
});
