from google import genai

# Menggunakan API Key valid dari screenshot kamu
API_KEY = "AQ.Ab8RN6KDCVOzRpwRF7-dxq6CDqVoy68QuLTGTt8sJebYC9kh4Q"
client = genai.Client(api_key=API_KEY)

# Mulai sesi chat interaktif
# Pasang model terbaru:
chat = client.chats.create(model="gemini-3-flash-preview")
# Teks indikator baru untuk memastikan file ini yang berjalan
print("=== INFO: SEKARANG KAMU MENJALANKAN FILE CHAT.PY ===")
print("Ketik 'keluar' untuk mengakhiri percakapan.\n")

while True:
    user_input = input("Kamu: ")
    
    if user_input.lower() == 'keluar':
        print("AI: Sampai jumpa!")
        break
        
    if not user_input.strip():
        continue

    try:
        response = chat.send_message(user_input)
        print(f"AI: {response.text}\n")
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}\n")