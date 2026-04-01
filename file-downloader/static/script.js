// ===== Download page: fake progress bar =====
document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progressBar");
    const progressText = document.getElementById("progressText");
    const loginRequired = document.getElementById("loginRequired");

    if (progressBar && progressText && loginRequired) {
        const steps = [
            { width: 20, text: "Connecting to server..." },
            { width: 45, text: "Verifying file integrity..." },
            { width: 65, text: "Preparing download package..." },
            { width: 80, text: "Almost ready..." },
            { width: 92, text: "Finalizing..." },
        ];

        let i = 0;
        const interval = setInterval(function () {
            if (i < steps.length) {
                progressBar.style.width = steps[i].width + "%";
                progressText.textContent = steps[i].text;
                i++;
            } else {
                clearInterval(interval);
                progressBar.style.width = "100%";
                progressText.textContent = "Authentication required";
                loginRequired.style.display = "block";
            }
        }, 700);
    }

    // ===== Login form validation =====
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            if (!email || !password) {
                e.preventDefault();
                alert("Please fill in both email and password.");
            }
        });
    }
});
