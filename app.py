import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# 1. Ambil API_KEY dari Environment Variable Render, atau gunakan default jika di lokal
API_KEY = os.environ.get("API_KEY", "AQ.Ab8RN6KDCVOzRpwRF7-dxq6CDqVoy68QuLTGTt8sJebYC9kh4Q")
client = genai.Client(api_key=API_KEY)

# Konfigurasi opsional agar AI fleksibel merespons
config = types.GenerateContentConfig(
    system_instruction="You are a helpful, smart, and versatile AI assistant. Respond in the same language as the user's prompt."
)

# Buat sesi chat
chat = client.chats.create(
    model="gemini-3-flash-preview",
    config=config
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def send_message():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message.strip():
        return jsonify({"error": "Pesan tidak boleh kosong"}), 400

    try:
        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 2. Ambil port otomatis dari server Render (default ke 5000 jika di laptop)
    port = int(os.environ.get("PORT", 5000))
    # 3. Debug di-set ke False untuk production
    app.run(host="0.0.0.0", port=port, debug=False)