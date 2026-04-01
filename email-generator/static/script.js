/**
 * MailCraft AI — Client-side Validation
 * Prevents empty form submissions on homepage & login pages.
 */

document.addEventListener("DOMContentLoaded", () => {
    // === Email Generator Form ===
    const emailForm = document.getElementById("email-form");
    if (emailForm) {
        emailForm.addEventListener("submit", (e) => {
            const emailType = document.getElementById("email_type").value;
            const recipient = document.getElementById("recipient").value.trim();
            const description = document.getElementById("description").value.trim();

            if (!emailType || !recipient || !description) {
                e.preventDefault();
                showToast("Please fill in all fields before generating.");
                return;
            }
        });

        // Add focus animations
        emailForm.querySelectorAll("input, select, textarea").forEach((el) => {
            el.addEventListener("focus", () => {
                el.closest(".form-group").classList.add("focused");
            });
            el.addEventListener("blur", () => {
                el.closest(".form-group").classList.remove("focused");
            });
        });
    }

    // === Login Form ===
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            if (!email || !password) {
                e.preventDefault();
                showToast("Please enter both email and password.");
                return;
            }
        });

        loginForm.querySelectorAll("input").forEach((el) => {
            el.addEventListener("focus", () => {
                el.closest(".form-group").classList.add("focused");
            });
            el.addEventListener("blur", () => {
                el.closest(".form-group").classList.remove("focused");
            });
        });
    }
});

/**
 * Simple toast notification
 */
function showToast(message) {
    // Remove existing toast
    const existing = document.querySelector(".toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;

    Object.assign(toast.style, {
        position: "fixed",
        bottom: "28px",
        left: "50%",
        transform: "translateX(-50%) translateY(20px)",
        background: "linear-gradient(135deg, #ef4444, #dc2626)",
        color: "#fff",
        padding: "12px 24px",
        borderRadius: "10px",
        fontSize: "0.88rem",
        fontWeight: "600",
        fontFamily: "'Inter', sans-serif",
        boxShadow: "0 8px 24px rgba(239, 68, 68, 0.3)",
        zIndex: "9999",
        opacity: "0",
        transition: "all 0.35s cubic-bezier(0.4, 0, 0.2, 1)",
    });

    document.body.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateX(-50%) translateY(0)";
    });

    // Auto-remove
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(-50%) translateY(20px)";
        setTimeout(() => toast.remove(), 350);
    }, 3000);
}
