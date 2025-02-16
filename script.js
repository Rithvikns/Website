const API_URL = "https://website-wlvy.onrender.com";

async function uploadResume() {
    try {
        let formData = new FormData();
        formData.append("resume", document.getElementById("resume").files[0]);

        let response = await fetch(`${API_URL}/upload_resume/`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        let result = await response.json();
        console.log("Success:", result);
    } catch (error) {
        console.error("Fetch error:", error);
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
    const response = await fetch("https://your-render-url.onrender.com/generate_cover_letter/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ resume, job_description: jobDescription }),
    });

    const data = await response.json();
    console.log("Generated Cover Letter:", data.cover_letter);
}
