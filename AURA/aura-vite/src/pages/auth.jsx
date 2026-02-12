// src/pages/auth.jsx

export const isLoggedIn = () => {
  const token = localStorage.getItem("access_token");
  return !!token; // true only if token exists
};

export const logout = () => {
  localStorage.removeItem("access_token");
};
