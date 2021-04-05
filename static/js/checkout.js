let counter = 0;
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
};

const refresh = () => {
    handleBreadcrumb();
    switchPage();
    if (counter !== 1) {
        addAddress.classList.add('d-none');
    } else {
        addAddress.classList.remove('d-none');
    }
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

// DATEFIELD START--------------------------------
const configureDate = (date) => {
    let month = date.getMonth() + 1;
    let day = date.getDate();
    const year = date.getFullYear();

    const hours =
        date.getHours() < 10 ? '0' + date.getHours() : date.getHours();
    const time = hours + ':' + date.getMinutes();

    if (month < 10) month = '0' + month.toString();
    if (day < 10) day = '0' + day.toString();

    const convertedDate = year + '-' + month + '-' + day;
    return { time, date: convertedDate };
};

const cartDate = document.querySelector('.cart-date');
const cartTime = document.querySelector('.cart-time');
const dtToday = new Date();
let dtTomorrow = new Date();
dtTomorrow.setDate(new Date().getDate() + 1);
const twoWeeks = new Date(Date.now() + 12096e5);

const convertedDtToday = configureDate(dtToday).date;
const convertedDtTomorrow = configureDate(dtTomorrow).date;
const convertedTwoWeeks = configureDate(twoWeeks).date;
const convertedTime = configureDate(dtToday).time;

cartDate.setAttribute('min', convertedDtToday);
cartDate.setAttribute('max', convertedTwoWeeks);

let setDateTimeMins = () => {
    // If 8am - 5pm, set the minimum time to whatever time it is right now
    if (
        ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17'].some((v) =>
            convertedTime.includes(v)
        )
    ) {
        cartTime.setAttribute('min', convertedTime);
    }

    // If 12am - 7am, set the minimum time to 8am
    else if (
        ['00', '01', '02', '03', '04', '05', '06', '07'].some((v) =>
            convertedTime.includes(v)
        )
    ) {
        cartTime.setAttribute('min', '08:00');
    }

    // If 6pm-11pm, set the minimum date to tomorrow and minimum time to 8am
    else {
        cartTime.setAttribute('min', '08:00');
        cartDate.setAttribute('min', convertedDtTomorrow);
        cartDate.setAttribute('value', convertedDtTomorrow);
    }
};

cartDate.addEventListener('change', (e) => {
    if (e.target.value === convertedDtToday) {
        setDateTimeMins();
    } else {
        cartTime.setAttribute('min', '08:00');
        cartDate.setAttribute('min', convertedDtToday)
    }
});

// DATEFIELD END--------------------------------

// ORDER DETAILS START--------------------------------
const orderTotal = document.querySelector('.order-total');
const deliveryFee = document.querySelector('.delivery-fee');
const totalAmount = document.querySelector('.total-amount');

const refreshTotal = () => {
    totalAmount.textContent = (
        parseFloat(orderTotal.textContent) + parseFloat(deliveryFee.textContent)
    ).toFixed(2);
};

refreshTotal();

const cartAddress = document.querySelector('.cart-address');
const cartPayment = document.querySelector('.cart-payment');
const detailDate = document.querySelector('.cart-detail-date');
const detailTime = document.querySelector('.cart-detail-time');
const detailPayment = document.querySelector('.cart-detail-payment');
const detailAddress = document.querySelector('.cart-detail-address');

// COVERTING DATE AND TIME
const convertDate = (date) => {
    const months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ];

    let month = parseInt(date.slice(5, 7));
    return months[month - 1] + ' ' + date.slice(-2) + ', ' + date.slice(0, 4);
};

const convertTime = (time) => {
    if (cartTime.value) {
        let hour = parseInt(time.slice(0, 2));
        if (hour > 12) {
            return hour - 12 + time.slice(2) + ' PM';
        } else if (hour === 12) {
            return hour + time.slice(2) + ' PM';
        } else {
            return hour + time.slice(2) + ' AM';
        }
    }
};
// ------------------------

const checkAddressFee = () => {
    let deliveryCity =
        cartAddress.options[cartAddress.selectedIndex].dataset.city;
    if (deliveryCity) {
        if (
            ['quezon city', 'san juan city'].includes(
                deliveryCity.toLowerCase()
            )
        ) {
            deliveryFee.textContent = '100.00';
        } else {
            deliveryFee.textContent = '150.00';
        }
    }
};

cartAddress.addEventListener('change', (e) => {
    let selectedAddress = e.target.options[e.target.selectedIndex].text;
    detailAddress.textContent = selectedAddress;
    if (
        cartPayment.options[cartPayment.selectedIndex].text !== 'Cash On Pickup'
    ) {
        checkAddressFee();
    }
    refreshTotal();
});

cartDate.addEventListener('change', () => {
    let convertedDate = convertDate(cartDate.value);
    detailDate.textContent = convertedDate;
});

cartTime.addEventListener('change', () => {
    let convertedTime = convertTime(cartTime.value);
    detailTime.textContent = convertedTime;
});

cartPayment.addEventListener('change', (e) => {
    let selectedPayment = e.target.options[e.target.selectedIndex].text;
    detailPayment.textContent = selectedPayment;

    if (selectedPayment == 'Cash On Pickup') {
        deliveryFee.textContent = '0.00';
    } else {
        checkAddressFee();
    }
    refreshTotal();
});
