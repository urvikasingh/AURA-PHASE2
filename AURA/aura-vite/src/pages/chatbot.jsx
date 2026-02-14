import { useState, useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "./Navbar.jsx";
import FloatingLines from "../react-comp/FloatingLines.jsx";
import "./chatbot.css";
import { apiRequest } from "../services/api";

export default function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const location = useLocation();
  const domain =
    new URLSearchParams(location.search).get("domain") || "usp";

  const storageKey = `aura_active_conversation_${domain}`;

  const [conversationId, setConversationId] = useState(() => {
    const saved = localStorage.getItem(storageKey);
    return saved ? Number(saved) : null;
  });

  const [conversations, setConversations] = useState([]);
  const bottomRef = useRef(null);

  /* =========================
     SCROLL
  ========================= */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  /* =========================
     RESET ON DOMAIN CHANGE
  ========================= */
  useEffect(() => {
    setMessages([]);
    setConversationId(null);
    localStorage.removeItem(storageKey);
  }, [domain]);

  /* =========================
     LOAD SIDEBAR
  ========================= */
  useEffect(() => {
    apiRequest(`/conversations?domain=${domain}`)
      .then(setConversations)
      .catch(console.error);
  }, [domain]);

  /* =========================
     RESTORE CHAT ON REFRESH
  ========================= */
  useEffect(() => {
    if (!conversationId) return;

    apiRequest(`/chat/history/${conversationId}`)
      .then((msgs) => {
        const formatted = msgs.map((m) => ({
          role: m.role === "assistant" ? "bot" : "user",
          text: m.content,
        }));
        setMessages(formatted);
      })
      .catch(console.error);
  }, [conversationId]);

  /* =========================
     OPEN EXISTING CHAT
  ========================= */
  const openConversation = async (convId) => {
    if (!convId) return;

    const conv = conversations.find(
      (c) => (c.id ?? c.conversation_id) === convId
    );

    if (!conv || conv.domain !== domain) return;

    setConversationId(convId);
    localStorage.setItem(storageKey, convId);

    const msgs = await apiRequest(`/chat/history/${convId}`);
    setMessages(
      msgs.map((m) => ({
        role: m.role === "assistant" ? "bot" : "user",
        text: m.content,
      }))
    );
  };

  /* =========================
     NEW CHAT
  ========================= */
  const startNewChat = () => {
    setConversationId(null);
    setMessages([]);
    localStorage.removeItem(storageKey);
  };

  /* =========================
     SEND MESSAGE
  ========================= */
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userMessage },
    ]);

    try {
      const payload = {
        domain,
        message: userMessage,
        conversation_id: conversationId,
      };

      const data = await apiRequest("/chat", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      setMessages((prev) => [
        ...prev,
        { role: "bot", text: data.reply },
      ]);

      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
        localStorage.setItem(storageKey, data.conversation_id);

        apiRequest(`/conversations?domain=${domain}`)
          .then(setConversations)
          .catch(console.error);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "LLM is temporarily unavailable." },
      ]);
    }
  };

  return (
    <div className="chatbot-page">
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

      <div className="chat-shell">
        <div className="chat-sidebar">
          <button className="new-chat-btn" onClick={startNewChat}>
            + New Chat
          </button>

          {conversations.map((c) => {
            const convId = c.id ?? c.conversation_id;
            if (c.domain !== domain) return null;

            return (
              <div
                key={convId}
                onClick={() => openConversation(convId)}
                className={`chat-history-item ${
                  convId === conversationId ? "active" : ""
                }`}
              >
                <div className="chat-title">
                  {new Date(c.created_at).toLocaleString()}
                </div>
              </div>
            );
          })}
        </div>

        <div className="chat-container">
          <div className="messages">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`message ${m.role}`}
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
