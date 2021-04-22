const viewButton = document.querySelectorAll('.view-order');
const editStatus = document.querySelectorAll('.edit-status');
const modals = document.querySelectorAll('.modal');
const closeButtons = document.querySelectorAll('.close');

for (let button of viewButton) {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        let order = e.target.dataset.product;
        const currentModal = document.querySelector(
            '.modal-' + order + '-items'
        );
        currentModal.style.display = 'block';
    });
}

for (let button of editStatus) {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        let order = e.target.dataset.product;
        const currentModal = document.querySelector(
            '.modal-' + order + '-status'
        );
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

// Status save

const statusSaveButtons = document.querySelectorAll('.status-save');

for (let button of statusSaveButtons) {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        let order = e.target.dataset.product;
        const currentModal = document.querySelector(
            '.modal-' + order + '-status .status-change'
        );
        const selectedValue = currentModal.value;

        fetch('/cashier/change-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ order, status: selectedValue }),
        })
            .then((res) => res.json())
            .then((data) => {
                location.reload();
            });
    });
}
