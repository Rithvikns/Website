const API_URL = "https://website-wlvy.onrender.com";

async function uploadResume() {
    try {
        let fileInput = document.getElementById("resume");
        let file = fileInput.files[0];

        if (!file) {
            console.log("No file selected.");
            return;
        }

        console.log("Uploading file:", file.name);
        console.log("File type:", file.type);

        // Display the uploaded file as a preview (only if it's a PDF)
        if (file.type === "application/pdf") {
            let fileURL = URL.createObjectURL(file);
            document.getElementById("resumePreview").innerHTML = `
                <iframe src="${fileURL}" width="100%" height="500px"></iframe>
            `;
        }

    } catch (error) {
        console.error("Error displaying resume:", error);
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


async function generateCoverLetter() {
    let resumeInput = document.getElementById("resume");
    let file = resumeInput.files[0];

    if (!file) {
        console.log("No resume uploaded.");
        return;
    }

    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = async function () {
        let resumeData = reader.result.split(",")[1]; // Base64 encoding

        let jobDescription = document.getElementById("job_description").innerText;

        try {
            let response = await fetch("https://website-wlvy.onrender.com/generate_cover_letter/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ resume: resumeData, job_description: jobDescription }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            let data = await response.json();
            console.log("Generated Cover Letter:", data.cover_letter);
        } catch (error) {
            console.error("Error generating the cover letter:", error);
        }
    };
}

