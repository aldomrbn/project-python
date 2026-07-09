import tkinter as tk
import math

class DualModeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Retro Calculator")
        self.root.geometry("390x650") # Ukuran awal untuk mode Basic
        self.root.resizable(False, False)
        
        # --- PALET WARNA (PERSIS GAMBAR) ---
        self.COLOR_BODY_BG = "#F3F3F3"     
        self.COLOR_LCD_BG = "#8FA88B"      
        self.COLOR_LCD_TEXT = "#1E261D"    
        self.COLOR_BTN_WHITE = "#FFFFFF"   
        self.COLOR_BTN_DARK = "#2D3130"    
        self.COLOR_TEXT_DARK = "#333333"   
        
        self.expression = ""
        self.current_mode = "BASIC" # Mode default awal
        
        # --- TOP HEADER BAR ---
        self.header_frame = tk.Frame(self.root, bg="#2D3130", height=45)
        self.header_frame.pack(fill="x")
        
        self.header_label = tk.Label(self.header_frame, text="  ≡  Basic Calculator", 
                                     font=("Helvetica", 13, "bold"), bg="#2D3130", fg="#FFFFFF", anchor="w")
        self.header_label.pack(side="left", fill="y", pady=5)
        
        # TOMBOL UNTUK BERUBAH MODE
        self.mode_btn = tk.Button(self.header_frame, text="SWITCH MODE ⇄ ", font=("Helvetica", 10, "bold"),
                                  bg="#404544", fg="#FFFFFF", bd=0, padx=10, cursor="hand2",
                                  activebackground="#555B5A", activeforeground="#FFFFFF",
                                  command=self.toggle_mode)
        self.mode_btn.pack(side="right", fill="y", padx=5, pady=5)
        
        # --- DISPLAY SCREEN AREA ---
        self.display_container = tk.Frame(self.root, bg=self.COLOR_BODY_BG, padx=20, pady=15)
        self.display_container.pack(fill="x")
        
        self.lcd_screen = tk.Label(self.display_container, text="0", anchor="e",
                                   font=("Courier", 42, "bold"), bg=self.COLOR_LCD_BG, fg=self.COLOR_LCD_TEXT,
                                   padx=15, pady=15, highlightbackground="#B5CBB1", highlightthickness=3, relief="flat")
        self.lcd_screen.pack(fill="x")
        
        # --- CONTAINER UTAMA UNTUK TOMBOL ---
        self.buttons_container = tk.Frame(self.root, bg=self.COLOR_BODY_BG)
        self.buttons_container.pack(expand=True, fill="both")
        
        # Gambar layout tombol pertama kali
        self.render_buttons()

    def toggle_mode(self):
        """ Fungsi utama untuk merubah mode kalkulator """
        if self.current_mode == "BASIC":
            self.current_mode = "SCIENTIFIC"
            self.header_label.config(text="  ≡  Scientific Calculator")
            self.root.geometry("520x680") # Melebar untuk menampung tombol scientific
        else:
            self.current_mode = "BASIC"
            self.header_label.config(text="  ≡  Basic Calculator")
            self.root.geometry("390x650") # Kembali ke ukuran semula
            
        self.expression = ""
        self.lcd_screen.config(text="0")
        self.render_buttons()

    def render_buttons(self):
        # Bersihkan tombol lama sebelum menggambar tombol baru
        for widget in self.buttons_container.winfo_children():
            widget.destroy()
            
        if self.current_mode == "BASIC":
            self.setup_basic_layout()
        else:
            self.setup_scientific_layout()

    # --- LAYOUT 1: BASIC CALCULATOR ---
    def setup_basic_layout(self):
        grid_frame = tk.Frame(self.buttons_container, bg=self.COLOR_BODY_BG, padx=15, pady=5)
        grid_frame.pack(expand=True, fill="both")
        
        for i in range(6): grid_frame.rowconfigure(i, weight=1, minsize=65)
        for j in range(5): grid_frame.columnconfigure(j, weight=1, minsize=70)
            
        layouts = [
            ('CHECK', 0, 0, 1, 2), ('DELETE', 0, 2, 1, 2), ('ON/AC', 0, 4, 1, 1),
            ('MU', 1, 0, 1, 1),    ('7', 1, 1, 1, 1),      ('8', 1, 2, 1, 1),    ('9', 1, 3, 1, 1), ('%', 1, 4, 1, 1),
            ('+/-', 2, 0, 1, 1),   ('4', 2, 1, 1, 1),      ('5', 2, 2, 1, 1),    ('6', 2, 3, 1, 1), ('÷', 2, 4, 1, 1),
            ('√', 3, 0, 1, 1),     ('1', 3, 1, 1, 1),      ('2', 3, 2, 1, 1),    ('3', 3, 3, 1, 1), ('×', 3, 4, 1, 1),
            ('M+', 4, 0, 1, 1),    ('0', 4, 1, 1, 1),      ('00', 4, 2, 1, 1),   ('+', 4, 3, 2, 1), ('-', 4, 4, 1, 1),
            ('M-', 5, 0, 1, 1),    ('MR', 5, 1, 1, 1),     ('.', 5, 2, 1, 1),                       ('=', 5, 4, 1, 1)
        ]
        self.build_grid(grid_frame, layouts)

    # --- LAYOUT 2: SCIENTIFIC CALCULATOR ---
    def setup_scientific_layout(self):
        grid_frame = tk.Frame(self.buttons_container, bg=self.COLOR_BODY_BG, padx=15, pady=5)
        grid_frame.pack(expand=True, fill="both")
        
        # Menyesuaikan jumlah baris & kolom scientific (di gambar kanan ada lebih banyak baris fungsi kecil)
        for i in range(7): grid_frame.rowconfigure(i, weight=1, minsize=55)
        for j in range(5): grid_frame.columnconfigure(j, weight=1, minsize=95)
            
        layouts = [
            # Baris Fungsi Ilmiah Atas (Ukuran Teks Agak Kecil)
            ('sin', 0, 0, 1, 1),   ('cos', 0, 1, 1, 1),    ('tan', 0, 2, 1, 1),  ('log', 0, 3, 1, 1),  ('ln', 0, 4, 1, 1),
            ('√', 1, 0, 1, 1),     ('x²', 1, 1, 1, 1),     ('(', 1, 2, 1, 1),    (')', 1, 3, 1, 1),    ('%', 1, 4, 1, 1),
            
            # Baris Angka & Operator Utama (Persis Layout Gambar Kanan)
            ('7', 2, 0, 1, 1),     ('8', 2, 1, 1, 1),      ('9', 2, 2, 1, 1),    ('ON/AC', 2, 3, 1, 1),('DEL', 2, 4, 1, 1),
            ('4', 3, 0, 1, 1),     ('5', 3, 1, 1, 1),      ('6', 3, 2, 1, 1),    ('×', 3, 3, 1, 1),    ('÷', 3, 4, 1, 1),
            ('1', 4, 0, 1, 1),     ('2', 4, 1, 1, 1),      ('3', 4, 2, 1, 1),    ('+', 4, 3, 1, 1),    ('-', 4, 4, 1, 1),
            ('0', 5, 0, 1, 1),     ('+/-', 5, 1, 1, 1),    ('.', 5, 2, 1, 1),    ('EXP', 5, 3, 1, 1),  ('=', 5, 4, 1, 1)
        ]
        self.build_grid(grid_frame, layouts)

    def build_grid(self, frame, layouts):
        for item in layouts:
            text = item[0]
            row, col = item[1], item[2]
            r_span = item[3]
            c_span = item[4]
            
            # Logika Pewarnaan Tombol agar rapi bodi putih / operator hitam arang
            if text in ['ON/AC', 'DEL', 'DELETE', '%', '÷', '×', '-', '=', 'EXP'] or (text == '+' and self.current_mode == "BASIC" and r_span == 2):
                bg_color = self.COLOR_BTN_DARK
                fg_color = "#FFFFFF"
                active_bg = "#404544"
            elif text in ['sin', 'cos', 'tan', 'log', 'ln', 'x²', '(', ')', '√', 'MU', 'CHECK', 'M+', 'M-', 'MR']:
                bg_color = "#E5E5E5" # Warna abu-abu tombol sekunder/fitur khusus
                fg_color = self.COLOR_TEXT_DARK
                active_bg = "#D6D6D6"
            else:
                bg_color = self.COLOR_BTN_WHITE
                fg_color = self.COLOR_TEXT_DARK
                active_bg = "#F5F5F5"
                
            font_size = 11 if len(text) > 3 else 14
            font_style = ("Arial", font_size, "bold")
            
            btn_border = tk.Frame(frame, bg=self.COLOR_BODY_BG)
            btn_border.grid(row=row, column=col, rowspan=r_span, columnspan=c_span, sticky="nsew", padx=4, pady=4)
            
            btn = tk.Button(btn_border, text=text, font=font_style, bg=bg_color, fg=fg_color,
                            bd=0, activebackground=active_bg, activeforeground=fg_color, relief="flat", cursor="hand2")
            btn.pack(expand=True, fill="both")
            
            btn.bind("<ButtonPress-1>", lambda event, b=btn, ab=active_bg: b.config(bg=ab))
            btn.bind("<ButtonRelease-1>", lambda event, b=btn, ob=bg_color, t=text: self.on_release_action(b, ob, t))

    def on_release_action(self, button, original_bg, text):
        button.config(bg=original_bg)
        self.process_logic(text)

    # --- LOGIKA OPERASI MATEMATIKA ---
    def process_logic(self, char):
        if char in ['ON/AC', 'C']:
            self.expression = ""
            self.lcd_screen.config(text="0")
        elif char in ['DEL', 'DELETE']:
            self.expression = self.expression[:-1]
            self.lcd_screen.config(text=self.expression if self.expression else "0")
        elif char == '=':
            try:
                prep_expr = self.expression.replace('×', '*').replace('÷', '/')
                result = eval(prep_expr)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self.lcd_screen.config(text=self.expression)
            except:
                self.lcd_screen.config(text="ERROR")
                self.expression = ""
        elif char == '√':
            try:
                val = float(self.expression) if self.expression else 0
                res = math.sqrt(val)
                self.expression = str(int(res) if res.is_integer() else res)
                self.lcd_screen.config(text=self.expression)
            except: self.lcd_screen.config(text="ERROR")
        elif char == 'x²':
            try:
                val = float(self.expression) if self.expression else 0
                res = val ** 2
                self.expression = str(int(res) if res.is_integer() else res)
                self.lcd_screen.config(text=self.expression)
            except: self.lcd_screen.config(text="ERROR")
        elif char in ['sin', 'cos', 'tan', 'log', 'ln']:
            try:
                val = float(self.expression) if self.expression else 0
                if char == 'sin': res = math.sin(math.radians(val))
                elif char == 'cos': res = math.cos(math.radians(val))
                elif char == 'tan': res = math.tan(math.radians(val))
                elif char == 'log': res = math.log10(val)
                elif char == 'ln': res = math.log(val)
                
                # Membulatkan hasil float agar rapi
                res = round(res, 6)
                if res.is_integer(): res = int(res)
                self.expression = str(res)
                self.lcd_screen.config(text=self.expression)
            except: self.lcd_screen.config(text="ERROR")
        elif char == '00':
            if self.expression and self.expression[-1].isdigit():
                self.expression += "00"
                self.lcd_screen.config(text=self.expression)
        elif char in ['M+', 'M-', 'MR', 'CHECK', 'MU', '+/-', 'EXP']:
            pass 
        else:
            if self.expression == "0" and char.isdigit():
                self.expression = str(char)
            else:
                self.expression += str(char)
            
            display_show = self.expression.replace('*', '×').replace('/', '÷')
            if len(display_show) > 12: display_show = display_show[-12:]
            self.lcd_screen.config(text=display_show)

if __name__ == "__main__":
    root = tk.Tk()
    app = DualModeCalculator(root)
    root.mainloop()