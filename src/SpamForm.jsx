import { useState } from "react";

function SpamForm() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null); // "Spam" | "Not Spam"

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!subject.trim() || !body.trim()) {
      setResult(null);
      alert("Please enter both subject and email content");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("https://spam-email-backend-t21e.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ subject, body }),
      });

      const data = await response.json();

      // Only store Spam / Not Spam
      setResult(data.prediction);
    } catch (error) {
      console.error(error);
      setResult("Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Spam Email Classifier</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Email Subject"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
        />

        <textarea
          placeholder="Email Body"
          rows="8"
          value={body}
          onChange={(e) => setBody(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Checking..." : "Check Email"}
        </button>
      </form>

      {/* RESULT BOX */}
      {result && result !== "Error" && (
        <div
          className={`result-box ${
            result === "Spam" ? "spam" : "not-spam"
          }`}
        >
          {result}
        </div>
      )}

      {result === "Error" && (
        <div className="result-box spam">
          Server Error
        </div>
      )}
    </div>
  );
}

export default SpamForm;
