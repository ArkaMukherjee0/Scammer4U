/**
 * Tech Insights Blog — Client-side logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // ── Form validation ──
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");

    loginForm.addEventListener("submit", (e) => {
      let valid = true;

      // Reset errors
      emailError.style.display = "none";
      passwordError.style.display = "none";
      emailInput.style.borderColor = "";
      passwordInput.style.borderColor = "";

      if (!emailInput.value.trim()) {
        emailError.textContent = "Please enter your email address";
        emailError.style.display = "block";
        emailInput.style.borderColor = "#f87171";
        valid = false;
      }

      if (!passwordInput.value.trim()) {
        passwordError.textContent = "Please enter your password";
        passwordError.style.display = "block";
        passwordInput.style.borderColor = "#f87171";
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
      }
    });

    // Clear error on input
    [emailInput, passwordInput].forEach((input) => {
      input.addEventListener("input", () => {
        input.style.borderColor = "";
        const errorEl = document.getElementById(input.id + "-error");
        if (errorEl) errorEl.style.display = "none";
      });
    });
  }
});
