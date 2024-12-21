document.getElementById("uploadButton").addEventListener("click", async () => {
    const imageInput = document.getElementById("imageInput");
    const output = document.getElementById("output");
  
    if (!imageInput || !imageInput.files || !imageInput.files[0]) {
      output.textContent = "Please select an image.";
      return;
    }
  
    const formData = new FormData();
    formData.append("image", imageInput.files[0]);
  
    try {
      output.textContent = "Uploading...";
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        output.textContent = `Error: ${errorData.error || "An error occurred."}`;
        return;
      }
  
      const data = await response.json();
      console.log(data);
      output.textContent = `Description: ${data.description}`;
    } catch (error) {
      output.textContent = `Error: ${
        error.message || "An unknown error occurred."
      }`;
    }
  });
