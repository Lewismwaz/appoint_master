// Function to open the popup
function openPopup() {
    let popup = document.getElementById("popup");
    if (popup) {
        popup.classList.add("open-popup");
    }
}

// Function to close the popup
function closePopup() {
    let popup = document.getElementById("popup");
    if (popup) {
        popup.classList.remove("open-popup");
    }
}

// Call openPopup() function when the document is ready or when the page is reloaded
document.addEventListener("DOMContentLoaded", openPopup);
