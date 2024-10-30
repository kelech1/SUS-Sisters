# ui/app_ui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from pairing.file_handler import load_data

class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Big Sister-Little Sister Pairing")
        self.geometry("600x400")
        self.bigSis_file = None
        self.lilSis_file = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Big Sister-Little Sister Pairing Application").pack(pady=20)

        tk.Label(self, text="Upload Big Sister File:").pack()
        tk.Button(self, text="Choose File", command=self.load_bigSis_file).pack(pady=5)

        tk.Label(self, text="Upload Little Sister File:").pack()
        tk.Button(self, text="Choose File", command=self.load_lilSis_file).pack(pady=5)

        tk.Button(self, text="Pair Big Sisters and Little Sisters", command=self.pair_bigSis_lilSis).pack(pady=20)

    def load_bigSis_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.bigSis_file = load_data(file_path)
            if self.bigSis_file is not None:
                messagebox.showinfo("File Loaded", f"Loaded Big Sister file: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to load Big Sister file.")

    def load_lilSis_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.lilSis_file = load_data(file_path)
            if self.lilSis_file is not None:
                messagebox.showinfo("File Loaded", f"Loaded Little Sister file: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to load Little Sister file.")

    def pair_bigSis_lilSis(self):
        if self.bigSis_file is None or self.lilSis_file is None:
            messagebox.showerror("Error", "Please load both Big Sister and Little Sister files.")
            return
        print("Proceeding with pairing process...")
