const addDriver = document.querySelectorAll('.add-driver');
const modals = document.querySelectorAll('.modal');
const closeButtons = document.querySelectorAll('.close');
const cancel = document.querySelectorAll('.cancel');

for (let button of addDriver) {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        let order = e.target.dataset.product;
        const currentModal = document.querySelector(`.modal-${order}`);
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

for (let button of closeButtons) {
    button.addEventListener('click', (e) => {
        button.parentElement.parentElement.style.display = 'none';
    });
}

// Driver save

const driverSaveButtons = document.querySelectorAll('.driver-save');

for (let button of driverSaveButtons) {
    console.log(driverSaveButtons);
    button.addEventListener('click', (e) => {
        e.preventDefault();
        let order = e.target.dataset.product;
        const currentModal = document.querySelector(
            '.modal-' + order + ' .driver-change'
        );
        const selectedValue = currentModal.value;

        fetch('/cashier/change-driver/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ order, driver: selectedValue }),
        })
            .then((res) => res.json())
            .then((data) => {
                location.reload();
            });
    });
}

for (let button of cancel) {
    button.addEventListener('click', (e) => {
        e.target.parentElement.parentElement.parentElement.style.display =
            'none';
    });
}
