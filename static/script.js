async function analyze() {
    const reviewsText = document.getElementById("reviewsInput").value;

    const reviewsArray = reviewsText.split("\n").filter(x => x.trim() !== "");

    const payload = { reviews: reviewsArray };

    const response = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
    document.getElementById("result").classList.remove("hidden");
}
