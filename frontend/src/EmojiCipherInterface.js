import React, { useState } from 'react';
import './EmojiCipherInterface.css'; // Updated CSS import

// --- Security Warning ---
// This component interacts with an API performing a simple substitution cipher.
// This cipher is NOT cryptographically secure and should NEVER be used
// for protecting sensitive information. It is for demonstration/novelty only.
// Ensure proper input validation and output encoding are handled,
// although React largely handles basic XSS prevention for rendered output.
// ------------------------

function EmojiCipherInterface() { // Renamed component function
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [error, setError] = useState('');
  // Ensure this matches the host/port your Flask backend is running on.
  const backendUrl = 'http://localhost:5000/api';

  const handleApiCall = async (endpoint, text) => {
    setError(''); // Clear previous errors
    setOutputText(''); // Clear previous output

    // Basic validation: prevent empty requests
    if (!text || !text.trim()) {
      setError('Input cannot be empty.');
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add other headers if needed, e.g., for authentication in a real app
        },
        body: JSON.stringify({ text: text }), // Send text in JSON body
      });

      const data = await response.json(); // Always expect JSON response

      if (!response.ok) {
        // Handle HTTP errors (e.g., 4xx, 5xx) using error message from backend if available
        throw new Error(data.error || `Request failed with status: ${response.status}`);
      }

      // Expecting { "result": "..." } on success
      if (data.result !== undefined) {
        setOutputText(data.result);
      } else {
        // Handle unexpected successful response format
        throw new Error("Received an unexpected response format from the server.");
      }

    } catch (err) {
      // Handle network errors or errors thrown above
      console.error(`API call error (${endpoint}):`, err);
      // Display a user-friendly error message
      setError(`Operation failed. ${err.message}. Is the backend running at ${backendUrl}?`);
    }
  };

  const handleEncrypt = () => {
    handleApiCall('encrypt', inputText);
  };

  const handleDecrypt = () => {
    handleApiCall('decrypt', inputText);
  };

  return (
    <div className="App">
      <h1>Emoji Cipher 🔒➡️😃</h1>
      <p style={{ fontSize: '0.8em', fontStyle: 'italic', color: '#aaa' }}>
        (Warning: This is a simple, insecure substitution cipher for novelty only.)
      </p>

      <textarea
        placeholder="Enter text to encrypt or emojis to decrypt..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        aria-label="Input text or emojis" // Accessibility improvement
      />

      <div>
        <button onClick={handleEncrypt}>Encrypt</button>
        <button onClick={handleDecrypt}>Decrypt</button>
      </div>

      {/* Display error messages */}
      {error && <div className="error-message" role="alert">Error: {error}</div>}

      {/* Display results */}
      {outputText && (
        <div>
          <h2>Result:</h2>
          <div className="result-area">
            {/* Output is rendered as text; React handles basic XSS protection */}
            {outputText}
          </div>
        </div>
      )}
    </div>
  );
}

export default EmojiCipherInterface; // Updated export
