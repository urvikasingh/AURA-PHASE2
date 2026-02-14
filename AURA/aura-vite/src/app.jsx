import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import { apiRequest } from "./services/api";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import HomePage from "./pages/HomePage";
import ChatbotPage from "./pages/Chatbot";
import PrivateRoute from "./components/PrivateRoute";

function App() {

  // ✅ FIX: validate token once on app startup
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    apiRequest("/auth/me").catch(() => {
      // Token exists but backend rejects it
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    });
  }, []);

  return (
    <Router>
      <Routes>
        {/* Public */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Domain selection */}
        <Route
          path="/homepage"
          element={
            <PrivateRoute>
              <HomePage />
            </PrivateRoute>
          }
        />

        {/* Chat */}
        <Route
          path="/chat"
          element={
            <PrivateRoute>
              <ChatbotPage />
            </PrivateRoute>
          }
        />

        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
    </Router>
  );
}

export default App;
