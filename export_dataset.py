import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Export Dataset")
        self.geometry("500x300+100+100")
        self.create_widgets()
    
    def create_widgets(self):
        
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        buttons = ["Home", "Search", "Classify", "Train", "Export", "Detect"]
        for button_text in buttons:
            tk.Button(left_frame, text=button_text, width=15).pack(side=tk.TOP, pady=5, fill=tk.X)
        
        # Create a frame for the center widgets
        self.center_frame = tk.Frame(self)
        self.center_frame.pack(side=tk.LEFT, padx=40, pady=20, expand=True)
        
        # Entry widget for text input
        self.input_text = tk.StringVar()
        self.text_entry = ttk.Entry(self.center_frame, textvariable=self.input_text, width=30)
        self.text_entry.pack(pady=10)
        
        # Button for "Export Dataset"
        self.export_dataset_button = ttk.Button(self.center_frame, text="Export Dataset")
        self.export_dataset_button.pack(pady=20)

def export_main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    export_main()
