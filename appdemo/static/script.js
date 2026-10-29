const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture');
const predictionDiv = document.getElementById('prediction');

// Get webcam stream
navigator.mediaDevices.getUserMedia({ video: { width: 224, height: 224 } })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        predictionDiv.textContent = 'Error accessing webcam: ' + err;
    });

captureBtn.onclick = async function() {
    // Draw current frame to canvas
    canvas.getContext('2d').drawImage(video, 0, 0, 224, 224);
    canvas.toBlob(async function(blob) {
        const formData = new FormData();
        formData.append('image', blob, 'capture.jpg');
        predictionDiv.textContent = 'Predicting...';
        try {
            const res = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.class) {
                predictionDiv.textContent = `Prediction: ${data.class} (नेपाली: ${data.nepali_name})\nConfidence: ${(data.confidence*100).toFixed(2)}%`;
            } else {
                predictionDiv.textContent = 'Error: ' + (data.error || 'Unknown error');
            }
        } catch (e) {
            predictionDiv.textContent = 'Prediction failed: ' + e;
        }
    }, 'image/jpeg');
}; 