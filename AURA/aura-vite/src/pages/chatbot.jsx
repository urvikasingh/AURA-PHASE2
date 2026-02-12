import { useState, useEffect, useRef } from "react";
import Navbar from "./Navbar.jsx";
import FloatingLines from "../react-comp/FloatingLines.jsx";
import "./chatbot.css";
import { apiRequest } from "../services/api";

export default function ChatbotPage() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hello. How can I assist you?" },
  ]);
  const [input, setInput] = useState("");
  const [domain, setDomain] = useState("usp");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);
    setInput("");

    try {
      const data = await apiRequest("/chat", {
        method: "POST",
        body: JSON.stringify({
          domain,
          message: userMessage,
        }),
      });

      setMessages((prev) => [...prev, { role: "bot", text: data.reply }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "LLM is temporarily unavailable." },
      ]);
    }
  };

  return (
    <div className="chatbot-page">
      {/* Aurora Background (UNCHANGED) */}
      <div className="chat-bg">
        <FloatingLines
          enabledWaves={["top", "middle", "bottom"]}
          lineCount={[10, 15, 20]}
          lineDistance={[8, 6, 4]}
          bendRadius={5.0}
          bendStrength={-0.5}
          interactive
          parallax
        />
      </div>

      <Navbar />

      {/* Chat Glass Shell */}
      <div className="chat-shell">
        <div className="chat-container">
          <div className="messages">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`message ${m.role === "bot" ? "bot" : "user"}`}
              >
                {m.text}
              </div>
            ))}
            <div ref={bottomRef} />
          </div>

          <div className="chat-input-bar">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Type your message…"
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}
