async function uploadResume() {
    let file = document.getElementById('resume').files[0];
    let formData = new FormData();
    formData.append("file", file);

    let response = await fetch("https://your-api-url.onrender.com/upload_resume/", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    localStorage.setItem("resume_text", data.resume_text);
}

async function fetchJobDescription() {
    let url = document.getElementById('job_url').value;
    let formData = new FormData();
    formData.append("url", url);

    let response = await fetch("https://your-api-url.onrender.com/fetch_job_description/", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    localStorage.setItem("job_description", data.job_description);
}

async function generateCoverLetter() {
    let resume_text = localStorage.getItem("resume_text");
    let job_description = localStorage.getItem("job_description");

    let response = await fetch("https://your-api-url.onrender.com/generate_cover_letter/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text, job_description })
    });

    let data = await response.json();
    document.getElementById("cover_letter").innerText = data.cover_letter;
}
