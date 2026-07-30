import random
import string
import tkinter as tk
from tkinter import messagebox, ttk


class PasswordGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("380x300")
        self.root.resizable(False, False)

        # Variabel
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Generator Password Safe", font=("Helvetica", 14, "bold")
        ).pack(pady=(0, 15))

        # Output Password
        self.pass_entry = ttk.Entry(frame, font=("Helvetica", 12), justify="center")
        self.pass_entry.pack(fill=tk.X, pady=(0, 15))

        # Kontrol Panjang
        len_frame = ttk.Frame(frame)
        len_frame.pack(fill=tk.X, pady=5)
        ttk.Label(len_frame, text="Panjang Password:").pack(side=tk.LEFT)
        ttk.Spinbox(
            len_frame,
            from_=6,
            to=32,
            textvariable=self.length_var,
            width=5,
            state="readonly",
        ).pack(side=tk.RIGHT)

        # Checkbox Opsi
        ttk.Checkbutton(
            frame, text="Sertakan Angka (0-9)", variable=self.use_digits
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            frame, text="Sertakan Simbol (!@#$)", variable=self.use_symbols
        ).pack(anchor=tk.W, pady=2)

        # Tombol
        btn_generate = ttk.Button(
            frame, text="Buat Password", command=self.generate_password
        )
        btn_generate.pack(fill=tk.X, pady=(15, 5))

        btn_copy = ttk.Button(
            frame, text="Salin ke Clipboard", command=self.copy_to_clipboard
        )
        btn_copy.pack(fill=tk.X)

    def generate_password(self):
        chars = string.ascii_letters
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += string.punctuation

        password = "".join(
            random.choice(chars) for _ in range(self.length_var.get())
        )
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, password)

    def copy_to_clipboard(self):
        password = self.pass_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Sukses", "Password berhasil disalin!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()