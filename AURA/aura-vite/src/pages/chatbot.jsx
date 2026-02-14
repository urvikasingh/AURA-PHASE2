import { useState, useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "./Navbar.jsx";
import FloatingLines from "../react-comp/FloatingLines.jsx";
import "./chatbot.css";
import { apiRequest } from "../services/api";

export default function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [conversations, setConversations] = useState([]);
  const [deleteTarget, setDeleteTarget] = useState(null);

  const bottomRef = useRef(null);
  const location = useLocation();

  const domain =
    new URLSearchParams(location.search).get("domain") || "usp";

  const storageKey = `aura_active_conversation_${domain}`;

  const [conversationId, setConversationId] = useState(() => {
    const saved = localStorage.getItem(storageKey);
    return saved ? Number(saved) : null;
  });

  /* =========================
     SCROLL TO BOTTOM
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
     LOAD SIDEBAR CONVERSATIONS
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
        setMessages(
          msgs.map((m) => ({
            role: m.role === "assistant" ? "bot" : "user",
            text: m.content,
          }))
        );
      })
      .catch(console.error);
  }, [conversationId]);

  /* =========================
     OPEN EXISTING CHAT
  ========================= */
  const openConversation = async (convId) => {
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
     DELETE CONVERSATION
     (FIXED — ALWAYS RESET CHAT)
  ========================= */
  const handleDeleteConversation = async (convId) => {
    try {
      await apiRequest(`/conversations/${convId}`, {
        method: "DELETE",
      });

      // Remove from sidebar
      setConversations((prev) =>
        prev.filter(
          (c) => (c.id ?? c.conversation_id) !== convId
        )
      );

      // ✅ ALWAYS reset chat (no ID comparison)
      startNewChat();

      setDeleteTarget(null);
    } catch (err) {
      console.error("Failed to delete conversation", err);
    }
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
        localStorage.setItem(
          storageKey,
          data.conversation_id
        );

        apiRequest(`/conversations?domain=${domain}`)
          .then(setConversations)
          .catch(console.error);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "LLM is temporarily unavailable.",
        },
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
        {/* SIDEBAR */}
        <div className="chat-sidebar">
          <button
            className="new-chat-btn"
            onClick={startNewChat}
          >
            + New Chat
          </button>

          {conversations.map((c) => {
            const convId = c.id ?? c.conversation_id;
            if (c.domain !== domain) return null;

            return (
              <div
                key={convId}
                className={`chat-history-item ${
                  convId === conversationId ? "active" : ""
                }`}
                onClick={() => openConversation(convId)}
              >
                <div className="chat-title">
                  {new Date(c.created_at).toLocaleString()}
                </div>

                <button
                  className="delete-conv-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteTarget(convId);
                  }}
                >
                  🗑
                </button>
              </div>
            );
          })}
        </div>

        {/* CHAT AREA */}
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
              onKeyDown={(e) =>
                e.key === "Enter" && sendMessage()
              }
              placeholder="Type your message…"
            />
            <button onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
      </div>

      {/* DELETE CONFIRMATION MODAL */}
      {deleteTarget && (
        <div className="modal-backdrop">
          <div className="modal">
            <h3>Delete this conversation?</h3>
            <p>This action can’t be undone.</p>

            <div className="modal-actions">
              <button
                onClick={() => setDeleteTarget(null)}
              >
                Cancel
              </button>
              <button
                className="danger"
                onClick={() =>
                  handleDeleteConversation(deleteTarget)
                }
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
