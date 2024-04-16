import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.simpledialog import askinteger

from annotate_image import *
from image_classifier import classify_main
from image_downloader_gui import *
from image_downloader import *
from image_classifier import *
from vAnnotate import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main

def annotate(image_path):
    print("Annotating image:")
    
    r=tk.Tk()
    app1 = MyApp(r,image_path)
    r.mainloop()

def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            images.append(image_path)
    return images

class ImageGalleryApp:
    def __init__(self, master, image_directory):
        self.master = master
        self.image_directory = image_directory
        self.images = load_images(image_directory)
        self.current_image_index = 0

        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.button_functions = {
            "Home": self.open_home_window,
            "Search": self.search,
            "Classify": self.classify,
            "Train": self.open_train_window,
            "Export": self.open_export_window,
            "Detect": self.open_detect_window,
        }

        self.show_images()
        
        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(self.bottom_frame, text="Preprocessing", command=self.data).pack(pady=10)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(self.bottom_frame, text="Separate Images", command=self.ask_move_images).pack(pady=10)

    def show_images(self):
        num_cols = 4
        for i, image_path in enumerate(self.images):
            row = i // num_cols
            col = i % num_cols

            image = Image.open(image_path)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(self.frame, image=photo)
            label.image = photo
            label.grid(row=row, column=col, padx=5, pady=5)

            label.bind("<Button-1>", lambda event, path=image_path: self.on_image_click(path))

        self.frame.update()  # Update the frame
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Update the canvas scroll region

    def on_image_click(self, image_path):
        self.master.destroy()
        annotate(image_path)

    def open_home_window(self):
        self.master.destroy()
        vAnnotate_main()

    def open_train_window(self):
        self.master.destroy()
        train_main()

    def open_export_window(self):
        self.master.destroy()
        export_main()

    def open_detect_window(self):
        self.master.destroy()
        detect_main()

    def search(self):
        self.master.destroy()
        image_gui_main(self.image_directory)

    def classify(self):
        self.master.destroy()
        classify_main(self.image_directory)
    
    def ask_move_images(self):
        percent = askinteger("Percent of Images", "Enter the percentage of images to move to the VALID folder:")
        if percent is not None:
            self.move_images(percent)
    
    def data(self):
        img=(os.path.dirname(os.path.dirname(self.image_directory)))
        txt_train=os.path.join(img,'train.txt')
        txt_valid=os.path.join(img,'valid.txt')
        img_train=os.path.join(img,'Image','Train')
        img_valid=os.path.join(img,'Image','valid')
        image_paths = []
        for root, _, files in os.walk(img_train):
            for file in files:
                # Check if the file is an image (you can add more extensions if needed)
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(root, file)
                    image_paths.append(image_path)

    # Write the image paths to a text file
        
        with open(txt_train, 'w') as f:
            for path in image_paths:
                f.write(path + '\n')
        print(img)
        image_paths = []
        for root, _, files in os.walk(img_valid):
            for file in files:
                # Check if the file is an image (you can add more extensions if needed)
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(root, file)
                    image_paths.append(image_path)

    # Write the image paths to a text file
        
        with open(txt_valid, 'w') as f:
            for path in image_paths:
                f.write(path + '\n')
        print(img)
    
    def move_images(self, percent):
        # Check if there are already enough images in the Valid folder
        valid_folder = self.image_directory.replace('Train', 'Valid')
        num_valid_images = len([filename for filename in os.listdir(valid_folder) if filename.endswith(('.jpg', '.png', '.jpeg'))])
        num_required_images = int(percent / 100 * len(self.images))

        if num_valid_images >= num_required_images:
            messagebox.showwarning("Warning", "There are already enough images in the Valid folder.")
        else:
            # Get the number of images to move
            num_to_move = num_required_images - num_valid_images
            images_to_move = self.images[:num_to_move]

            # Move images and corresponding .txt files to the Valid folder
            os.makedirs(valid_folder, exist_ok=True)

            for image_path in images_to_move:
                txt_file_path = image_path.replace('Image', 'Label').replace('.jpg', '.txt')
                new_image_path = os.path.join(valid_folder, os.path.basename(image_path))
                new_txt_file_path = os.path.join(valid_folder, os.path.basename(txt_file_path))

                # Move image
                os.rename(image_path, new_image_path)

                # Move text file if it exists
                if os.path.exists(txt_file_path):
                    os.rename(txt_file_path, new_txt_file_path)

            # Update the list of images
            self.images = self.images[num_to_move:]
            self.show_images()

def call_main(image_directory):
    root = tk.Tk()
    root.title("Image Gallery")
    root.geometry("1000x600")
    
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
    buttons = ["Home", "Search", "Classify", "Train", "Export", "Detect"]
    new_directory1 = os.path.join(image_directory,'Image')
    
    new_directory = os.path.join(new_directory1,'Train')
    app = ImageGalleryApp(root,new_directory)
    
    for button_text in buttons:
        tk.Button(left_frame, text=button_text, width=15, command=app.button_functions.get(button_text,lambda:None)).pack(side=tk.TOP, pady=5, fill=tk.X)
    
    root.mainloop()
    
if __name__ == "__main__":
    call_main(image_directory="Parent/Dataset/cricket/Image/Train")

"""import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.simpledialog import askinteger

from annotate_image import *
from image_classifier import classify_main
from image_downloader_gui import *
from image_downloader import *
from image_classifier import *
from vAnnotate import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main

def annotate(image_path):
    print("Annotating image:")
    
    r=tk.Tk()
    app1 = MyApp(r,image_path)
    r.mainloop()

def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            images.append(image_path)
    return images

class ImageGalleryApp:
    def __init__(self, master, image_directory):
        self.master = master
        self.image_directory = image_directory
        self.images = load_images(image_directory)
        self.current_image_index = 0

        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.button_functions = {
            "Home": self.open_home_window,
            "Search": self.search,
            "Classify": self.classify,
            "Train": self.open_train_window,
            "Export": self.open_export_window,
            "Detect": self.open_detect_window,
        }

        self.show_images()
        
        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.bottom_frame, text="Separate Images", command=self.ask_move_images).pack(pady=10)

    def show_images(self):
        num_cols = 4
        for i, image_path in enumerate(self.images):
            row = i // num_cols
            col = i % num_cols

            image = Image.open(image_path)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(self.frame, image=photo)
            label.image = photo
            label.grid(row=row, column=col, padx=5, pady=5)

            label.bind("<Button-1>", lambda event, path=image_path: self.on_image_click(path))

        self.frame.update()  # Update the frame
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Update the canvas scroll region

    def on_image_click(self, image_path):
        self.master.destroy()
        annotate(image_path)

    def open_home_window(self):
        self.master.destroy()
        vAnnotate_main()

    def open_train_window(self):
        self.master.destroy()
        train_main()

    def open_export_window(self):
        self.master.destroy()
        export_main()

    def open_detect_window(self):
        self.master.destroy()
        detect_main()

    def search(self):
        self.master.destroy()
        image_gui_main(self.image_directory)

    def classify(self):
        self.master.destroy()
        classify_main(self.image_directory)
    
    def ask_move_images(self):
        percent = askinteger("Percent of Images", "Enter the percentage of images to move to the VALID folder:")
        if percent is not None:
            self.move_images(percent)
    
    def move_images(self, percent):
        # Check if there are already enough images in the Valid folder
        valid_folder = self.image_directory.replace('Train', 'Valid')
        num_valid_images = len([filename for filename in os.listdir(valid_folder) if filename.endswith(('.jpg', '.png', '.jpeg'))])
        num_required_images = int(percent / 100 * len(self.images))

        if num_valid_images >= num_required_images:
            messagebox.showwarning("Warning", "There are already enough images in the Valid folder.")
        else:
            # Get the number of images to move
            num_to_move = num_required_images - num_valid_images
            images_to_move = self.images[:num_to_move]

            # Move images and corresponding .txt files to the Valid folder
            os.makedirs(valid_folder, exist_ok=True)

            for image_path in images_to_move:
                txt_file_path = image_path.replace('Image', 'Label').replace('.jpg', '.txt')
                new_image_path = os.path.join(valid_folder, os.path.basename(image_path))
                new_txt_file_path = os.path.join(valid_folder, os.path.basename(txt_file_path))

                # Move image
                os.rename(image_path, new_image_path)

                # Move text file if it exists
                if os.path.exists(txt_file_path):
                    os.rename(txt_file_path, new_txt_file_path)

            # Update the list of images
            self.images = self.images[num_to_move:]
            self.show_images()

def call_main(image_directory):
    root = tk.Tk()
    root.title("Image Gallery")
    root.geometry("1000x600")
    
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
    buttons = ["Home", "Search", "Classify", "Train", "Export", "Detect"]
    new_directory1 = os.path.join(image_directory,'Image')
    
    new_directory = os.path.join(new_directory1,'Train')
    app = ImageGalleryApp(root,new_directory)
    
    for button_text in buttons:
        tk.Button(left_frame, text=button_text, width=15, command=app.button_functions.get(button_text,lambda:None)).pack(side=tk.TOP, pady=5, fill=tk.X)
    
    root.mainloop()
    
if __name__ == "__main__":
    call_main(image_directory="Parent/Dataset/cricket/Image/Train")"""











"""import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox

from annotate_image import *
from image_classifier import classify_main
from image_downloader_gui import *
from image_downloader import *
from image_classifier import *
from vAnnotate import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main

def annotate(image_path):
    print("Annotating image:")
    
    r=tk.Tk()
    app1 = MyApp(r,image_path)
    r.mainloop()

def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            images.append(image_path)
    return images

class ImageGalleryApp:
    def __init__(self, master, image_directory):
        self.master = master
        self.image_directory = image_directory
        self.images = load_images(image_directory)
        self.current_image_index = 0

        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.button_functions = {
            "Home": self.open_home_window,
            "Search": self.search,
            "Classify": self.classify,
            "Train": self.open_train_window,
            "Export": self.open_export_window,
            "Detect": self.open_detect_window,
        }

        self.show_images()
        
        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(self.bottom_frame, text="Separate Images", command=self.separate_images).pack(side=tk.BOTTOM, pady=10)

    def show_images(self):
        num_cols = 4
        for i, image_path in enumerate(self.images):
            row = i // num_cols
            col = i % num_cols

            image = Image.open(image_path)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(self.frame, image=photo)
            label.image = photo
            label.grid(row=row, column=col, padx=5, pady=5)

            label.bind("<Button-1>", lambda event, path=image_path: self.on_image_click(path))

        self.frame.update()  # Update the frame
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Update the canvas scroll region

    def on_image_click(self, image_path):
        self.master.destroy()
        annotate(image_path)

    def open_home_window(self):
        self.master.destroy()
        vAnnotate_main()

    def open_train_window(self):
        self.master.destroy()
        train_main()

    def open_export_window(self):
        self.master.destroy()
        export_main()

    def open_detect_window(self):
        self.master.destroy()
        detect_main()

    def search(self):
        self.master.destroy()
        image_gui_main(self.image_directory)

    def classify(self):
        self.master.destroy()
        classify_main(self.image_directory)
    
    def separate_images(self):
        # Check if there are already enough images in the Valid folder
        
        valid_folder = self.image_directory.replace('Train', 'Valid')
        num_valid_images = len([filename for filename in os.listdir(valid_folder) if filename.endswith(('.jpg', '.png', '.jpeg'))])
        num_required_images = int(0.2 * len(self.images))

        if num_valid_images >= num_required_images:
            messagebox.showwarning("warning","There are already enough images in the Valid folder")
        else:
            # Get 20% of the images
            num_images = len(self.images)
            num_to_move = num_required_images - num_valid_images
            images_to_move = self.images[:num_to_move]

            # Move images and corresponding .txt files to the Valid folder
            os.makedirs(valid_folder, exist_ok=True)

            for image_path in images_to_move:
                txt_file_path = image_path.replace('Image', 'Label').replace('.jpg', '.txt')
                new_image_path = os.path.join(valid_folder, os.path.basename(image_path))
                new_txt_file_path = os.path.join(valid_folder, os.path.basename(txt_file_path))

                # Move image
                os.rename(image_path, new_image_path)

                # Move text file if it exists
                if os.path.exists(txt_file_path):
                    os.rename(txt_file_path, new_txt_file_path)

            # Update the list of images
            self.images = self.images[num_to_move:]
            self.show_images()

def call_main(image_directory):
    root = tk.Tk()
    root.title("Image Gallery")
    root.geometry("1000x600")
    
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
    buttons = ["Home", "Search", "Classify", "Train", "Export", "Detect"]
    new_directory1 = os.path.join(image_directory,'Image')
    
    new_directory = os.path.join(new_directory1,'Train')
    app = ImageGalleryApp(root,new_directory)
    
    for button_text in buttons:
        tk.Button(left_frame, text=button_text, width=15, command=app.button_functions.get(button_text,lambda:None)).pack(side=tk.TOP, pady=5, fill=tk.X)
    
    root.mainloop()
    
if __name__ == "__main__":
    call_main(image_directory="Parent/Dataset/cricket/Image/Train")


"""