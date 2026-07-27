import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load file .env jika ada
load_dotenv()

app = Flask(__name__)

# Mengambil API Key dari Environment Variable
API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_INSTRUCTION = "You are a helpful, smart, and versatile AI assistant. Respond in the same language as the user's prompt."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def send_message():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message.strip():
        return jsonify({"error": "Pesan tidak boleh kosong"}), 400

    if not API_KEY:
        return jsonify({"error": "API Key tidak ditemukan"}), 500

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
        
        payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_message}]
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()

        if response.status_code != 200:
            print("--- GOOGLE ERROR RESPONSE ---")
            print(res_data)
            return jsonify({"error": res_data.get("error", {}).get("message", "Terjadi kesalahan pada API")}), response.status_code

        reply_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply_text})
        
    except Exception as e:
        print("--- SERVER ERROR ---")
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)