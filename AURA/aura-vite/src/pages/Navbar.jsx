import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Navbar() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const token = localStorage.getItem("token");
  const userEmail = localStorage.getItem("user");

  const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  navigate("/", { replace: true });
};



  // Derive a clean display name
  const displayName = userEmail
    ? userEmail.split("@")[0]
    : "User";

  return (
    <nav className="navbar">
      {/* Left: Brand */}
      <div className="navbar-left" onClick={() => navigate("/")}>
        AURA
      </div>

      {/* Right: Auth section */}
      <div className="navbar-right">
        {!token ? (
          <button className="nav-btn" onClick={() => navigate("/login")}>
            Sign In
          </button>
        ) : (
          <div className="account-wrapper">
            <button
              className="account-btn"
              onClick={() => setOpen((v) => !v)}
            >
              {displayName}
            </button>

            {open && (
              <div className="account-dropdown">
                <div className="account-email">
                  {userEmail}
                </div>
                <button onClick={handleLogout}>Logout</button>
              </div>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
