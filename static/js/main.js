document.addEventListener('DOMContentLoaded', function() {
    // Theme Toggle
    const themeToggle = document.getElementById('themeToggle');
    
    if (themeToggle) {
        // Get saved theme or default to light
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);

        // Add click event listener
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            console.log('Theme switched to:', newTheme); // Debug log
        });
    } else {
        console.error('Theme toggle button not found!');
    }

    const thermalInput = document.getElementById('thermalFile');
    const rgbInput = document.getElementById('rgbFile');
    const thermalPreview = document.getElementById('thermalPreview');
    const rgbPreview = document.getElementById('rgbPreview');
    const submitBtn = document.getElementById('submitBtn');
    const uploadForm = document.getElementById('uploadForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');

    // Preview images when selected
    thermalInput.addEventListener('change', function(e) {
        handleFilePreview(e.target.files[0], thermalPreview);
        checkFormReady();
    });

    rgbInput.addEventListener('change', function(e) {
        handleFilePreview(e.target.files[0], rgbPreview);
        checkFormReady();
    });

    function handleFilePreview(file, previewContainer) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                previewContainer.classList.add('active');
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.innerHTML = '';
            previewContainer.classList.remove('active');
        }
    }

    function checkFormReady() {
        const thermalFile = thermalInput.files[0];
        const rgbFile = rgbInput.files[0];
        
        if (thermalFile && rgbFile) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const thermalFile = thermalInput.files[0];
        const rgbFile = rgbInput.files[0];

        if (!thermalFile || !rgbFile) {
            showError('Please select both thermal and RGB images.');
            return;
        }

        // Hide previous messages
        hideMessages();

        // Show loading state
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').style.display = 'none';
        submitBtn.querySelector('.btn-loader').style.display = 'inline-flex';

        // Create FormData
        const formData = new FormData();
        formData.append('thermal', thermalFile);
        formData.append('rgb', rgbFile);

        try {
            const response = await fetch('/align', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // Check if response is an image file
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('image')) {
                    // Download the aligned image
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'aligned_AT.JPG';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    showSuccess('Image processed successfully! Your aligned thermal image download should start shortly.');
                } else {
                    // Try to parse as JSON for error messages
                    const data = await response.json();
                    if (data.error) {
                        showError(data.error);
                    } else {
                        showError('Unexpected response format.');
                    }
                }
            } else {
                // Try to get error message from response
                try {
                    const data = await response.json();
                    showError(data.error || `Server error: ${response.status}`);
                } catch {
                    showError(`Server error: ${response.status} ${response.statusText}`);
                }
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            // Reset button state
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').style.display = 'inline';
            submitBtn.querySelector('.btn-loader').style.display = 'none';
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
    }

    function showSuccess(message) {
        successMessage.textContent = message;
        successMessage.style.display = 'block';
        errorMessage.style.display = 'none';
    }

    function hideMessages() {
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';
    }
});

