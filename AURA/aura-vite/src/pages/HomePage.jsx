import { useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();
  const user = localStorage.getItem("user");

  const displayName = user
    ? user.split("@")[0]
    : "there";

  const goToChat = (domain) => {
    // ✅ CLEAR active conversation for this domain
    localStorage.removeItem(`aura_active_conversation_${domain}`);

    navigate(`/chat?domain=${domain}`);
  };

  return (
    <div className="homepage homepage-bg">
      <div className="homepage-content homepage-center">
        {/* Heading */}
        <h1 className="homepage-title">
          Welcome, <span>{displayName}</span>
        </h1>

        <p className="homepage-subtitle">
          Choose a domain to begin your conversation with AURA
        </p>

        {/* Domain cards */}
        <div className="box-grid box-grid-center">
          <div
            className="page-box"
            onClick={() => goToChat("usp")}
          >
            <h3>ME-AI</h3>
            <p>
              General-purpose reasoning, exploration,
              and intelligent problem-solving.
            </p>
          </div>

          <div
            className="page-box"
            onClick={() => goToChat("academic")}
          >
            <h3>ACADM-AI</h3>
            <p>
              Structured explanations designed for learning,
              exams, and conceptual clarity.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
