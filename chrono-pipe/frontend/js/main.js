// API endpoints - Use relative URLs instead of absolute URLs
const API_BASE_URL = ''; // Empty string for relative URLs
const CAPTURE_ENDPOINT = `/capture`;
const SCREENSHOTS_ENDPOINT = `/screenshots`;
const QUERY_ENDPOINT = `/query`;

// DOM elements
const captureBtn = document.getElementById('capture-btn');
const screenshotNameInput = document.getElementById('screenshot-name');
const captureStatus = document.getElementById('capture-status');
const queryBtn = document.getElementById('query-btn');
const queryInput = document.getElementById('query-input');
const queryStatus = document.getElementById('query-status');
const explanation = document.getElementById('explanation');
const screenshotsContainer = document.getElementById('screenshots-container');
const gallery = document.getElementById('gallery');

// Event listeners
document.addEventListener('DOMContentLoaded', loadGallery);
captureBtn.addEventListener('click', captureScreenshot);
queryBtn.addEventListener('click', queryScreenshots);

// Capture screenshot
async function captureScreenshot() {
    try {
        const name = screenshotNameInput.value.trim() || 'Screenshot';
        
        captureStatus.textContent = 'Capturing screenshot...';
        captureStatus.className = 'status-message';
        
        const response = await fetch(CAPTURE_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            captureStatus.textContent = 'Screenshot captured successfully!';
            captureStatus.className = 'status-message success';
            screenshotNameInput.value = '';
            
            // Reload gallery to show new screenshot
            loadGallery();
        } else {
            throw new Error(data.error || 'Failed to capture screenshot');
        }
    } catch (error) {
        console.error('Error capturing screenshot:', error);
        captureStatus.textContent = `Error: ${error.message}`;
        captureStatus.className = 'status-message error';
    }
}

// Load screenshots gallery
async function loadGallery() {
    try {
        const response = await fetch(SCREENSHOTS_ENDPOINT);
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        
        const screenshots = await response.json();
        
        if (screenshots.length === 0) {
            gallery.innerHTML = '<p>No screenshots available. Capture some to get started!</p>';
            return;
        }
        
        // Sort screenshots by timestamp (newest first)
        screenshots.sort((a, b) => {
            return new Date(b.datetime) - new Date(a.datetime);
        });
        
        gallery.innerHTML = '';
        screenshots.forEach(screenshot => {
            const screenshotEl = createScreenshotElement(screenshot);
            gallery.appendChild(screenshotEl);
        });
    } catch (error) {
        console.error('Error loading gallery:', error);
        gallery.innerHTML = `<p class="error">Error loading screenshots: ${error.message}</p>`;
    }
}

// Query screenshots
async function queryScreenshots() {
    try {
        const query = queryInput.value.trim();
        
        if (!query) {
            queryStatus.textContent = 'Please enter a query';
            queryStatus.className = 'status-message error';
            return;
        }
        
        queryStatus.textContent = 'Searching...';
        queryStatus.className = 'status-message';
        explanation.textContent = '';
        screenshotsContainer.innerHTML = '';
        
        const response = await fetch(QUERY_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            queryStatus.textContent = 'Search completed!';
            queryStatus.className = 'status-message success';
            
            // Display results
            explanation.textContent = data.result.explanation;
            
            // Get all screenshots metadata for showing results
            const screenshotsResponse = await fetch(SCREENSHOTS_ENDPOINT);
            
            if (!screenshotsResponse.ok) {
                throw new Error(`Server returned ${screenshotsResponse.status}: ${screenshotsResponse.statusText}`);
            }
            
            const allScreenshots = await screenshotsResponse.json();
            
            // Find matching screenshots
            const relevantScreenshots = allScreenshots.filter(screenshot => 
                data.result.screenshots.includes(screenshot.filename)
            );
            
            if (relevantScreenshots.length === 0) {
                screenshotsContainer.innerHTML = '<p>No relevant screenshots found for your query.</p>';
                return;
            }
            
            screenshotsContainer.innerHTML = '';
            relevantScreenshots.forEach(screenshot => {
                const screenshotEl = createScreenshotElement(screenshot);
                screenshotsContainer.appendChild(screenshotEl);
            });
        } else {
            throw new Error(data.error || 'Failed to query screenshots');
        }
    } catch (error) {
        console.error('Error querying screenshots:', error);
        queryStatus.textContent = `Error: ${error.message}`;
        queryStatus.className = 'status-message error';
    }
}

// Create screenshot element
function createScreenshotElement(screenshot) {
    const div = document.createElement('div');
    div.className = 'screenshot-item';
    
    const img = document.createElement('img');
    img.className = 'screenshot-img';
    img.src = `/screenshots/${screenshot.filename}`; // Using relative URL
    img.alt = screenshot.name;
    
    const info = document.createElement('div');
    info.className = 'screenshot-info';
    
    const name = document.createElement('h3');
    name.textContent = screenshot.name;
    
    const datetime = document.createElement('p');
    datetime.textContent = new Date(screenshot.datetime).toLocaleString();
    
    info.appendChild(name);
    info.appendChild(datetime);
    div.appendChild(img);
    div.appendChild(info);
    
    return div;
}