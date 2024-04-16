import tkinter as tk
from tkinter import ttk

class TkinterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Train Dataset")
        self.geometry("400x300+100+100")
        self.create_widgets()

    def create_widgets(self):
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        buttons = ["Home", "Search", "Classify", "Train", "Export", "Detect"]
        for button_text in buttons:
            tk.Button(left_frame, text=button_text, width=15).pack(side=tk.TOP, pady=5, fill=tk.X)

        # Frame for the center widgets
        center_frame = tk.Frame(self)
        center_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Spinbox for integer input
        integer_spinbox = ttk.Spinbox(center_frame, from_=0, to=100, width=10)
        integer_spinbox.pack(pady=5)

        # Spinbox for decimal input
        decimal_spinbox = ttk.Spinbox(center_frame, from_=0.9, to=0.97, increment=0.01, format="%.2f", width=10)
        decimal_spinbox.pack(pady=5)

        # Button for "Train Dataset"
        train_dataset_button = ttk.Button(center_frame, text="Train Dataset")
        train_dataset_button.pack(pady=10)

def train_main():
    app = TkinterApp()
    app.mainloop()

if __name__ == "__main__":
    train_main()
