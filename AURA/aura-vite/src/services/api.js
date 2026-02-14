// src/services/api.js

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
    body:
      options.body && typeof options.body === "object"
        ? JSON.stringify(options.body)
        : options.body,
  });

  // ✅ FIX 1: handle auth desync FIRST
  if (response.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user"); // if you store it
    window.location.href = "/login";
    return;
  }

  // Existing error handling (keep this)
  if (!response.ok) {
    let errorMessage = "API request failed";
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {}
    throw new Error(errorMessage);
  }

  // Safe JSON handling
  const text = await response.text();
  return text ? JSON.parse(text) : null;
}
