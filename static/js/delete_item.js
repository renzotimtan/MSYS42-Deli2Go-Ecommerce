// Get the modal
const modal = document.querySelector('.modal');
const deleteButton = document.querySelector('.delete-item');
const no = document.querySelector('.delete-item-no');
const yes = document.querySelector('.delete-item-yes');

// When the user clicks on the button, open the modal
deleteButton.addEventListener('click', (e) => {
    e.preventDefault();
    modal.style.display = 'block';
});

no.addEventListener('click', () => {
    modal.style.display = 'none';
});

yes.addEventListener('click', (e) => {
    modal.style.display = 'none';
    let item = e.target.dataset.product;

    fetch('/cashier/delete-items/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ item }),
    })
        .then((res) => res.json())
        .then((data) => {
            location.href = '/cashier/edit-inventory/';
        });
});

// When the user clicks anywhere outside of the modal, close it
window.addEventListener('click', (e) => {
    if (e.target == modal) {
        modal.style.display = 'none';
    }
});
