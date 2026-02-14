import React, { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { login } from "../services/auth.service";
import "./Login.css";
import { jwtDecode } from "jwt-decode";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // 🔒 If already logged in, redirect away from login
  const token = localStorage.getItem("token");
  if (token) {
    return <Navigate to="/homepage" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(email, password);

      // ✅ Save JWT token (single source of truth)
      localStorage.setItem("token", data.access_token);

      // (Optional) decode token if you need info later
      jwtDecode(data.access_token);

      // (Optional) store email for UI convenience
      localStorage.setItem("user", email);

      // ✅ Redirect and remove /login from history
      navigate("/homepage", { replace: true });
    } catch (err) {
      setError(err.message || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Login</h2>

        {error && <p className="error-text">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        <p>
          Don’t have an account?{" "}
          <span className="link" onClick={() => navigate("/signup")}>
            Sign up
          </span>
        </p>
      </form>
    </div>
  );
}

export default Login;
