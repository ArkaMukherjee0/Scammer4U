// Character counter for textarea
document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('textInput');
    const charCount = document.getElementById('charCount');

    if (textInput) {
        // Update character count on input
        textInput.addEventListener('input', function() {
            if (charCount) {
                charCount.textContent = textInput.value.length;
            }
        });

        // Form validation
        const checkForm = document.getElementById('checkForm');
        if (checkForm) {
            checkForm.addEventListener('submit', function(e) {
                const text = textInput.value.trim();
                if (!text) {
                    e.preventDefault();
                    alert('Please enter some text to check for plagiarism');
                    return false;
                }
                if (text.length < 10) {
                    e.preventDefault();
                    alert('Please enter at least 10 characters');
                    return false;
                }
            });
        }
    }

    // Login form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email) {
                e.preventDefault();
                alert('Please enter your email address');
                return false;
            }

            if (!password) {
                e.preventDefault();
                alert('Please enter your password');
                return false;
            }

            // Basic email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                alert('Please enter a valid email address');
                return false;
            }

            if (password.length < 6) {
                e.preventDefault();
                alert('Password must be at least 6 characters');
                return false;
            }
        });
    }
});
