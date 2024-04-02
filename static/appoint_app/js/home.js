// Auto-hide messages after 4 seconds
setTimeout(function () {
    var messages = document.querySelectorAll('.message');
    messages.forEach(function (message) {
        message.style.display = 'none';
    });
}, 4000);

function toggleSearchButton() {
    var searchInput = document.getElementById("searchInput");
    var searchButton = document.getElementById("searchButton");

    // Enable the button if the input has a value, disable otherwise
    searchButton.disabled = !searchInput.value.trim();
}
