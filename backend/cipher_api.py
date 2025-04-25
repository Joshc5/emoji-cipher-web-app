import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Security Warning ---
# This emoji cipher is a simple substitution cipher.
# It is NOT cryptographically secure and should NEVER be used
# for protecting sensitive information. It is for demonstration/novelty only.
# ------------------------

# Initialize Flask app
app = Flask(__name__)

# Configure CORS: Allow requests from the typical React dev server origin.
# For production, restrict this to your actual frontend domain.
# Example: CORS(app, origins=["https://your-frontend-domain.com"])
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Define the character-to-emoji mapping
# Ensure enough unique emojis are chosen
emoji_map = {
    # Lowercase
    'a': '🍎', 'b': '🍌', 'c': '🍒', 'd': '🍇', 'e': '🍓', 'f': '🥝', 'g': '🍍',
    'h': '🥭', 'i': '🍑', 'j': '🥥', 'k': '🍅', 'l': '🍆', 'm': '🥑', 'n': '🥦',
    'o': '🥬', 'p': '🥒', 'q': '🌶️', 'r': '🌽', 's': '🥕', 't': '🧄', 'u': '🧅',
    'v': '🥔', 'w': '🍠', 'x': '🥐', 'y': '🥯', 'z': '🍞',
    # Uppercase
    'A': '🌀', 'B': '🗿', 'C': '🔭', 'D': '🧬', 'E': '🪐', 'F': '🛸', 'G': '🚀',
    'H': '🌠', 'I': '🌌', 'J': '🌋', 'K': '🏛️', 'L': '⛩️', 'M': '🕋', 'N': '🕌',
    'O': '🕍', 'P': '🕎', 'Q': '☯️', 'R': '☦️', 'S': '☮️', 'T': '✝️', 'U': '☪️',
    'V': '🕉️', 'W': '☸️', 'X': '☢️', 'Y': '🔯', 'Z': '🪁',
    # Digits (Scrambled)
    '0': '7️⃣', '1': '3️⃣', '2': '9️⃣', '3': '1️⃣', '4': '6️⃣',
    '5': '0️⃣', '6': '4️⃣', '7': '8️⃣', '8': '2️⃣', '9': '5️⃣',
    # Space and Punctuation (Expanded)
    ' ': '␣', # Using symbol for space for clarity
    '.': '⚫', ',': '⚪', '!': '❗', '?': '❓', "'": '✨', '"': '💬',
    ';': '↔️', ':': '🕒', '-': '➖', '(': '👈', ')': '👉', '\n': '␤',
    '@': '📧', '#': '#️⃣', '$': '💲', '%': '💹', '^': '🔼', '&': '🔗',
    '*': '✳️', '=': '🟰', '[': '⏪', ']': '⏩', '\\': '📉', '/': '📈',
}

# Create the reverse mapping (emoji-to-character) for decryption
# Sort keys by length descending to handle multi-character emojis correctly during decryption
reverse_emoji_map = {v: k for k, v in emoji_map.items()}
sorted_emoji_keys = sorted(reverse_emoji_map.keys(), key=len, reverse=True)

def encrypt(text):
    """
    Encrypts text to emojis using the defined map.
    WARNING: This is NOT a secure encryption method.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    encrypted_text = ""
    for char in text:
        encrypted_text += emoji_map.get(char, char) # Keep unknown chars as is
    return encrypted_text

def decrypt(emoji_text):
    """
    Decrypts emojis back to text using the reverse map.
    WARNING: This is NOT a secure encryption method.
    """
    if not isinstance(emoji_text, str):
        raise TypeError("Input must be a string")

    decrypted_text = ""
    i = 0
    text_len = len(emoji_text)
    while i < text_len:
        found_match = False
        # Iterate through known emojis (longest first) to find a match
        for emoji_key in sorted_emoji_keys:
            if emoji_text.startswith(emoji_key, i):
                decrypted_text += reverse_emoji_map[emoji_key]
                i += len(emoji_key) # Move index past the matched emoji
                found_match = True
                break # Found the longest match starting at i

        if not found_match:
            # If no known emoji starts at the current position, treat it as an unknown character.
            # Append the character as is. This could be an unmapped character
            # or part of an invalid/incomplete emoji sequence.
            # Consider logging this occurrence if it's unexpected.
            decrypted_text += emoji_text[i]
            i += 1
    return decrypted_text

@app.route('/api/encrypt', methods=['POST'])
def handle_encrypt():
    """API endpoint to encrypt text."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415 # Unsupported Media Type

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field in JSON body"}), 400 # Bad Request

    text_to_encrypt = data['text']

    if not isinstance(text_to_encrypt, str):
         return jsonify({"error": "'text' field must be a string"}), 400 # Bad Request

    try:
        encrypted_result = encrypt(text_to_encrypt)
        return jsonify({"result": encrypted_result}), 200
    except Exception as e:
        # Log the exception e here in a real application
        print(f"Error during encryption: {e}") # Basic logging for dev
        return jsonify({"error": "An internal error occurred during encryption."}), 500 # Internal Server Error


@app.route('/api/decrypt', methods=['POST'])
def handle_decrypt():
    """API endpoint to decrypt emoji text."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415 # Unsupported Media Type

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field in JSON body"}), 400 # Bad Request

    text_to_decrypt = data['text']

    if not isinstance(text_to_decrypt, str):
         return jsonify({"error": "'text' field must be a string"}), 400 # Bad Request

    try:
        decrypted_result = decrypt(text_to_decrypt)
        return jsonify({"result": decrypted_result}), 200
    except Exception as e:
        # Log the exception e here in a real application
        print(f"Error during decryption: {e}") # Basic logging for dev
        return jsonify({"error": "An internal error occurred during decryption."}), 500 # Internal Server Error

if __name__ == '__main__':
    # --- Development Server ---
    # The following runs Flask's built-in development server.
    # It is NOT suitable for production.
    # For production, use a proper WSGI server like Gunicorn or Waitress.
    # Example using Gunicorn: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    # Also, ensure debug=False in production.
    # --------------------------
    app.run(debug=True, host='0.0.0.0', port=5000) # Use 0.0.0.0 to be accessible on network
