function togglePasswordVisibility(inputId, iconId) {
    var passwordInput = document.getElementById(inputId);
    var passwordIcon = document.getElementById(iconId);
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordIcon.classList.remove('fa-eye');
        passwordIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        passwordIcon.classList.remove('fa-eye-slash');
        passwordIcon.classList.add('fa-eye');
    }
}

// Auto-hide messages after 4 seconds and scroll to the top
setTimeout(function () {
    var messages = document.querySelectorAll('.messages li');
    messages.forEach(function (message) {
        message.style.display = 'none';
    });

    // Scroll to the top
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}, 4000);
