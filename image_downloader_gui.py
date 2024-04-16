import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os

import image_downloader
from vAnnotate import *
from image_classifier import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main

class ImageDownloaderApp:
    def __init__(self, master, image_path):
        self.master = master
        self.image_path = image_path

        # Left Sidebar with six buttons
        left_frame = tk.Frame(master)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        buttons = ["Home", "Search", "Classify", "Train", "Export", "Detect"]
        for button_text, command in [("Home", self.home),
                                     ("Search", self.search),
                                     ("Classify", self.classify),
                                     ("Train", self.train),
                                     ("Export", self.export),
                                     ("Detect", self.detect)]:
            tk.Button(left_frame, text=button_text, width=15, command=command).pack(side=tk.TOP, pady=5, fill=tk.X)

        # Create a frame for the search and download buttons
        search_download_frame = ttk.Frame(master)
        search_download_frame.pack(pady=10)

        self.query_label = ttk.Label(search_download_frame, text="Query:")
        self.query_label.grid(row=0, column=0)
        self.query_entry = ttk.Entry(search_download_frame)
        self.query_entry.grid(row=0, column=1, padx=(0, 10))

        num_images_label = ttk.Label(search_download_frame, text="Number of Images:")
        num_images_label.grid(row=0, column=2)
        self.num_images_entry = ttk.Entry(search_download_frame)
        self.num_images_entry.grid(row=0, column=3, padx=(0, 10))

        search_button = ttk.Button(search_download_frame, text="Search", command=self.search_function)
        search_button.grid(row=0, column=4, padx=(0, 10))

        # Create a frame for the image display
        image_frame = ttk.Frame(master)
        image_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas widget for scrollable image display
        self.image_canvas = tk.Canvas(image_frame, width=320, height=480)
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(image_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_canvas.configure(yscrollcommand=scrollbar.set)

    def home(self):
        self.master.destroy()
        vAnnotate_main()

    def search(self):
        print("Search button clicked")
        

    def classify(self):
        self.master.destroy()
        classify_main(self.image_path) 

    def train(self):
        self.master.destroy()
        train_main()
        

    def export(self):
        self.master.destroy()
        export_main()
        

    def detect(self):
        self.master.destroy()
        detect_main()
        

    def search_function(self):
        query = self.query_entry.get()
        num_images = int(self.num_images_entry.get())
        image_folder = self.image_path
        image_downloader.run(query, image_folder, num_images=num_images)
        
        if not os.path.exists(image_folder) or not os.listdir(image_folder):
            # Images folder is empty
            self.query_label.config(text="No images found")
            return

        # Clear existing items in the canvas
        for widget in self.image_canvas.winfo_children():
            widget.destroy()

        image_files = os.listdir(image_folder)
        # Filter out non-image files
        image_files = [file for file in image_files if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

        if not image_files:
            # No images found in the folder
            self.query_label.config(text="No images found")
            return

        # Display all images in the folder
        for i, image_file in enumerate(image_files):
            try:
                image_url = os.path.join(image_folder, image_file)
                image = Image.open(image_url)
                image = image.resize((300, 300))  # Resize the image
                photo = ImageTk.PhotoImage(image)
                # Create a new label for each image
                image_label = ttk.Label(self.image_canvas, image=photo, text=f"Image {i+1}")
                image_label.image = photo  # Keep a reference to the image
                self.image_canvas.create_window(0, i*320, anchor=tk.NW, window=image_label)
            except Exception as e:
                print(f"Error loading image {image_file}: {e}")

        # Update the scroll region of the canvas
        self.image_canvas.update_idletasks()  # Update the canvas to get the correct frame height
        canvas_height = len(image_files) * 320  # Calculate the total height of the content
        self.image_canvas.config(scrollregion=(0, 0, 320, canvas_height))  # Set the scroll region

def image_gui_main(image_path):
    root = tk.Tk()
    root.title("Search Image")
    root.geometry("1000x600")

    app = ImageDownloaderApp(root, image_path)
    root.mainloop()
   

