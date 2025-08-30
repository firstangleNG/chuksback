document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("scanner");
    const scanResult = document.getElementById("scan-result");
    const startScanButton = document.getElementById("start-scan");
    let stream;

    async function startScanner() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
            video.srcObject = stream;
            scanResult.textContent = "Scanning...";
        } catch (error) {
            scanResult.textContent = "Error accessing camera: " + error.message;
        }
    }

    function stopScanner() {
        if (stream) {
            let tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
        }
    }

    startScanButton.addEventListener("click", () => {
        if (stream) {
            stopScanner();
            scanResult.textContent = "Scan a barcode or QR code";
        } else {
            startScanner();
        }
    });

    // Mock barcode detection (Replace this with actual barcode scanning library like QuaggaJS)
    video.addEventListener("click", function () {
        let mockBarcode = "123456789"; // Simulated barcode
        fetch(`/scan-barcode/?barcode=${mockBarcode}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    scanResult.textContent = `Item: ${data.data.part_name}, Stock: ${data.data.quantity_available}`;
                } else {
                    scanResult.textContent = "Item not found";
                }
            })
            .catch(error => {
                scanResult.textContent = "Error scanning barcode";
            });
    });
});