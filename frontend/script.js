const API_BASE = "http://127.0.0.1:8000/api";

// Load destinations from backend
async function loadDestinations() {
  const container = document.getElementById("destinations");
  container.innerHTML = "<p>Loading destinations...</p>";

  try {
    const res = await fetch(`${API_BASE}/destinations`);
    if (!res.ok) throw new Error("Failed to fetch destinations");

    const data = await res.json();
    container.innerHTML = "";

    data.forEach(dest => {
      const div = document.createElement("div");
      div.className = "destination";
      div.innerHTML = `<strong>${dest.name}</strong><br>${dest.description}`;
      container.appendChild(div);
    });
  } catch (error) {
    console.error("Error loading destinations:", error);
    container.innerHTML = "<p>Unable to load destinations. Please try again later.</p>";
  }
}

// Handle booking form submission
document.getElementById("bookingForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const payload = Object.fromEntries(formData.entries());

  // Basic validation
  if (!payload.user_id || !payload.destination_id || !payload.date_from || !payload.date_to || !payload.guests) {
    alert("Please fill in all fields before submitting.");
    return;
  }

  const token = localStorage.getItem("token");
  if (!token) {
    alert("You must be logged in to book a trip.");
    window.location.href = "auth.html";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/bookings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    const result = await res.json();

    if (!res.ok) {
      alert("Booking failed: " + (result.detail || JSON.stringify(result)));
      return;
    }

    alert("✅ Booking confirmed!\nID: " + result.id + "\nStatus: " + result.status);
    e.target.reset();
  } catch (error) {
    console.error("Error submitting booking:", error);
    alert("Something went wrong. Please try again.");
  }
});

// Initialize page
loadDestinations();