const breadSection = document.querySelectorAll('.breadcrumb-section');
const pages = document.querySelectorAll('.cart-left');
const next = document.querySelector('.checkout-next');
const back = document.querySelector('.checkout-back');
const submit = document.querySelector('.checkout-submit');
const addAddress = document.querySelector('.add-address');

document.querySelector('.checkout-next').addEventListener('click', (e) => {
    e.preventDefault();
});
document.querySelector('.checkout-back').addEventListener('click', (e) => {
    e.preventDefault();
});

// BREADCRUMB START--------------------------------
let counter = 0;

const handleBreadcrumb = () => {
    for (let section of breadSection) {
        section.classList.remove('active');
        breadSection[counter].classList.add('active');
    }

    if (counter === 0) {
        back.classList.add('d-none');
    } else {
        back.classList.remove('d-none');
    }

    if (counter === breadSection.length - 1) {
        next.classList.add('d-none');
        submit.classList.remove('d-none');
    } else {
        next.classList.remove('d-none');
        submit.classList.add('d-none');
    }
};

const switchPage = () => {
    for (let page of pages) {
        page.classList.add('d-none');
    }
    pages[counter].classList.remove('d-none');

    if (counter !== 1) {
        addAddress.classList.add('d-none');
    } else {
        addAddress.classList.remove('d-none');
    }
};

const refresh = () => {
    handleBreadcrumb();
    switchPage();
};

refresh();

next.addEventListener('click', () => {
    counter++;
    refresh();
});

back.addEventListener('click', () => {
    counter--;
    refresh();
});

// BREADCRUMB END--------------------------------
