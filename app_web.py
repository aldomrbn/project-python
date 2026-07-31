import os
import speech_recognition as sr
import streamlit as st
import yt_dlp
from moviepy import AudioFileClip

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Video to Text Converter", page_icon="🎬", layout="centered"
)

st.title("🎬 Video to Text Converter")
st.write(
    "Masukkan link video (YouTube / Instagram / TikTok / MP4) untuk mengonversi suaranya menjadi teks."
)


def download_audio_from_url(url):
    """Mendownload audio langsung dari link video menggunakan yt-dlp."""
    # Bersihkan file sampah lama jika ada
    for f in os.listdir("."):
        if f.startswith("temp_downloaded_media"):
            try:
                os.remove(f)
            except Exception:
                pass

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "temp_downloaded_media.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename


def convert_to_wav(input_file, output_wav="temp_audio.wav"):
    """Mengonversi file audio/video apa pun (m4a, mp4, webm) menjadi WAV standar."""
    # Menggunakan AudioFileClip agar kompatibel dengan file m4a / mp3 / mp4
    with AudioFileClip(input_file) as clip:
        clip.write_audiofile(
            output_wav,
            logger=None,
            codec="pcm_s16le",
            fps=16000,  # Optimal untuk speech recognition
        )
    return output_wav


# --- TAMPILAN FORM WEB ---
url_input = st.text_input("🔗 Link Video:", placeholder="https://...")

basa_pilihan = st.selectbox(
    "🌐 Bahasa dalam Video:",
    [("Bahasa Indonesia", "id-ID"), ("Bahasa Inggris", "en-US")],
    format_func=lambda x: x[0],
)

if st.button("🚀 Proses & Ubah ke Teks", type="primary"):
    if not url_input.strip():
        st.error("Silakan masukkan link video terlebih dahulu!")
    else:
        try:
            with st.spinner("1/3 Mendownload media dari link..."):
                media_file = download_audio_from_url(url_input)

            with st.spinner("2/3 Memproses format audio..."):
                wav_file = convert_to_wav(media_file)

            with st.spinner("3/3 Mengonversi suara menjadi teks..."):
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_file) as source:
                    audio_data = recognizer.record(source)

                text_result = recognizer.recognize_google(
                    audio_data, language=basa_pilihan[1]
                )

            # TAMPILKAN HASIL TEKS
            st.success("✅ Transkripsi Selesai!")
            st.subheader("Hasil Teks:")
            st.text_area("Teks Transkripsi:", value=text_result, height=200)

            # TOMBOL DOWNLOAD TEKS
            st.download_button(
                label="📥 Download Hasil (.txt)",
                data=text_result,
                file_name="hasil_transkrip.txt",
                mime="text/plain",
            )

        except sr.UnknownValueError:
            st.warning(
                "⚠️ Suara dalam video tidak terdeteksi atau kurang jelas."
            )
        except sr.RequestError as e:
            st.error(f"❌ Gagal terhubung ke Google API: {e}")
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")
        finally:
            # Bersihkan file sementara
            for f in os.listdir("."):
                if f.startswith("temp_downloaded_media") or f == "temp_audio.wav":
                    try:
                        os.remove(f)
                    except Exception:
                        pass