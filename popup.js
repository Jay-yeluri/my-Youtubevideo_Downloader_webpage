document.getElementById('downloadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    const videoLink = document.getElementById('videoLink').value;
    formData.append('link', videoLink);

    try {
        const response = await fetch('http://127.0.0.1:8000/download', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob(); 
            const url = window.URL.createObjectURL(blob); 
            const a = document.createElement('a');
            a.href = url; 
            a.download = 'sample.mp4';
            document.body.appendChild(a);
            a.click(); 
            a.remove();
            window.URL.revokeObjectURL(url);
            document.getElementById('statusMessage').innerText = 'Download started!';
        } else {
            const result = await response.json();
            document.getElementById('statusMessage').innerText = result.detail || 'Error occurred.';
        }
    } catch (error) {
        document.getElementById('statusMessage').innerText = 'An error occurred during the download.';
    }
});
