const API_URL = "https://website-wlvy.onrender.com";

async function uploadResume() {
    try {
        // Get the uploaded file from the input
        let fileInput = document.getElementById("resume");
        let file = fileInput.files[0];

        if (file) {
            // Log the details of the uploaded file (name and type)
            console.log("Uploading file:", file.name);
            console.log("File type:", file.type);

            // Prepare FormData for file upload
            let formData = new FormData();
            formData.append("resume", file);

            // Send POST request to the server
            let response = await fetch(`${API_URL}/upload_resume/`, {
                method: "POST",
                body: formData
            });

            // Check if the response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Parse the JSON response
            let result = await response.json();

            // Log the success response
            console.log("Resume uploaded successfully:", result);
        } else {
            console.log("No file selected.");
        }

    } catch (error) {
        // Log any error that occurred
        console.error("Error uploading resume:", error);
    }
}



async function fetchJobDescription() {
    let url = document.getElementById('job_url').value;
    let formData = new FormData();
    formData.append("url", url);

    try {
        let response = await fetch(`${API_URL}/fetch_job_description/`, {
            method: "POST",
            body: formData
        });

        console.log("Raw Response:", response);

        let data = await response.json();
        console.log("API Response:", data);

        if (response.ok && data.job_description) {
            localStorage.setItem("job_description", data.job_description);
            document.getElementById("job_description").innerText = data.job_description;
        } else {
            document.getElementById("job_description").innerText = `Error: ${data.detail || "Unknown error"}`;
        }
    } catch (error) {
        console.error("Fetch error:", error);
        document.getElementById("job_description").innerText = "Error fetching job description!";
    }
}


async function generateCoverLetter(resume, jobDescription) {
    try {
        const response = await fetch("https://your-render-url.onrender.com/generate_cover_letter/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ resume, job_description: jobDescription }),
        });

        console.log("Raw Response:", response);

        const data = await response.json();
        console.log("API Response:", data);

        if (response.ok && data.cover_letter) {
            localStorage.setItem("cover_letter", data.cover_letter);
            document.getElementById("cover_letter").innerText = data.cover_letter;
        } else {
            document.getElementById("cover_letter").innerText = `Error: ${data.detail || "Unknown error"}`;
        }
    } catch (error) {
        console.error("Fetch error:", error);
        document.getElementById("cover_letter").innerText = "Error generating cover letter!";
    }
}

