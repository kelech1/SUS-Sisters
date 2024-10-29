import tkinter as tk

class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StepUp Sorority Pairing")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Placeholder label and buttons for file upload
        tk.Label(self, text="Big Sister - Little Sister Pairing Application").pack(pady=20)

        tk.Label(self, text="Upload Big Sister File:").pack()
        tk.Button(self, text="Choose File", command=self.load_bigSis_file).pack(pady=5)

        tk.Label(self, text="Upload Little Sister File:").pack()
        tk.Button(self, text="Choose File", command=self.load_lilSis_file).pack(pady=5)

        tk.Button(self, text="Pair Big Sister and LittleSisters", command=self.pair_bigSis_lilSis).pack(pady=20)

    def load_bigSis_file(self):
        # Placeholder function for loading bigSis file
        print("Big Sister file loading...")

    def load_lilSis_file(self):
        # Placeholder function for loading lilSis file
        print("Little Sister file loading...")

    def pair_bigSis_lilSis(self):
        # Placeholder function for pairing
        print("Pairing big Sisters to little Sisters...")
