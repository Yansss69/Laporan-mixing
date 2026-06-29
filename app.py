main.py
import customtkinter as ctk
from datetime import datetime, timedelta
import pandas as pd
from tkinter import messagebox
from PIL import Image

# --- KONFIGURASI FONT & TEMA ---
FONT_UTAMA = ("Segoe UI Variable", 48, "bold")
FONT_INPUT = ("Segoe UI Variable", 32)
FONT_DATA  = ("Cascadia Code", 24)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PRODUCTION MONITOR - SACHET LINE")
        self.geometry("1000x1200") 
        self.grid_columnconfigure(0, weight=1)

        # Logo otomatis
        try:
            logo_path = "logo.png"
            self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path), dark_image=Image.open(logo_path), size=(150, 150))
            ctk.CTkLabel(self, text="", image=self.logo_image).pack(pady=15)
        except: 
            pass

        ctk.CTkLabel(self, text="LINE SACHET MONITOR", font=FONT_UTAMA, text_color="#38bdf8").pack(pady=10)

        # Input Form
        self.entry_op = ctk.CTkEntry(self, placeholder_text="Nama Operator", height=90, font=FONT_INPUT, corner_radius=20)
        self.entry_op.pack(fill="x", padx=80, pady=10)
        
        self.combo_shift = ctk.CTkComboBox(self, values=["Shift 1 (Pagi)", "Shift 2 (Siang)", "Shift 3 (Malam)"], height=90, font=FONT_INPUT, corner_radius=20)
        self.combo_shift.pack(fill="x", padx=80, pady=10)

        self.entry_start = ctk.CTkEntry(self, placeholder_text="Jam Mulai (HH:MM)", height=90, font=FONT_INPUT, corner_radius=20)
        self.entry_start.pack(fill="x", padx=80, pady=10)

        self.seg_durasi = ctk.CTkSegmentedButton(self, values=["40 Min", "50 Min"], height=70, font=FONT_INPUT, corner_radius=20)
        self.seg_durasi.set("50 Min")
        self.seg_durasi.pack(fill="x", padx=80, pady=10)

        # TabView Data
        self.tabview = ctk.CTkTabview(self, height=350, segmented_button_font=FONT_INPUT, corner_radius=20)
        self.tabview.pack(fill="both", expand=True, padx=80, pady=10)
        
        self.txt1 = ctk.CTkTextbox(self.tabview.add("3m + 12m"), font=FONT_DATA)
        self.txt1.pack(fill="both", expand=True, padx=20, pady=20)
        self.txt2 = ctk.CTkTextbox(self.tabview.add("Proses"), font=FONT_DATA)
        self.txt2.pack(fill="both", expand=True, padx=20, pady=20)
        self.txt3 = ctk.CTkTextbox(self.tabview.add("Hasil"), font=FONT_DATA)
        self.txt3.pack(fill="both", expand=True, padx=20, pady=20)

        # Tombol Aksi
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=80, pady=10)
        ctk.CTkButton(btn_frame, text="➕ TAMBAH", command=self.tambah_log, height=100, corner_radius=30, font=("Segoe UI Variable", 36, "bold")).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(btn_frame, text="🔄 RESET", fg_color="#ef4444", hover_color="#b91c1c", command=self.reset_app, height=100, width=200, corner_radius=30, font=("Segoe UI Variable", 36, "bold")).pack(side="right")
        
        ctk.CTkButton(self, text="💾 EXPORT EXCEL", fg_color="#10b981", hover_color="#059669", command=self.simpan_excel, height=100, corner_radius=30, font=("Segoe UI Variable", 36, "bold")).pack(fill="x", padx=80, pady=10)

    # --- LOGIKA APLIKASI ---
    def reset_app(self):
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus semua log?"):
            for t in [self.txt1, self.txt2, self.txt3]: t.delete("1.0", "end")
            self.entry_start.delete(0, "end")

    def tambah_log(self):
        try:
            t_start = datetime.strptime(self.entry_start.get().strip(), "%H:%M")
            durasi = int(self.seg_durasi.get().replace(" Min", ""))
            t1 = t_start + timedelta(minutes=3)
            t2 = t1 + timedelta(minutes=12)
            t3 = t2 + timedelta(minutes=3)
            t_end = t_start + timedelta(minutes=durasi)
            self.txt1.insert("end", f"{t_start.strftime('%H:%M')} | {t1.strftime('%H:%M')} | {t2.strftime('%H:%M')} | {t3.strftime('%H:%M')}\n")
            self.txt2.insert("end", f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}\n")
            self.txt3.insert("end", f"{t_start.strftime('%H:%M')} - {t_end.strftime('%H:%M')}\n")
            self.entry_start.delete(0, "end"); self.entry_start.insert(0, t3.strftime("%H:%M"))
        except: messagebox.showerror("Error", "Format jam salah! (HH:MM)")

    def simpan_excel(self):
        log1, log2, log3 = self.txt1.get("1.0", "end-1c").splitlines(), self.txt2.get("1.0", "end-1c").splitlines(), self.txt3.get("1.0", "end-1c").splitlines()
        if not log1: return messagebox.showwarning("Info", "Data kosong!")
        try:
            max_len = max(len(log1), len(log2), len(log3))
            df = pd.DataFrame({
                "Operator": self.entry_op.get(), "Shift": self.combo_shift.get(),
                "3m + 12m": log1 + [None]*(max_len-len(log1)),
                "Proses": log2 + [None]*(max_len-len(log2)),
                "Hasil": log3 + [None]*(max_len-len(log3))
            })
            filename = f"Log_Produksi_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            df.to_excel(filename, index=False)
            messagebox.showinfo("Sukses", f"Data tersimpan di {filename}!")
        except Exception as e: messagebox.showerror("Gagal", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()