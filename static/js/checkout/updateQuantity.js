const updateQuantity = document.querySelectorAll('.update-cart');

for (let arrowButton of updateQuantity) {
    arrowButton.addEventListener('click', (e) => {
        let item = e.target.dataset.product;
        let action = e.target.dataset.action;
        updateUserOrder(item, action);
    });
}

const updateUserOrder = (item, action) => {
    fetch('/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ item, action }),
    })
        .then((res) => res.json())
        .then((data) => location.reload());
};
