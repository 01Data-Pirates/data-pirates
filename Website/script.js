document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewImage = document.getElementById('previewImage');
    const uploadPrompt = document.getElementById('uploadPrompt');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultArea = document.getElementById('resultArea');
    const predictionResult = document.getElementById('predictionResult');

    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            let ripple = document.createElement('div');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            let rect = this.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;
            
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            setTimeout(() => {
                ripple.remove();
            }, 1000);
        });
    });

    // Handle drag and drop with animations
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        uploadArea.classList.add('border-primary');
        uploadArea.style.transform = 'scale(1.02)';
    }

    function unhighlight() {
        uploadArea.classList.remove('border-primary');
        uploadArea.style.transform = 'scale(1)';
    }

    // Handle file drop with animation
    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // Handle file input change
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Fade out upload prompt
                    uploadPrompt.style.opacity = '0';
                    setTimeout(() => {
                        uploadPrompt.classList.add('hide');
                        // Fade in preview image
                        previewImage.src = e.target.result;
                        previewImage.classList.add('show');
                        // Enable analyze button with animation
                        analyzeBtn.disabled = false;
                        analyzeBtn.style.transform = 'scale(1.05)';
                        setTimeout(() => {
                            analyzeBtn.style.transform = 'scale(1)';
                        }, 200);
                    }, 300);
                }
                
                reader.readAsDataURL(file);
            } else {
                showError('Please upload an image file.');
            }
        }
    }

    // Show error message with animation
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        uploadArea.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            errorDiv.classList.remove('show');
            setTimeout(() => {
                errorDiv.remove();
            }, 300);
        }, 3000);
    }

    // Handle analyze button click with animations
    analyzeBtn.addEventListener('click', async function() {
        // Show loading state with animation
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
        analyzeBtn.classList.add('loading');

        // TODO: Replace this with actual API call to your ML model
        setTimeout(() => {
            // Show result area with animation
            resultArea.style.display = 'block';
            setTimeout(() => {
                resultArea.classList.add('show');
            }, 10);
            
            predictionResult.textContent = 'Sample prediction: This image shows potential signs of [Disease Name]. Please consult a dermatologist for proper diagnosis.';
            
            // Reset button state with animation
            analyzeBtn.classList.remove('loading');
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze Image';
            
            // Scroll to result
            resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 2000);
    });
}); 