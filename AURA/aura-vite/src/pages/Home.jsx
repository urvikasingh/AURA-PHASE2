import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar.jsx";
import LiquidEther from "../react-comp/LiquidEther.jsx";
import "../App.css";

function Home() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    const token = localStorage.getItem("token"); // ✅ FIXED

    if (token) {
      navigate("/homepage");
    } else {
      navigate("/signup");
    }
  };

  return (
    <div className="hero">
      {/* Background */}
      <div className="liquid-wrapper">
        <LiquidEther
          colors={["#5227FF", "#FF9FFC", "#B19EEF"]}
          mouseForce={20}
          cursorSize={100}
          isViscous={false}
          viscous={30}
          iterationsViscous={32}
          iterationsPoisson={32}
          resolution={0.5}
          isBounce={false}
          autoDemo={true}
          autoSpeed={0.5}
          autoIntensity={2.2}
          takeoverDuration={0.25}
          autoResumeDelay={3000}
          autoRampDuration={0.6}
          style={{ background: "transparent" }}
        />
      </div>

      {/* Navbar */}
      <Navbar />
      <div className="navbar-placeholder" />

      {/* HERO CONTENT */}
      <div className="hero-content">
        <h1 className="hero-title">
          Build, Learn, and Reason <br /> with <span>AURA</span>
        </h1>

        <p className="hero-subtitle">
          A multi-domain AI assistant designed for deep thinking,
          structured learning, and intelligent exploration.
        </p>

        <button className="start-btn" onClick={handleGetStarted}>
          Get Started
        </button>
      </div>
    </div>
  );
}

export default Home;
