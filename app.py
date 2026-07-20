from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Inisialisasi Gemini Client
API_KEY = "AQ.Ab8RN6KDCVOzRpwRF7-dxq6CDqVoy68QuLTGTt8sJebYC9kh4Q"
client = genai.Client(api_key=API_KEY)

# Buat sesi chat
chat = client.chats.create(model="gemini-3-flash-preview")

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
    app.run(host="0.0.0.0", port=5000, debug=True)