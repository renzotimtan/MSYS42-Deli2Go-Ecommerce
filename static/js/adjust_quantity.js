const arrowButton = document.querySelectorAll('.chg-quantity');
const quantityInput = document.querySelectorAll('.quantity-input');
const submit = document.querySelector('.adjust-quantity__save');

const changedValues = {};

for (let button of arrowButton) {
    button.addEventListener('click', (e) => {
        let item = e.target.dataset.product;
        let action = e.target.dataset.action;
        const quantity = document.querySelector('.quantity-' + item);
        if (action === 'add') {
            const newVal = parseInt(quantity.innerText) + 5;
            quantity.innerText = newVal;
            changedValues[item] = newVal;
        } else if (action == 'remove') {
            const newVal = parseInt(quantity.innerText) - 5;
            quantity.innerText = newVal;
            changedValues[item] = newVal;
        }
    });
}

submit.addEventListener('click', () => {
    fetch('/cashier/adjust-quantity-action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ quantities: changedValues }),
    })
        .then((res) => res.json())
        .then((data) => location.reload());
});
