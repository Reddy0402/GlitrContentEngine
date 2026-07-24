const form = document.getElementById('generatorForm');
const generateBtn = document.getElementById('generateBtn');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const jobIdElement = document.getElementById('jobId');
const jobStatusElement = document.getElementById('jobStatus');
const generatedPromptElement = document.getElementById('generatedPrompt');
const generatedImageElement = document.getElementById('generatedImage');
const imagePlaceholder = document.getElementById('imagePlaceholder');

let pollingInterval = null;

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    
    errorMessage.style.display = 'none';
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating...';
    
    try {
        // Include CSRF token for Django CSRF protection
        function getCookie(name) {
            const match = document.cookie.match(new RegExp('(^|; )' + name + '=([^;]+)'));
            return match ? decodeURIComponent(match[2]) : null;
        }

        const csrftoken = getCookie('csrftoken');

        const response = await fetch('/api/generate/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            },
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error('Failed to generate content');
        }

        const data = await response.json();
        const jobId = data.id;

        jobIdElement.textContent = jobId;
        jobStatusElement.textContent = 'Processing...';
        jobStatusElement.className = 'loading';
        generatedPromptElement.textContent = '—';
        generatedImageElement.style.display = 'none';
        imagePlaceholder.textContent = '—';
        imagePlaceholder.style.display = 'block';

        resultsSection.style.display = 'block';

        startPolling(jobId);

    } catch (error) {
        errorMessage.textContent = `Error: ${error.message}`;
        errorMessage.style.display = 'block';
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate';
    }
});

function startPolling(jobId) {
    pollingInterval = setInterval(() => {
        pollJobStatus(jobId);
    }, 2000);
}

async function pollJobStatus(jobId) {
    try {
        const response = await fetch(`/api/jobs/${jobId}/`);

        if (!response.ok) {
            throw new Error('Failed to fetch job status');
        }

        const data = await response.json();
        const status = data.status;

        jobStatusElement.textContent = status;

        if (status === 'Completed') {
            jobStatusElement.className = 'success';
            if (data.prompt) {
                generatedPromptElement.textContent = data.prompt;
            }
            if (data.image_url) {
                generatedImageElement.src = data.image_url;
                generatedImageElement.style.display = 'block';
                imagePlaceholder.style.display = 'none';
            }
            stopPolling();
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate';
        } else if (status === 'Failed') {
            jobStatusElement.className = 'failed';
            stopPolling();
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate';
            errorMessage.textContent = 'Job failed. Please try again.';
            errorMessage.style.display = 'block';
        }

    } catch (error) {
        errorMessage.textContent = `Polling error: ${error.message}`;
        errorMessage.style.display = 'block';
        stopPolling();
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate';
    }
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}
