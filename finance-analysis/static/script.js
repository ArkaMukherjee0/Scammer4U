// FinanceInsight — Client-side validation

document.addEventListener("DOMContentLoaded", function () {

    // Prevent empty financial data submission
    const analyzeForm = document.getElementById("analyzeForm");
    if (analyzeForm) {
        analyzeForm.addEventListener("submit", function (e) {
            const textarea = document.getElementById("text");
            if (!textarea.value.trim()) {
                e.preventDefault();
                textarea.style.borderColor = "#ef4444";
                textarea.setAttribute("placeholder", "Please paste your financial data before analyzing.");
                textarea.focus();
                setTimeout(() => {
                    textarea.style.borderColor = "";
                }, 2000);
            }
        });
    }

    // Prevent empty API key submission
    const premiumForm = document.getElementById("premiumForm");
    if (premiumForm) {
        premiumForm.addEventListener("submit", function (e) {
            const apiKeyInput = document.getElementById("api_key");
            if (!apiKeyInput.value.trim()) {
                e.preventDefault();
                apiKeyInput.style.borderColor = "#ef4444";
                apiKeyInput.setAttribute("placeholder", "API Key is required");
                apiKeyInput.focus();
                setTimeout(() => {
                    apiKeyInput.style.borderColor = "";
                }, 2000);
            }
        });
    }

});
