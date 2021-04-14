// const deleteButtons = document.querySelectorAll('.delete-address');

// for (let deleteButton of deleteButtons) {
//     deleteButton.addEventListener('click', (e) => {
//         let address = e.target.dataset.product;

//         fetch('/delete_address/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrftoken,
//             },
//             body: JSON.stringify({ address }),
//         })
//             .then((res) => res.json())
//             .then((data) => location.reload());
//     });
// }
