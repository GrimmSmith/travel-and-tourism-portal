// frontend/js/main.js
const DEFAULT_API_BASE = `${window.location.origin}/api`;
const API_BASE = (window.API_BASE || DEFAULT_API_BASE);
const TIMEOUT_MS = 10000;

function getToken() {
  return localStorage.getItem("token");
}

function redirectToLogin() {
  const loginPage = "auth.html";
  window.location.href = loginPage;
}

function escapeHtml(text) {
  if (!text) return "";
  return String(text).replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
}

async function fetchWithTimeout(url, opts = {}, timeout = TIMEOUT_MS) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  try {
    const res = await fetch(url, { signal: controller.signal, ...opts });
    clearTimeout(id);
    return res;
  } catch (err) {
    clearTimeout(id);
    throw err;
  }
}

function showStatus(text, el = null, color = "#0b7285") {
  if (el) {
    el.textContent = text;
    el.style.color = color;
  } else {
    console.info(text);
  }
}

/* Auth check */
const token = getToken();
if (!token) {
  alert("Please log in to access this page.");
  redirectToLogin();
}

/* Optional user badge in heading */
const userEmailStored = localStorage.getItem("user_email");
if (userEmailStored) {
  const heading = document.querySelector("h1");
  if (heading) heading.innerHTML += ` <span style="font-size:0.8rem;color:#555">(Logged in as ${escapeHtml(userEmailStored)})</span>`;
}

/* Logout handler */
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    try {
      await fetchWithTimeout(`${API_BASE}/auth/logout`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` }
      });
    } catch (e) {
      console.warn("Logout request failed, clearing local session anyway");
    } finally {
      localStorage.removeItem("token");
      localStorage.removeItem("user_email");
      alert("You have been logged out.");
      redirectToLogin();
    }
  });
}

/* Load and render destinations */
async function loadDestinations() {
  const container = document.getElementById("destinations");
  if (!container) return;
  container.innerHTML = "<p>Loading destinations...</p>";

  try {
    const res = await fetchWithTimeout(`${API_BASE}/destinations`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) throw new Error("Failed to fetch destinations");
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = "<p class='muted'>No destinations available yet.</p>";
      return;
    }

    container.innerHTML = "";
    data.forEach(dest => {
      const div = document.createElement("div");
      div.className = "destination";
      const imageUrl = dest.image ? `/static/hotel_img/${encodeURIComponent(dest.image)}` : "";
      div.innerHTML = `
        <div style="display:flex;gap:12px;align-items:flex-start">
          ${imageUrl ? `<img src="${imageUrl}" alt="${escapeHtml(dest.name)}" style="width:120px;height:80px;object-fit:cover;border-radius:6px">` : ""}
          <div>
            <strong>${escapeHtml(dest.name)}</strong>
            <div style="color:#666;margin-top:6px">${escapeHtml(dest.short_description || dest.description || "")}</div>
            <div style="margin-top:8px">
              <a href="/destination/${dest.id}">View</a>
              &nbsp;|&nbsp;
              <a href="/book?dest=${dest.id}">Book</a>
            </div>
          </div>
        </div>
      `;
      container.appendChild(div);
    });

    // If booking form has a destination select, populate it
    const destSelect = document.getElementById("destination_id");
    if (destSelect) {
      destSelect.innerHTML = '<option value="">Select destination</option>' + data.map(d => `<option value="${d.id}">${escapeHtml(d.name)}</option>`).join("");
    }
  } catch (error) {
    console.error("Error loading destinations:", error);
    container.innerHTML = "<p>Unable to load destinations. Please try again later.</p>";
  }
}

/* Auto-fill current user info into available fields */
async function autofillUser() {
  const nameInput = document.getElementById("user_name");
  const emailInput = document.getElementById("user_email");
  const userIdInput = document.querySelector("input[name='user_id']");
  try {
    const res = await fetchWithTimeout(`${API_BASE}/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) return;
    const user = await res.json();
    if (nameInput) nameInput.value = user.name || "";
    if (emailInput) emailInput.value = user.email || "";
    if (userIdInput && user.id) userIdInput.value = String(user.id);
    if (user && user.email) localStorage.setItem("user_email", user.email);
  } catch (err) {
    console.warn("Autofill failed", err);
  }
}

/* Date validation */
function validateDates(from, to) {
  const f = new Date(from);
  const t = new Date(to);
  const today = new Date();
  today.setHours(0,0,0,0);
  if (isNaN(f.valueOf()) || isNaN(t.valueOf())) return "Please provide valid dates.";
  if (f < today) return "Start date cannot be in the past.";
  if (t < f) return "End date cannot be before start date.";
  return null;
}

/* Booking submission */
const bookingForm = document.getElementById("bookingForm");
if (bookingForm) {
  bookingForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const statusEl = document.getElementById("formStatus");
    showStatus("", statusEl);

    const formData = new FormData(bookingForm);
    // Build payload adapting to present fields
    const payload = {};
    if (formData.get("user_id")) payload.user_id = Number(formData.get("user_id"));
    if (formData.get("destination_id")) payload.destination_id = Number(formData.get("destination_id"));
    if (formData.get("date_from")) payload.date_from = formData.get("date_from");
    if (formData.get("date_to")) payload.date_to = formData.get("date_to");
    if (formData.get("guests")) payload.guests = Number(formData.get("guests"));

    // Basic required checks
    if (!payload.destination_id || !payload.date_from || !payload.date_to || !payload.guests) {
      showStatus("Please fill in all required fields.", statusEl, "#b91c1c");
      return;
    }

    const dateErr = validateDates(payload.date_from, payload.date_to);
    if (dateErr) {
      showStatus(dateErr, statusEl, "#b91c1c");
      return;
    }

    // Disable submit while processing
    const submitBtn = bookingForm.querySelector("button[type='submit']");
    if (submitBtn) submitBtn.disabled = true;

    try {
      const res = await fetchWithTimeout(`${API_BASE}/bookings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      let result;
      try { result = await res.json(); } catch { result = null; }

      if (!res.ok) {
        const msg = result && (result.detail || result.message) ? (result.detail || result.message) : res.statusText;
        showStatus("Booking failed: " + msg, statusEl, "#b91c1c");
        return;
      }

      showStatus("✅ Booking confirmed. ID: " + (result && result.id ? result.id : "N/A"), statusEl, "#0b7285");
      bookingForm.reset();
      await loadDestinations();
    } catch (err) {
      console.error("Error submitting booking:", err);
      showStatus("Something went wrong. Please try again.", statusEl, "#b91c1c");
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });
}

/* Initialize */
document.addEventListener("DOMContentLoaded", () => {
  loadDestinations();
  autofillUser();
});