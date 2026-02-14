document.addEventListener('DOMContentLoaded', () => {
    const statusText = document.getElementById('status-text');
    const statusDot = document.querySelector('.status-dot');
    const detectionList = document.getElementById('detection-list');

    // Polling interval for status and detections
    const POLL_INTERVAL = 500; // ms

    async function fetchStatus() {
        try {
            const response = await fetch('/api/status');
            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            updateUI(data);

            // Connected state
            statusText.textContent = data.status || "Connected";
            statusDot.classList.add('active');
            statusDot.classList.remove('error');

        } catch (error) {
            console.error('Error fetching status:', error);
            statusText.textContent = "Disconnected";
            statusDot.classList.remove('active');
            statusDot.classList.add('error');
        }
    }

    function updateUI(data) {
        // Update Detections
        const detections = data.detections || [];
        detectionList.innerHTML = ''; // Clear current

        if (detections.length === 0) {
            detectionList.innerHTML = '<li class="placeholder" style="color:#666; padding:10px;">No objects detected</li>';
        } else {
            detections.forEach(det => {
                const li = document.createElement('li');
                li.className = 'detection-item';

                const labelSpan = document.createElement('span');
                labelSpan.className = 'detection-label';
                labelSpan.textContent = det.label;

                if (det.is_dangerous) {
                    const dangerTag = document.createElement('span');
                    dangerTag.className = 'tag-dangerous';
                    dangerTag.textContent = 'DANGER';
                    labelSpan.appendChild(dangerTag);
                }

                const confSpan = document.createElement('span');
                confSpan.className = 'detection-conf';
                confSpan.textContent = `${(det.confidence * 100).toFixed(0)}%`;

                li.appendChild(labelSpan);
                li.appendChild(confSpan);
                detectionList.appendChild(li);
            });
        }
    }

    // Start polling
    setInterval(fetchStatus, POLL_INTERVAL);
});
