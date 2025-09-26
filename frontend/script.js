const API_BASE = "http://127.0.0.1:8000";

// Load destinations from backend
async function loadDestinations() {
  try {
    const res = await fetch(`${API_BASE}/destinations`);
    const data = await res.json();
    const container = document.getElementById("destinations");
    container.innerHTML = "";
    data.forEach(dest => {
      const div = document.createElement("div");
      div.className = "destination";
      div.innerHTML = `<strong>${dest.name}</strong><br>${dest.description}`;
      container.appendChild(div);
    });
  } catch (error) {
    console.error("Error loading destinations:", error);
  }
}

// Handle booking form submission
document.getElementById("bookingForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const payload = Object.fromEntries(formData.entries());

  try {
    const res = await fetch(`${API_BASE}/bookings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errorData = await res.json();
      alert("Booking failed: " + JSON.stringify(errorData));
      return;
    }

    const result = await res.json();
    alert("Booking confirmed: " + JSON.stringify(result));
    e.target.reset();
  } catch (error) {
    console.error("Error submitting booking:", error);
    alert("Something went wrong. Please try again.");
  }
});

// Load destinations on page load
loadDestinations();