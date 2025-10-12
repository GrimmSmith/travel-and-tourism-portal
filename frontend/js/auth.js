const API_BASE = "http://127.0.0.1:8000/api";

// Handle registration
document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const payload = Object.fromEntries(formData.entries());

  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await res.json();

    if (!res.ok) {
      alert("Registration failed: " + (result.detail || JSON.stringify(result)));
      return;
    }

    alert("✅ Registration successful! You can now log in.");
    e.target.reset();
  } catch (error) {
    console.error("Error during registration:", error);
    alert("Something went wrong. Please try again.");
  }
});

// Handle login
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const payload = Object.fromEntries(formData.entries());

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await res.json();

    if (!res.ok || !result.access_token) {
      alert("Login failed: " + (result.detail || JSON.stringify(result)));
      return;
    }

    // Store token in localStorage
    localStorage.setItem("token", result.access_token);
    alert("✅ Login successful!");

    // Redirect to booking page
    window.location.href = "index.html";
  } catch (error) {
    console.error("Error during login:", error);
    alert("Something went wrong. Please try again.");
  }
});