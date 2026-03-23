import React, { useEffect, useRef, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8010";

function App() {
  const [inputText, setInputText] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showIntro, setShowIntro] = useState(true);
  const [menuOpen, setMenuOpen] = useState(false);
  const [showContact, setShowContact] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [showEnhanceTip, setShowEnhanceTip] = useState(false);
  const [enhanceTipShown, setEnhanceTipShown] = useState(false);
  const [showPdfSummary, setShowPdfSummary] = useState(false);
  const [pdfSummaryText, setPdfSummaryText] = useState("");
  const [pdfFileName, setPdfFileName] = useState("");
  const [theme, setTheme] = useState(() => localStorage.getItem("promptify-theme") || "dark");
  const pdfInputRef = useRef(null);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setShowIntro(false);
    }, 1700);

    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("promptify-theme", theme);
  }, [theme]);

  const handleEnhance = async () => {
    if (!inputText.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/enhance`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: inputText }),
      });

      const data = await response.json();
      const enhanced = (data.enhanced_message || "").trim();
      if (enhanced) {
        setInputText(enhanced);
        if (!enhanceTipShown) {
          setShowEnhanceTip(true);
          setEnhanceTipShown(true);
        }
      }
    } catch (error) {
      // Keep existing input text unchanged if enhancement fails.
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    const outgoingMessage = inputText.trim();
    if (!outgoingMessage) return;

    const userMessage = { role: "user", content: outgoingMessage };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: outgoingMessage }),
      });

      const data = await response.json();
      const assistantMessage = {
        role: "assistant",
        content: data.reply || "No response received.",
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setInputText("");
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error: unable to fetch response from server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSummarizePdf = async (file) => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/summarize-pdf`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || "Could not summarize PDF.");
      }
      setPdfFileName(file.name);
      setPdfSummaryText(data.summary || "No summary returned.");
      setShowPdfSummary(true);
    } catch (error) {
      setPdfFileName(file.name || "PDF");
      setPdfSummaryText(`Error: ${error.message}`);
      setShowPdfSummary(true);
    } finally {
      setLoading(false);
    }
  };

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  return (
    <div className="page">
      <div className="bg-orb orb-1" />
      <div className="bg-orb orb-2" />

      <button
        className={`menu-fab ${menuOpen ? "open" : ""}`}
        aria-label="Open menu"
        onClick={() => setMenuOpen((prev) => !prev)}
      >
        <span />
        <span />
        <span />
      </button>

      {menuOpen && <div className="sidebar-overlay" onClick={() => setMenuOpen(false)} />}

      <aside className={`menu-panel ${menuOpen ? "open" : ""}`} role="menu" aria-label="Main menu">
        <h3>Quick Settings</h3>
        <button className="menu-item" onClick={toggleTheme}>
          <span className="menu-item-label">Theme</span>
        </button>
        <button
          className="menu-item"
          onClick={() => {
            setShowContact(true);
            setMenuOpen(false);
          }}
        >
          <span className="menu-item-label">Contact</span>
        </button>
        <button
          className="menu-item"
          onClick={() => {
            setShowAbout(true);
            setMenuOpen(false);
          }}
        >
          <span className="menu-item-label">About</span>
        </button>
      </aside>

      {showContact && (
        <div className="modal-backdrop" onClick={() => setShowContact(false)}>
          <div className="contact-modal" onClick={(e) => e.stopPropagation()}>
            <h3>Contact Us</h3>
            <p>
              Email: <a href="mailto:abhisheksumod10@gmail.com">abhisheksumod10@gmail.com</a>
            </p>
            <button className="close-btn" onClick={() => setShowContact(false)}>
              Close
            </button>
          </div>
        </div>
      )}

      {showAbout && (
        <div className="modal-backdrop" onClick={() => setShowAbout(false)}>
          <div className="contact-modal" onClick={(e) => e.stopPropagation()}>
            <h3>About Promptify</h3>
            <p>
              Promptify is a smart prompt-first chatbot workspace. It helps users enhance their
              prompts before sending, then delivers better assistant responses in a clean,
              modern chat interface.
            </p>
            <button className="close-btn" onClick={() => setShowAbout(false)}>
              Close
            </button>
          </div>
        </div>
      )}

      {showEnhanceTip && (
        <div className="modal-backdrop" onClick={() => setShowEnhanceTip(false)}>
          <div className="contact-modal" onClick={(e) => e.stopPropagation()}>
            <h3>Prompt Enhanced</h3>
            <p>
              Your enhanced prompt is now in the input box. If you want another version,
              click Enhance Prompt again.
            </p>
            <button className="close-btn" onClick={() => setShowEnhanceTip(false)}>
              OK
            </button>
          </div>
        </div>
      )}

      {showPdfSummary && (
        <div className="modal-backdrop" onClick={() => setShowPdfSummary(false)}>
          <div className="contact-modal pdf-summary-modal" onClick={(e) => e.stopPropagation()}>
            <h3>PDF Summary</h3>
            <p className="pdf-summary-file">{pdfFileName}</p>
            <div className="pdf-summary-content">{pdfSummaryText}</div>
            <button className="close-btn" onClick={() => setShowPdfSummary(false)}>
              Close
            </button>
          </div>
        </div>
      )}

      {showIntro ? (
        <div className="intro-text-wrap">
          <h1 className="intro-title">Promptify</h1>
          <p className="intro-subtitle">
            Elevate every prompt before it reaches your AI assistant.
          </p>
        </div>
      ) : (
        <main className="workspace">
          <section className="hero-row">
            <h1>Promptify</h1>
            <p>Sharper prompts. Better answers.</p>
          </section>

          {(messages.length > 0 || loading) && (
            <section className="messages-surface">
              {messages.map((msg, index) => (
                <div key={`${msg.role}-${index}`} className={`message ${msg.role}`}>
                  <strong>{msg.role === "user" ? "You" : "Assistant"}</strong>
                  <p>{msg.content}</p>
                </div>
              ))}

              {loading && <p className="loading">Generating response...</p>}
            </section>
          )}

          <section className="composer-surface">
            <input
              ref={pdfInputRef}
              type="file"
              accept="application/pdf"
              className="hidden-file-input"
              onChange={(e) => {
                const file = e.target.files?.[0] || null;
                if (file) {
                  handleSummarizePdf(file);
                }
                e.target.value = "";
              }}
            />

            <textarea
              rows={4}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your message..."
            />

            <div className="buttons">
              <button onClick={handleEnhance} disabled={loading || !inputText.trim()}>
                Enhance Prompt
              </button>
              <button
                onClick={() => pdfInputRef.current?.click()}
                disabled={loading}
              >
                PDF Summarizer
              </button>
              <button
                className="send"
                onClick={handleSend}
                disabled={loading || !inputText.trim()}
              >
                Send
              </button>
            </div>

          </section>
        </main>
      )}
    </div>
  );
}

export default App;
