const files = document.getElementById('files');
const removeImage = document.querySelector('.remove-image');

// image upload
files.onchange = function () {
    var reader = new FileReader();

    reader.onload = function (e) {
        // get loaded data and render thumbnail.
        document.getElementById('image').src = e.target.result;
    };
    // read the image file as a data URL.
    reader.readAsDataURL(this.files[0]);
};

removeImage.addEventListener('click', (e) => {
    e.preventDefault();
    files.value = '';
    document.getElementById('image').src = '';
});
