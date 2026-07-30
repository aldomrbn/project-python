import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import yt_dlp


class SocialMediaDownloaderApp:

    def __init__(self, root):
        self.root = root
        self.root.title("YouTube & Instagram Downloader")
        self.root.geometry("520x360")
        self.root.resizable(False, False)

        # Variabel Penyimpan Data
        self.download_folder = tk.StringVar(
            value=os.path.join(os.path.expanduser("~"), "Downloads")
        )
        self.quality_var = tk.StringVar(value="Kualitas Terbaik")

        self.setup_ui()

    def setup_ui(self):
        # Frame Utamanya
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Judul Aplikasi
        title_label = ttk.Label(
            main_frame,
            text="YouTube & Instagram Downloader",
            font=("Helvetica", 15, "bold"),
        )
        title_label.pack(pady=(0, 15))

        # 2. Input Link Video
        url_frame = ttk.LabelFrame(
            main_frame, text=" Link Video (YouTube / Instagram) ", padding=10
        )
        url_frame.pack(fill=tk.X, pady=(0, 10))

        self.url_entry = ttk.Entry(url_frame, font=("Helvetica", 10))
        self.url_entry.pack(fill=tk.X)
        self.url_entry.insert(
            0, "Tempel link YouTube atau Instagram di sini..."
        )  # Placeholder
        self.url_entry.bind(
            "<FocusIn>",
            lambda e: (
                self.url_entry.delete(0, tk.END)
                if "Tempel link" in self.url_entry.get()
                else None
            ),
        )

        # 3. Pilihan Kualitas & Folder Simpan
        opt_frame = ttk.Frame(main_frame)
        opt_frame.pack(fill=tk.X, pady=(0, 15))

        # Pilihan Kualitas / Format
        ttk.Label(opt_frame, text="Format:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        quality_cb = ttk.Combobox(
            opt_frame,
            textvariable=self.quality_var,
            state="readonly",
            width=22,
        )
        quality_cb["values"] = (
            "Kualitas Terbaik",
            "Audio Saja (MP3)",
            "720p (Khusus YouTube)",
            "480p (Khusus YouTube)",
        )
        quality_cb.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Lokasi Penyimpanan
        ttk.Label(opt_frame, text="Simpan Ke:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 5)
        )
        folder_entry = ttk.Entry(
            opt_frame, textvariable=self.download_folder, width=30
        )
        folder_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        btn_browse = ttk.Button(
            opt_frame, text="Cari...", command=self.browse_folder, width=8
        )
        btn_browse.grid(row=1, column=2, padx=(5, 0))

        # 4. Progress Bar & Status
        self.status_label = ttk.Label(
            main_frame, text="Siap mendownload", font=("Helvetica", 9, "italic")
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 5))

        self.progress = ttk.Progressbar(
            main_frame, orient=tk.HORIZONTAL, mode="determinate"
        )
        self.progress.pack(fill=tk.X, pady=(0, 15))

        # 5. Tombol Download
        self.btn_download = ttk.Button(
            main_frame, text="Mulai Download", command=self.start_download_thread
        )
        self.btn_download.pack(ipady=5, fill=tk.X)

    def browse_folder(self):
        selected_dir = filedialog.askdirectory(
            initialdir=self.download_folder.get()
        )
        if selected_dir:
            self.download_folder.set(selected_dir)

    def progress_hook(self, d):
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)

            if total_bytes > 0:
                percentage = (downloaded / total_bytes) * 100
                self.progress["value"] = percentage
                speed = d.get("_speed_str", "N/A")
                self.status_label.config(
                    text=f"Mendownload: {percentage:.1f}% ({speed})"
                )
                self.root.update_idletasks()

        elif d["status"] == "finished":
            self.progress["value"] = 100
            self.status_label.config(text="Memproses/Menggabungkan file...")

    def start_download_thread(self):
        # Thread terpisah agar UI tidak Not Responding / Freeze
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

    def download_video(self):
        url = self.url_entry.get().strip()

        # Validasi domain terdukung
        allowed_domains = ["youtube.com", "youtu.be", "instagram.com"]
        if not url or not any(domain in url for domain in allowed_domains):
            messagebox.showerror(
                "Error", "Masukkan URL valid dari YouTube atau Instagram!"
            )
            return

        self.btn_download.config(state=tk.DISABLED)
        self.progress["value"] = 0
        self.status_label.config(text="Menghubungkan ke server...")

        selected_format = self.quality_var.get()
        postprocessors = []

        # Penyesuaian format untuk YouTube vs Instagram
        if "instagram.com" in url:
            # Instagram fleksibel menggunakan format terbaik yang tersedia
            if selected_format == "Audio Saja (MP3)":
                ydl_format = "bestaudio/best"
                postprocessors.append(
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                )
            else:
                ydl_format = "best"
        else:
            # Konfigurasi khusus YouTube
            if selected_format == "Audio Saja (MP3)":
                ydl_format = "bestaudio/best"
                postprocessors.append(
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                )
            elif selected_format == "720p (Khusus YouTube)":
                ydl_format = "bestvideo[height<=720]+bestaudio/best[height<=720]"
            elif selected_format == "480p (Khusus YouTube)":
                ydl_format = "bestvideo[height<=480]+bestaudio/best[height<=480]"
            else:
                ydl_format = "bestvideo+bestaudio/best"

        ydl_opts = {
            "format": ydl_format,
            "outtmpl": os.path.join(
                self.download_folder.get(), "%(title)s_%(id)s.%(ext)s"
            ),
            "progress_hooks": [self.progress_hook],
            "postprocessors": postprocessors,
            "quiet": True,
            # User agent khusus untuk menghindari pemblokiran batas permintaan
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            ),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo(
                "Sukses", "Media dari YouTube/Instagram berhasil diunduh!"
            )
            self.status_label.config(text="Selesai!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mendownload:\n{str(e)}")
            self.status_label.config(text="Download Gagal")
        finally:
            self.btn_download.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaDownloaderApp(root)
    root.mainloop()