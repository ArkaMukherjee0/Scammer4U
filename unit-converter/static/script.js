// ── Form validation ───────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    // Convert form validation
    const convertForm = document.getElementById("convertForm");
    if (convertForm) {
        convertForm.addEventListener("submit", (e) => {
            const value = document.getElementById("value").value.trim();
            const fromUnit = document.getElementById("from_unit").value;
            const toUnit = document.getElementById("to_unit").value;

            if (!value || isNaN(Number(value))) {
                e.preventDefault();
                alert("Please enter a valid number.");
                return;
            }

            if (!fromUnit) {
                e.preventDefault();
                alert("Please select a 'From' unit.");
                return;
            }

            if (!toUnit) {
                e.preventDefault();
                alert("Please select a 'To' unit.");
                return;
            }
        });

        // Swap button
        const swapBtn = document.getElementById("swapBtn");
        if (swapBtn) {
            swapBtn.addEventListener("click", () => {
                const fromSelect = document.getElementById("from_unit");
                const toSelect = document.getElementById("to_unit");
                const temp = fromSelect.value;
                fromSelect.value = toSelect.value;
                toSelect.value = temp;
            });
        }
    }

    // Premium form validation
    const premiumForm = document.getElementById("premiumForm");
    if (premiumForm) {
        premiumForm.addEventListener("submit", (e) => {
            const apiKey = document.getElementById("api_key").value.trim();

            if (!apiKey) {
                e.preventDefault();
                alert("Please enter your API key.");
                return;
            }
        });
    }
});
