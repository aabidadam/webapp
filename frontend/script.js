document.getElementById('uploadButton').addEventListener('click', async () => {
    const imageInput = document.getElementById('imageInput');
    const output = document.getElementById('output');

    if (!imageInput.files[0]) {
        output.textContent = "Please select an image.";
        return;
    }

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    try {
        output.textContent = "Uploading...";
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();

        if (response.ok) {
            output.textContent = `Description: ${data.description}`;
        } else {
            output.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
    }
});
