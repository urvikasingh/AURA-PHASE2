// src/services/auth.service.js

const API_BASE = "http://127.0.0.1:8000/auth";

async function handleResponse(response) {
  const data = await response.json();

  if (!response.ok) {
    const error = new Error(data.detail || "Request failed");
    error.status = response.status;
    throw error;
  }

  return data;
}

export async function signup(email, password) {
  const response = await fetch(`${API_BASE}/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  return handleResponse(response);
}

export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email); // OAuth2 expects "username"
  formData.append("password", password);

  const response = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Login failed");
  }

  return response.json();
}

