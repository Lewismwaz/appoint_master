
function togglePasswordVisibility() {
    var passwordInput = document.getElementById('password');
    var passwordIcon = document.getElementById('passwordIcon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordIcon.className = 'fas fa-eye-slash';
    } else {
        passwordInput.type = 'password';
        passwordIcon.className = 'fas fa-eye';
    }
}

// Auto-hide messages after 4 seconds and scroll to the top
setTimeout(function () {
    var messages = document.querySelectorAll('.message');
    messages.forEach(function (message) {
        message.style.display = 'none';
    });

    // Scroll to the top
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}, 4000);

function validateLoginForm() {
    var usernameInput = document.getElementById('username');
    var passwordInput = document.getElementById('password');
    var messagesContainer = document.querySelector('.message-container');

    if (usernameInput.value.trim() === '' || passwordInput.value.trim() === '') {
        // Show a message indicating that fields are empty
        messagesContainer.innerHTML = '<div class="message message-error">Username/Password cannot be Empty!</div>';

        // Auto-hide messages after 4 seconds
        setTimeout(function () {
            var messages = document.querySelectorAll('.message');
            messages.forEach(function (message) {
                message.style.display = 'none';
            });
            // Scroll to the top
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }, 4000);

        return;
    }

    // If the fields are not empty, submit the form
    document.forms[0].submit();
}

