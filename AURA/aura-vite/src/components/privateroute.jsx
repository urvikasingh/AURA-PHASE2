import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { apiRequest } from "../services/api";

function PrivateRoute({ children }) {
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setAuthorized(false);
      setLoading(false);
      return;
    }

    // ✅ Validate token using a protected endpoint
    apiRequest("/conversations?domain=usp")
      .then(() => {
        setAuthorized(true);
      })
      .catch(() => {
        // ❌ Token expired / invalid
        localStorage.removeItem("token");
        setAuthorized(false);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return null; // or a loader

  if (!authorized) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default PrivateRoute;
