    // Get the video element
    const videoElement = document.getElementById('camera-preview');

    // Check if the browser supports accessing the camera
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Access the camera
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                // Set the video source to the camera stream
                videoElement.srcObject = stream;
            })
            .catch(function (error) {
                console.error('Error accessing the camera:', error);
            });
    } else {
        console.error('Camera access is not supported in this browser.');
    }