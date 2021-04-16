// Get the modal
const deleteButtons = document.querySelectorAll('.delete-address');
const nos = document.querySelectorAll('.delete-address-no');
const yess = document.querySelectorAll('.delete-address-yes');
const modals = document.querySelectorAll('.modal');

const removeModal = () => {
    for (let modal of modals) {
        modal.style.display = 'none';
    }
};

for (let button of deleteButtons) {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        let address = e.target.dataset.product;
        const currentModal = document.querySelector('.modal-' + address);
        currentModal.style.display = 'block';
    });
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener('click', (e) => {
    for (let modal of modals) {
        if (e.target == modal) {
            modal.style.display = 'none';
        }
    }
});

for (let no of nos) {
    no.addEventListener('click', (e) => {
        removeModal();
    });
}

for (let yes of yess) {
    yes.addEventListener('click', (e) => {
        removeModal();
        let address =
            e.target.parentElement.parentElement.parentElement.dataset.product;

        fetch('/delete_address/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ address }),
        })
            .then((res) => res.json())
            .then((data) => location.reload());
    });
}
