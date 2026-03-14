import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pairing.file_handler import load_data
from pairing.matcher import pair_sisters
from pairing.exporter import export_to_excel


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Big Sister – Little Sister Pairing")
        self.geometry("700x560")
        self.resizable(True, True)
        self.big_sis_data = None
        self.lil_sis_data = None
        self.pairs_df = None
        self._create_widgets()

    def _create_widgets(self):
        # Header
        tk.Label(
            self,
            text="Big Sister – Little Sister Pairing",
            font=("Helvetica", 14, "bold")
        ).pack(pady=(20, 10))

        # File upload row
        upload_frame = tk.Frame(self)
        upload_frame.pack(pady=5)

        self.big_sis_label = tk.Label(upload_frame, text="No file loaded", fg="grey", width=30, anchor="w")
        self.lil_sis_label = tk.Label(upload_frame, text="No file loaded", fg="grey", width=30, anchor="w")

        tk.Label(upload_frame, text="Big Sister file:").grid(row=0, column=0, padx=5, sticky="e")
        tk.Button(upload_frame, text="Choose File", command=self._load_big_sis_file).grid(row=0, column=1, padx=5)
        self.big_sis_label.grid(row=0, column=2, padx=5)

        tk.Label(upload_frame, text="Little Sister file:").grid(row=1, column=0, padx=5, pady=8, sticky="e")
        tk.Button(upload_frame, text="Choose File", command=self._load_lil_sis_file).grid(row=1, column=1, padx=5)
        self.lil_sis_label.grid(row=1, column=2, padx=5)

        # Pair button
        tk.Button(
            self,
            text="Pair Big Sisters and Little Sisters",
            command=self._run_pairing,
            font=("Helvetica", 11),
            pady=6,
        ).pack(pady=10)

        # Results table
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 5))

        columns = ("big_sister", "little_sister", "match_score")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree.heading("big_sister", text="Big Sister")
        self.tree.heading("little_sister", text="Little Sister")
        self.tree.heading("match_score", text="Match Score")
        self.tree.column("big_sister", width=220)
        self.tree.column("little_sister", width=220)
        self.tree.column("match_score", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Export button (disabled until results exist)
        self.export_btn = tk.Button(
            self,
            text="Export to Excel",
            command=self._export_results,
            state=tk.DISABLED,
        )
        self.export_btn.pack(pady=(0, 15))

    # ------------------------------------------------------------------ #
    #  File loading
    # ------------------------------------------------------------------ #

    def _load_file(self, role: str) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        data = load_data(file_path)
        if data is None:
            messagebox.showerror("Error", f"Failed to load {role} file.")
            return

        short_name = file_path.split("/")[-1]

        if role == "Big Sister":
            self.big_sis_data = data
            self.big_sis_label.config(text=f"{short_name} ({len(data)} records)", fg="green")
        else:
            self.lil_sis_data = data
            self.lil_sis_label.config(text=f"{short_name} ({len(data)} records)", fg="green")

    def _load_big_sis_file(self):
        self._load_file("Big Sister")

    def _load_lil_sis_file(self):
        self._load_file("Little Sister")

    # ------------------------------------------------------------------ #
    #  Pairing
    # ------------------------------------------------------------------ #

    def _run_pairing(self):
        if self.big_sis_data is None or self.lil_sis_data is None:
            messagebox.showerror("Error", "Please load both files before pairing.")
            return

        try:
            pairs_df, _ = pair_sisters(self.big_sis_data, self.lil_sis_data)
            self.pairs_df = pairs_df
            self._populate_table(pairs_df)
            self.export_btn.config(state=tk.NORMAL)
            messagebox.showinfo(
                "Pairing Complete",
                f"{len(pairs_df)} pairs created successfully."
            )
        except Exception as e:
            messagebox.showerror("Pairing Error", str(e))

    def _populate_table(self, pairs_df):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in pairs_df.iterrows():
            self.tree.insert("", tk.END, values=(
                row["big_sister"],
                row["little_sister"],
                row["match_score"],
            ))

    # ------------------------------------------------------------------ #
    #  Export
    # ------------------------------------------------------------------ #

    def _export_results(self):
        if self.pairs_df is None:
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="pairing_results.xlsx",
        )
        if not save_path:
            return

        try:
            export_to_excel(self.pairs_df, save_path)
            messagebox.showinfo("Exported", f"Results saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))