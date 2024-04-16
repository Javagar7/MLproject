import os
import json
import subprocess
from tkinter import Tk, Listbox, Button, StringVar, messagebox, Frame, Label, TOP, Canvas, Scrollbar
from PIL import Image, ImageTk
import shutil

from list_images import *
from annotate_image import *
from vAnnotate import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main

class ImageClassifierApp:
    def __init__(self, root, config):
        self.root = root
        self.root.title("Image Classifier")
        self.root.geometry("1000x600")
        
        # Left Sidebar with six buttons
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        buttons = ["Search", "Annotate", "Classify", "Train", "Export", "Detect"]
        for button_text in buttons:
            tk.Button(self.left_frame, text=button_text, width=15).pack(side=tk.TOP, pady=5, fill=tk.X)

        self.train_folder = config["train_folder"]
        self.valid_folder = config["valid_folder"]
        self.test_folder = config["test_folder"]

        # Load information about images from the "info.txt" file
        self.load_image_info()
        
        self.create_frames()
        
        self.create_listboxes()
        
        self.bind_listbox_select()
        
    def create_frames(self):
        self.train_frame = Frame(self.root)
        self.train_frame.pack(side="left", anchor="nw", padx=10, pady=10)
            
        self.test_frame = Frame(self.root)
        self.test_frame.pack(side="left", anchor="nw", padx=10, pady=10)
            
        self.valid_frame = Frame(self.root)
        self.valid_frame.pack(side="left", anchor="nw", padx=10, pady=10)
            
            
    def create_listboxes(self):
        self.train_label = Label(self.train_frame, text="Train Folder")
        self.train_label.pack()
        self.train_listbox = Listbox(self.train_frame, selectmode="SINGLE", width=50, height=100)
        self.train_listbox.pack(side="left", fill="both", expand=True)
        self.populate_listbox(self.train_listbox, self.train_folder)
            
        self.train_nav_frame = Frame(self.train_frame)
        self.train_nav_frame.pack(side="left", padx=(10,0))
        self.train_nav_buttons = {
            ">": lambda: self.move_to_folder(self.test_folder),
            "<": lambda: self.move_to_folder(self.train_folder),
            ">>": lambda: self.move_to_folder(self.valid_folder)
        }
        for button_text, command in self.train_nav_buttons.items():
            button = Button(self.train_nav_frame, text=button_text, command=command)
            button.pack()

        self.test_label = Label(self.test_frame, text="Test Folder")
        self.test_label.pack()
        self.test_listbox = Listbox(self.test_frame, selectmode="SINGLE", width=50, height=100)
        self.test_listbox.pack(side="left", fill="both", expand=True)
        self.populate_listbox(self.test_listbox, self.test_folder)

        self.test_nav_frame = Frame(self.test_frame)
        self.test_nav_frame.pack(side="left", padx=(10,0))
        self.test_nav_buttons = {
            ">": lambda: self.move_to_folder(self.valid_folder),
            "<": lambda: self.move_to_folder(self.test_folder),
            "<<": lambda: self.move_to_folder(self.train_folder)
        }
        for button_text, command in self.test_nav_buttons.items():
            button = Button(self.test_nav_frame, text=button_text, command=command)
            button.pack()

        self.valid_label = Label(self.valid_frame, text="Valid Folder")
        self.valid_label.pack()
        self.valid_listbox = Listbox(self.valid_frame, selectmode="SINGLE", width=50, height=100)
        self.valid_listbox.pack(side="left", fill="both", expand=True)
        self.populate_listbox(self.valid_listbox, self.valid_folder)
            
            
    def bind_listbox_select(self):
        self.train_listbox.bind("<<ListboxSelect>>", lambda event: self.on_listbox_select(event, self.train_listbox))
        self.test_listbox.bind("<<ListboxSelect>>", lambda event: self.on_listbox_select(event, self.test_listbox))
        self.valid_listbox.bind("<<ListboxSelect>>", lambda event: self.on_listbox_select(event, self.valid_listbox))
        
    def load_image_info(self):
        try:
            with open("info.txt", "w") as info_file:
                for folder_name, folder_path in [("train", self.train_folder), ("test", self.test_folder), ("valid", self.valid_folder)]:
                    for file_name in os.listdir(folder_path):
                        if file_name.endswith((".jpg", ".jpeg", ".png", ".webp", ".avif")):
                            info_file.write(f"{folder_name},{file_name}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading image info: {e}")

    def on_label_click(self,label):
        listbox = label.master
        listbox.selection_clear(0, "end")  
        index = listbox.get(0, "end").index(label.cget("text"))  
        listbox.selection_set(index)  
        listbox.event_generate("<<ListboxSelect>>")
        
    def on_listbox_select(self, event,listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_image = listbox.get(selected_index[0])
            image_path = os.path.join(self.get_current_folder(listbox), selected_image)
            print("Selected image path:", image_path)
            
            

    def open_file(self, button_text):
        try:
            file_name = self.placeholder_buttons.get(button_text)
            if file_name:
                file_path = os.path.join(os.path.dirname(__file__), file_name)
                subprocess.Popen(["open", file_path])  # Use "open" command for macOS
            else:
                messagebox.showerror("Error", f"No file path found for {button_text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {e}")

    def populate_listbox(self, listbox, folder_path):
        listbox.delete(0, "end")  # Clear current items
        listbox.image_labels = []  # Store labels to prevent garbage collection
        image_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg", ".png", ".webp", ".avif"))]
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            image = Image.open(image_path)
            image.thumbnail((100, 100))  # Resize image to fit in listbox
            photo = ImageTk.PhotoImage(image)
            listbox.image = photo  # Save a reference to the image to prevent garbage collection
            listbox.insert("end", image_file)

            # Create a label for each image and pack it into the listbox
            label = Label(listbox, image=photo, text=image_file)
            label.image = photo  # Save reference to prevent garbage collection
            label.pack(anchor="w")
            listbox.image_labels.append(label)  # Store label reference

            # Bind click event to each label to trigger listbox selection
            label.bind("<Button-1>", lambda event, img_label=label: self.on_label_click(img_label))
            
    def clear_listbox(self, listbox):
        listbox.delete(0, "end")  
        for label in listbox.image_labels:
            label.destroy()
        listbox.image_labels = []  
    
    def refresh_listboxes(self):
        self.clear_listbox(self.train_listbox)
        self.clear_listbox(self.test_listbox)
        self.clear_listbox(self.valid_listbox)
        
        self.populate_listbox(self.train_listbox, self.train_folder)
        self.populate_listbox(self.valid_listbox, self.valid_folder)
        self.populate_listbox(self.test_listbox, self.test_folder)

    def move_to_folder(self, destination_path):
        selected_listbox = self.get_selected_listbox()
        if not selected_listbox:
            messagebox.showinfo("Error", "Please select an image.")
            return

        selected_index = selected_listbox.curselection()

        if not selected_index:
            messagebox.showinfo("Error", "Please select an image.")
            return

        selected_image = selected_listbox.get(selected_index[0])
        source_path = os.path.join(self.get_current_folder(selected_listbox), selected_image)
        image_extension = os.path.splitext(selected_image)[1].lower()
        source_txt_path = os.path.join(self.get_txt_folder(selected_listbox), selected_image.replace(image_extension, ".txt"))

        try:
            os.makedirs(destination_path, exist_ok=True)

            if os.path.exists(source_txt_path):
                destination_txt_path = os.path.join(destination_path.replace("Image", "Label"), selected_image.replace(image_extension, ".txt"))
                shutil.move(source_txt_path, destination_txt_path)

            destination_image_path = os.path.join(destination_path, selected_image)
            Image.open(source_path).save(destination_image_path)
            os.remove(source_path)
            messagebox.showinfo("Success", f"Image moved to {destination_path}")
            # Refresh listboxes after move
            self.refresh_listboxes()
        except Exception as e:
            messagebox.showinfo("Error", f"Error moving image: {e}")

    def get_txt_folder(self, listbox):
        if listbox == self.train_listbox:
            return self.train_folder.replace("Image", "Label")
        elif listbox == self.test_listbox:
            return self.test_folder.replace("Image", "Label")
        elif listbox == self.valid_listbox:
            return self.valid_folder.replace("Image", "Label")

    def get_selected_listbox(self):
        if self.train_listbox.curselection():
            return self.train_listbox
        elif self.test_listbox.curselection():
            return self.test_listbox
        elif self.valid_listbox.curselection():
            return self.valid_listbox

    def get_current_folder(self, listbox):
        if listbox == self.train_listbox:
            return self.train_folder
        elif listbox == self.test_listbox:
            return self.test_folder
        elif listbox == self.valid_listbox:
            return self.valid_folder

def classify_main(image_directory):
    root = Tk()
    
    valid_folder = image_directory.replace("Train", "Valid")
    
    test_folder = image_directory.replace("Train", "Test")

    print(image_directory)
    print(test_folder)
    print(valid_folder)

    data = {
        "train_folder": os.path.join(image_directory),
        "valid_folder": os.path.join(valid_folder),
        "test_folder": os.path.join(test_folder)
    }

    with open("config.json", "w") as f:
        json.dump(data, f)

    with open("config.json", "r") as f:
        config = json.load(f)

    app = ImageClassifierApp(root, config)
    app.load_image_info()
    root.mainloop()

    





"""import os
import json
import subprocess
from tkinter import Tk, Listbox, Button, StringVar, messagebox, Frame, Label, TOP, Canvas, Scrollbar
from PIL import Image, ImageTk
import shutil

from list_images import *
from annotate_image import *
from vAnnotate import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main

class ImageClassifierApp:
    def __init__(self, root, config):
        self.root = root
        self.root.title("Image Classifier")
        self.root.geometry("1000x600")
        
        # Left Sidebar with six buttons
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        buttons = ["Search", "Annotate", "Classify", "Train", "Export", "Detect"]
        for button_text in buttons:
            tk.Button(self.left_frame, text=button_text, width=15).pack(side=tk.TOP, pady=5, fill=tk.X)

        self.train_folder = config["train_folder"]
        self.valid_folder = config["valid_folder"]
        self.test_folder = config["test_folder"]

        # Load information about images from the "info.txt" file
        self.load_image_info()
        
        self.create_frames()
        
        self.create_listboxes()
        
        self.bind_listbox_select()
        
    def create_frames(self):
        self.train_frame = Frame(self.root)
        self.train_frame.pack(side="left", anchor="nw", padx=10, pady=10)
            
        self.test_frame = Frame(self.root)
        self.test_frame.pack(side="left", anchor="nw", padx=10, pady=10)
            
        self.valid_frame = Frame(self.root)
        self.valid_frame.pack(side="left", anchor="nw", padx=10, pady=10)
            
            
    def create_listboxes(self):
        self.train_label = Label(self.train_frame, text="Train Folder")
        self.train_label.pack()
        self.train_listbox = Listbox(self.train_frame, selectmode="SINGLE")
        self.train_listbox.pack(side="left", fill="both", expand=True)
        self.populate_listbox(self.train_listbox, self.train_folder)
            
        self.train_nav_frame = Frame(self.train_frame)
        self.train_nav_frame.pack(side="left", padx=(10,0))
        self.train_nav_buttons = {
            ">": lambda: self.move_to_folder(self.test_folder),
            "<": lambda: self.move_to_folder(self.train_folder),
            ">>": lambda: self.move_to_folder(self.valid_folder)
        }
        for button_text, command in self.train_nav_buttons.items():
            button = Button(self.train_nav_frame, text=button_text, command=command)
            button.pack()

        self.test_label = Label(self.test_frame, text="Test Folder")
        self.test_label.pack()
        self.test_listbox = Listbox(self.test_frame, selectmode="SINGLE")
        self.test_listbox.pack(side="left", fill="both", expand=True)
        self.populate_listbox(self.test_listbox, self.test_folder)

        self.test_nav_frame = Frame(self.test_frame)
        self.test_nav_frame.pack(side="left", padx=(10,0))
        self.test_nav_buttons = {
            ">": lambda: self.move_to_folder(self.valid_folder),
            "<": lambda: self.move_to_folder(self.test_folder),
            "<<": lambda: self.move_to_folder(self.train_folder)
        }
        for button_text, command in self.test_nav_buttons.items():
            button = Button(self.test_nav_frame, text=button_text, command=command)
            button.pack()

        self.valid_label = Label(self.valid_frame, text="Valid Folder")
        self.valid_label.pack()
        self.valid_listbox = Listbox(self.valid_frame, selectmode="SINGLE")
        self.valid_listbox.pack(side="left", fill="both", expand=True)
        self.populate_listbox(self.valid_listbox, self.valid_folder)
            
            
    def bind_listbox_select(self):
        self.train_listbox.bind("<<ListboxSelect>>", lambda event: self.on_listbox_select(event, self.train_listbox))
        self.test_listbox.bind("<<ListboxSelect>>", lambda event: self.on_listbox_select(event, self.test_listbox))
        self.valid_listbox.bind("<<ListboxSelect>>", lambda event: self.on_listbox_select(event, self.valid_listbox))
        
    def load_image_info(self):
        try:
            with open("info.txt", "w") as info_file:
                for folder_name, folder_path in [("train", self.train_folder), ("test", self.test_folder), ("valid", self.valid_folder)]:
                    for file_name in os.listdir(folder_path):
                        if file_name.endswith((".jpg", ".jpeg", ".png", ".webp", ".avif")):
                            info_file.write(f"{folder_name},{file_name}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading image info: {e}")

    def on_label_click(self,label):
        listbox = label.master
        listbox.selection_clear(0, "end")  
        index = listbox.get(0, "end").index(label.cget("text"))  
        listbox.selection_set(index)  
        listbox.event_generate("<<ListboxSelect>>")
        
    def on_listbox_select(self, event,listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_image = listbox.get(selected_index[0])
            image_path = os.path.join(self.get_current_folder(listbox), selected_image)
            print("Selected image path:", image_path)
            
            

    def open_file(self, button_text):
        try:
            file_name = self.placeholder_buttons.get(button_text)
            if file_name:
                file_path = os.path.join(os.path.dirname(__file__), file_name)
                subprocess.Popen(["open", file_path])  # Use "open" command for macOS
            else:
                messagebox.showerror("Error", f"No file path found for {button_text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening file: {e}")

    def populate_listbox(self, listbox, folder_path):
        listbox.delete(0, "end")  # Clear current items
        listbox.image_labels = []  # Store labels to prevent garbage collection
        image_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg", ".png", ".webp", ".avif"))]
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            image = Image.open(image_path)
            image.thumbnail((100, 100))  # Resize image to fit in listbox
            photo = ImageTk.PhotoImage(image)
            listbox.image = photo  # Save a reference to the image to prevent garbage collection
            listbox.insert("end", image_file)

            # Create a label for each image and pack it into the listbox
            label = Label(listbox, image=photo, text=image_file)
            label.image = photo  # Save reference to prevent garbage collection
            label.pack(anchor="w")
            listbox.image_labels.append(label)  # Store label reference

            # Bind click event to each label to trigger listbox selection
            label.bind("<Button-1>", lambda event, img_label=label: self.on_label_click(img_label))
            
    def clear_listbox(self, listbox):
        listbox.delete(0, "end")  
        for label in listbox.image_labels:
            label.destroy()
        listbox.image_labels = []  
    
    def refresh_listboxes(self):
        self.clear_listbox(self.train_listbox)
        self.clear_listbox(self.test_listbox)
        self.clear_listbox(self.valid_listbox)
        
        self.populate_listbox(self.train_listbox, self.train_folder)
        self.populate_listbox(self.valid_listbox, self.valid_folder)
        self.populate_listbox(self.test_listbox, self.test_folder)

    def move_to_folder(self, destination_path):
        selected_listbox = self.get_selected_listbox()
        if not selected_listbox:
            messagebox.showinfo("Error", "Please select an image.")
            return

        selected_index = selected_listbox.curselection()

        if not selected_index:
            messagebox.showinfo("Error", "Please select an image.")
            return

        selected_image = selected_listbox.get(selected_index[0])
        source_path = os.path.join(self.get_current_folder(selected_listbox), selected_image)
        image_extension = os.path.splitext(selected_image)[1].lower()
        source_txt_path = os.path.join(self.get_txt_folder(selected_listbox), selected_image.replace(image_extension, ".txt"))

        try:
            os.makedirs(destination_path, exist_ok=True)
            destination_image_path = os.path.join(destination_path, selected_image)
            destination_txt_path = os.path.join(destination_path.replace("Image", "Label"), selected_image.replace(image_extension, ".txt"))
            Image.open(source_path).save(destination_image_path)
            shutil.move(source_txt_path, destination_txt_path)
            os.remove(source_path)
            messagebox.showinfo("Success", f"Image moved to {destination_path}")
            # Refresh listboxes after move
            self.refresh_listboxes()
        except Exception as e:
            messagebox.showinfo("Error", f"Error moving image: {e}")

    def get_txt_folder(self, listbox):
        if listbox == self.train_listbox:
            return self.train_folder.replace("Image", "Label")
        elif listbox == self.test_listbox:
            return self.test_folder.replace("Image", "Label")
        elif listbox == self.valid_listbox:
            return self.valid_folder.replace("Image", "Label")

    def get_selected_listbox(self):
        if self.train_listbox.curselection():
            return self.train_listbox
        elif self.test_listbox.curselection():
            return self.test_listbox
        elif self.valid_listbox.curselection():
            return self.valid_listbox

    def get_current_folder(self, listbox):
        if listbox == self.train_listbox:
            return self.train_folder
        elif listbox == self.test_listbox:
            return self.test_folder
        elif listbox == self.valid_listbox:
            return self.valid_folder

def classify_main(image_directory):
    root = Tk()
    
    valid_folder = image_directory.replace("Train", "Valid")
    
    test_folder = image_directory.replace("Train", "Test")

    print(image_directory)
    print(test_folder)
    print(valid_folder)

    data = {
        "train_folder": os.path.join(image_directory),
        "valid_folder": os.path.join(valid_folder),
        "test_folder": os.path.join(test_folder)
    }

    with open("config.json", "w") as f:
        json.dump(data, f)

    with open("config.json", "r") as f:
        config = json.load(f)

    app = ImageClassifierApp(root, config)
    app.load_image_info()
    root.mainloop()"""

    
