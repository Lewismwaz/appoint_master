// Select all toggle buttons for password visibility
const toggleButtons = document.querySelectorAll('.toggle-password');

toggleButtons.forEach(button => {
  button.addEventListener('click', () => {
    const passwordField = button.closest('.relative').querySelector('input');
    const isPasswordVisible = passwordField.type === 'text';

    if (isPasswordVisible) {
      passwordField.type = 'password';
      button.querySelector('i').classList.remove('fa-eye-slash');
      button.querySelector('i').classList.add('fa-eye');
    } else {
      passwordField.type = 'text';
      button.querySelector('i').classList.remove('fa-eye');
      button.querySelector('i').classList.add('fa-eye-slash');
    }
  });
});
