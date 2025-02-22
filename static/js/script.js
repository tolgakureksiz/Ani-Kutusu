const form = document.querySelector("form");
const fileInput = document.querySelector(".file-input");
const gallery = document.getElementById("gallery");
const uploadBox = document.getElementById("upload-box");
const append = document.getElementById("append");
const submitBtn = document.getElementById("submit-btn");
const descriptionInput = document.getElementById("description-box"); // ✅ Ensure this is defined

let selectedFile = null;

// Handle file selection
form.addEventListener("click", () => {
    fileInput.click();
});

// Make the function async
fileInput.onchange = async ({ target }) => {
    let file = target.files[0];

    if (file) {
        selectedFile = file;
        uploadBox.style.display = "none";

        const preDiv = document.createElement("div");
        preDiv.classList.add("pre-upload");
        const preImg = document.createElement("img");
        preImg.src = URL.createObjectURL(file);
        preDiv.appendChild(preImg);
        append.appendChild(preDiv);
    }
};

submitBtn.addEventListener("click", async () => {
    if (!selectedFile) {
        alert("Please select an image first.");
        return;
    }
    let descriptionText = descriptionInput.value.trim();
    console.log(descriptionText)

    let formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("description", descriptionText)
    try {
        let response = await fetch("/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed! Status: ${response.status}`);
        }

        console.log("Upload successful!", response);
    } catch (error) {
        console.error("Error:", error);
        return;
    }

    // Step 4: Display the uploaded image in the gallery
    let fileName = selectedFile.name;
    console.log(fileName);

    const imageDiv = document.createElement("div");
    imageDiv.classList.add("image-style");
    imageDiv.setAttribute("data-description", descriptionText)
    const img = document.createElement("img");
    img.src = URL.createObjectURL(selectedFile); // ✅ Fixed: Use selectedFile instead of file
    img.alt = fileName;
    imageDiv.appendChild(img);
    gallery.appendChild(imageDiv);

    // Apply Justified Gallery
    $(gallery).justifiedGallery('norewind').justifiedGallery({
        rowHeight: 300,
        margins: 10,
        lastRow: "nojustify",
        captions: false,
        border: 5
    });

    // 🔄 Delay the refresh to let the UI update first
    setTimeout(() => {
        window.location.reload();
    }, 1000);
});


