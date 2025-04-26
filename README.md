# Emoji Cipher Web App 🔒➡️😃

[![React](https://img.shields.io/badge/React-^19.1.0-blue?logo=react)](https://reactjs.org/) [![Flask](https://img.shields.io/badge/Flask-3.0.3-grey?logo=flask)](https://flask.palletsprojects.com/) [![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)

Turn your text into a secret (well, not *really* secret) emoji code! This web application uses a simple substitution cipher to convert text characters into corresponding emojis and back again.

**✨ Features:**

*   Encrypts letters (uppercase & lowercase), numbers, and common symbols into unique emojis.
*   Decrypts the emoji code back into the original text.
*   Sleek, dark theme UI. ;)
*   Built with a React frontend and a Python Flask backend API.

**🚨 IMPORTANT SECURITY WARNING 🚨**

This application implements a **simple substitution cipher**. It is **NOT cryptographically secure** in any way and should **NEVER** be used to protect sensitive information. It is purely for educational purposes, demonstration, or novelty fun. Treat the "encrypted" output as easily decipherable.

## Project Structure

```
emoji_cipher_app/
├── backend/         # Python Flask API
│   ├── cipher_api.py  # Main Flask application, cipher logic, API endpoints
│   └── requirements.txt # Backend Python dependencies
├── frontend/        # React User Interface
│   ├── public/        # Static assets
│   ├── src/           # React components and source code
│   │   ├── EmojiCipherInterface.js # Main application component
│   │   └── EmojiCipherInterface.css # Styling
│   ├── package.json   # Frontend Node.js dependencies and scripts
│   └── ...            # Other React project files
└── README.md        # This file
```

## Setup and Installation

You'll need [Python](https://www.python.org/downloads/) (3.x recommended) and [Node.js](https://nodejs.org/) (v14 or higher, includes npm) installed.

### 1. Backend Setup (Flask)

```bash
# Navigate to the backend directory
cd emoji_cipher_app/backend

# (Recommended) Create and activate a Python virtual environment
# On Windows:
# python -m venv venv
# .\venv\Scripts\activate
# On macOS/Linux:
# python3 -m venv venv
# source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt
```

### 2. Frontend Setup (React)

```bash
# Navigate to the frontend directory from the project root
cd ../frontend
# Or if you are already in the backend directory: cd ../frontend

# Install required Node.js packages
npm install
```

## Running the Application

You need to run both the backend and frontend servers simultaneously in separate terminals.

### 1. Run the Backend Server

```bash
# Make sure you are in the backend directory (emoji_cipher_app/backend)
# Make sure your Python virtual environment is activated (if you created one)
python cipher_api.py
```

The Flask backend server will start on `http://localhost:5000`. Keep this terminal running.

### 2. Run the Frontend Server

```bash
# Open a NEW terminal
# Make sure you are in the frontend directory (emoji_cipher_app/frontend)
npm start
```

This command should automatically open the application in your default web browser at `http://localhost:3000`.

Now you can use the Emoji Cipher app! 🎉

## How it Works

The React frontend captures user input and sends it to the Flask backend API via `fetch` requests. The backend has two main endpoints:

*   `/api/encrypt` (POST): Takes `{"text": "your input"}` and returns `{"result": "🍎🍌🍒..."}`.
*   `/api/decrypt` (POST): Takes `{"text": "🍎🍌🍒..."}` and returns `{"result": "your input"}`.

The backend uses a predefined Python dictionary (`emoji_map`) to perform the character-to-emoji substitution and a reverse map for decryption.
