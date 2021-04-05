// CSRF Token for JavaScript
function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getToken('csrftoken');

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
