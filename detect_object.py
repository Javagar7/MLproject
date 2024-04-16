import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Processing App")
        self.geometry("600x400+100+100")
        self.create_widgets()

    def create_widgets(self):
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        buttons = ["Home", "Search", "Classify", "Train", "Export", "Detect"]
        for button_text in buttons:
            tk.Button(left_frame, text=button_text, width=15).pack(side=tk.TOP, pady=5, fill=tk.X)

        # Top center frame for search box and detect button
        top_center_frame = tk.Frame(self)
        top_center_frame.pack(anchor=tk.N, padx=20, pady=20)

        # Search box
        self.search_entry = tk.Entry(top_center_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Detect button
        detect_button = ttk.Button(top_center_frame, text="Detect", command=self.detect_image)
        detect_button.pack(side=tk.LEFT)

        # Frame for displaying images
        image_frame = tk.Frame(self)
        image_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Image display area for selected image
        self.selected_image_label = tk.Label(image_frame, text="Selected Image", relief=tk.GROOVE, width=25, height=10)
        self.selected_image_label.pack(anchor=tk.W)

        # Image display area for detected images
        self.detected_images_label = tk.Label(image_frame, text="Detected Images", relief=tk.GROOVE, width=25, height=10)
        self.detected_images_label.pack(anchor=tk.W)

        # Frame for all detected images
        all_detected_frame = tk.Frame(self)
        all_detected_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Label for all detected images
        tk.Label(all_detected_frame, text="All Detected Images").pack(anchor=tk.W)

        # Scrollbar for detected images
        scrollbar = tk.Scrollbar(all_detected_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox to display all detected images
        self.detected_images_listbox = tk.Listbox(all_detected_frame, yscrollcommand=scrollbar.set, width=30, height=10)
        self.detected_images_listbox.pack(pady=(5, 0))

        # Attach scrollbar to listbox
        scrollbar.config(command=self.detected_images_listbox.yview)

    def detect_image(self):
        # Get image from search box and display in selected image box
        image_name = self.search_entry.get()
        # Perform detection and update detected images label
        self.detected_images_label.config(text=f"Detected Images for {image_name}")
        # Clear previously detected images
        self.detected_images_listbox.delete(0, tk.END)
        # Simulating detection results
        for i in range(5):
            self.detected_images_listbox.insert(tk.END, f"Detected Image {i+1}")

def detect_main():
    app = Application()
    app.mainloop()

# Entry point of the application
if __name__ == "__main__":
    detect_main()
