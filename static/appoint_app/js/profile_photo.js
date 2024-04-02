function choosePhoto() {
    document.getElementById('id_profile_photo').click();
}

function showPreview(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.createElement('img');
            preview.src = e.target.result;
            preview.classList.add('w-24', 'h-24', 'rounded-full', 'mt-2', 'cursor-pointer');
            preview.setAttribute('onclick', 'choosePhoto()');

            const container = input.parentElement;
            const existingImage = container.querySelector('img');
            if (existingImage) {
                container.removeChild(existingImage);
            }
            container.appendChild(preview);
        };
        reader.readAsDataURL(file);
    }
}