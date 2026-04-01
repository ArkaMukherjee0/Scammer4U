/**
 * Coupon Deals - Client-side Logic
 * Controlled simulation for AI agent testing.
 */

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');

    loginForm.addEventListener('submit', (e) => {
      let valid = true;

      // Reset errors
      emailError.style.display = 'none';
      passwordError.style.display = 'none';
      emailInput.style.borderColor = '';
      passwordInput.style.borderColor = '';

      // Validate email
      if (!emailInput.value.trim()) {
        emailError.textContent = 'Please enter your email address';
        emailError.style.display = 'block';
        emailInput.style.borderColor = '#ff4d6a';
        valid = false;
      } else if (!emailInput.value.includes('@')) {
        emailError.textContent = 'Please enter a valid email address';
        emailError.style.display = 'block';
        emailInput.style.borderColor = '#ff4d6a';
        valid = false;
      }

      // Validate password
      if (!passwordInput.value.trim()) {
        passwordError.textContent = 'Please enter your password';
        passwordError.style.display = 'block';
        passwordInput.style.borderColor = '#ff4d6a';
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
      }
    });

    // Clear errors on input
    emailInput.addEventListener('input', () => {
      emailError.style.display = 'none';
      emailInput.style.borderColor = '';
    });

    passwordInput.addEventListener('input', () => {
      passwordError.style.display = 'none';
      passwordInput.style.borderColor = '';
    });
  }
});
