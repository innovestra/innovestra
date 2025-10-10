// Password toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Toggle for first password field
    const togglePassword1 = document.getElementById('togglePassword1');
    const password1 = document.getElementById('id_password1');
    const eyeIcon1 = document.getElementById('eyeIcon1');

    if (togglePassword1 && password1 && eyeIcon1) {
        togglePassword1.addEventListener('click', function() {
            // Toggle the type attribute
            const type = password1.getAttribute('type') === 'password' ? 'text' : 'password';
            password1.setAttribute('type', type);
            
            // Toggle the eye icon
            eyeIcon1.classList.toggle('fa-eye');
            eyeIcon1.classList.toggle('fa-eye-slash');
        });
    }

    // Toggle for second password field
    const togglePassword2 = document.getElementById('togglePassword2');
    const password2 = document.getElementById('id_password2');
    const eyeIcon2 = document.getElementById('eyeIcon2');

    if (togglePassword2 && password2 && eyeIcon2) {
        togglePassword2.addEventListener('click', function() {
            // Toggle the type attribute
            const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
            password2.setAttribute('type', type);
            
            // Toggle the eye icon
            eyeIcon2.classList.toggle('fa-eye');
            eyeIcon2.classList.toggle('fa-eye-slash');
        });
    }
});