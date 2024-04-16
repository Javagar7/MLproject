"""import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk

from image_classifier import *
from image_downloader_gui import *
from annotate_image import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main


class MyApp:
    def __init__(self, root,imgdir):
        self.root = root
        self.root.title("Image Annotation Tool")
        self.root.geometry("1000x600")
        # Left Sidebar with six buttons
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.classes = ['helmet', 'bat', 'glove', 'shoe', 'ball', 'stumps', 'pads']
        
        '''buttons = ["Home","Search", "Classify", "Train", "Export", "Detect"]
        for button_text in buttons:
            tk.Button(self.left_frame, text=button_text, width=15).pack(side=tk.TOP, pady=5, fill=tk.X)'''
            
        self.button_functions = {
            "Home": self.open_home_window,
            "Search": self.search,
            "Classify": self.classify,
            "Train": self.open_train_window,
            "Export": self.open_export_window,
            "Detect": self.open_detect_window
        }

        self.create_buttons()

        # Right Frame with buttons from 1 to n
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        self.text_file_path = imgdir.replace("Image","Label")
        image_extensions = [".jpg",".jpeg",".png"]
        
        for ext in image_extensions:
            self.text_file_path = self.text_file_path.replace(ext,".txt")
        print(self.text_file_path)
        # Example annotations with center points in relative coordinates (0 to 1)
        self.annotations = self.read_annotation(self.text_file_path)
        # Create buttons dynamically based on the number of annotations
        self.right_buttons = []
        self.image_path = imgdir         
        self.img = Image.open(self.image_path)
        self.img=self.img.resize((837,540))
        self.iwidth, self.iheight = self.img.size
        print(self.iwidth)
        print(self.iheight)
        self.i=0
        label_text = "Annotations"
        label = tk.Label(self.right_frame, text=label_text)
        label.pack(side=tk.TOP, pady=5) 
        for self.i, annotation in enumerate(self.annotations, start=0):
            cx, cy, width, height = annotation['cx'], annotation['cy'], annotation['width'], annotation['height']
            button_text = f"(cx: {cx * self.iwidth}, cy: {cy * self.iheight}, w: {width * self.iwidth}, h: {height * self.iheight})"
            button = tk.Button(self.right_frame, text=button_text, width=50, command=lambda n=self.i : self.on_button_click(n))
            button.pack(side=tk.TOP, pady=5, fill=tk.X)
            self.right_buttons.append(button)
        self.i+=1
        if len(self.right_buttons) == 0:
            
            self.i=0  

        # Top Frame with image region
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, pady=10, fill=tk.BOTH, expand=True)
        
        self.cxt = None
        self.cyt = None
        self.width = None
        self.height = None

        # Bottom Frame with +/- buttons for values
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        spinbox_labels = ["cx :", "cy :", "w :", "h :"]
        spinboxes = []
        for label in spinbox_labels:
            tk.Label(self.bottom_frame, text=label, width=0).pack(side=tk.LEFT, padx=10)
            spinbox = tk.Spinbox(self.bottom_frame, from_=0, to=1000, width=5)
            spinbox.pack(side=tk.LEFT, padx=10)
            spinboxes.append(spinbox)

        # Assign the actual spinbox widgets
        self.cx_spinbox = spinboxes[0]
        self.cy_spinbox = spinboxes[1]
        self.w_spinbox = spinboxes[2]
        self.h_spinbox = spinboxes[3]
        for spinbox in spinboxes:
            spinbox.bind("<KeyRelease-Up>", self.update_annotation_values)
            spinbox.bind("<KeyRelease-Down>", self.update_annotation_values)
            
        tk.Label(self.bottom_frame, text="Class:").pack(side=tk.LEFT, padx=(20, 0))
        self.class_choice = StringVar()
        
        self.classes_dropdown = ttk.Combobox(self.bottom_frame, textvariable=self.class_choice, values=self.classes)
        self.classes_dropdown.set('helmet')
        self.classes_dropdown.pack(side=tk.LEFT, padx=5)
        self.classes_dropdown.bind("<<ComboboxSelected>>", self.update_annotation_values)

        # Bind functions to Spinbox and Combobox widgets
        self.cx_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.cy_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.w_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.h_spinbox.bind("<FocusOut>", self.update_annotation_values)

        self.selected_annotation_index = None  # Variable to store the selected annotation index
        self.canvas = tk.Canvas(self.top_frame, width=self.iwidth, height=self.iheight)  # Resize canvas
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.load_and_display_image()

        # Allow frames to resize with the window
        self.root.update()
        self.left_frame.pack_propagate(0)
        self.right_frame.pack_propagate(0)
        self.top_frame.pack_propagate(0)
        self.bottom_frame.pack_propagate(0)
        update_button = tk.Button(self.bottom_frame, text="Update", command=self.update_annotation_values)
        update_button.pack(side=tk.RIGHT, padx=10)
        delete_button = tk.Button(self.bottom_frame, text="Delete Annotation", command=self.delete_annotation)
        delete_button.pack(side=tk.RIGHT, padx=10)
        
    def create_buttons(self):
        for button_text, button_function in self.button_functions.items():
            button = tk.Button(self.left_frame, text=button_text, width=15, command=button_function)
            button.pack(side=tk.TOP, pady=5, fill=tk.X)

    def open_home_window(self):
        self.root.destroy()
        vAnnotate_main()

    def search(self):
        train_folder_path = os.path.dirname(os.path.dirname(self.image_path))
        self.root.destroy()
        image_gui_main(train_folder_path)

    def classify(self):
        train_folder_path =os.path.dirname(self.image_path)
        self.root.destroy()
        classify_main(train_folder_path)

    def open_train_window(self):
        self.root.destroy()
        train_main()

    def open_export_window(self):
        self.root.destroy()
        export_main()

    def open_detect_window(self):
        self.root.destroy()
        detect_main()
    
    def delete_annotation(self):
        if self.selected_annotation_index is not None:
            # Update the button text to "Annotation deleted"
            self.right_buttons[self.selected_annotation_index].config(text="Annotation deleted", state="disabled")
            self.annotations[self.selected_annotation_index]['color'] = 'invisible'
            # Rewrite the annotations to the file without the deleted annotation
            with open(self.text_file_path, "r") as file:            
                lines = file.readlines()

            # Update the line corresponding to the selected annotation index
            del lines[self.selected_annotation_index]

            # Write the updated lines back to the annotations file
            with open(self.text_file_path, "w") as file:
                file.writelines(lines)

            # Reload the image to reflect the changes
            
            self.load_and_display_image()

    def on_click(self, event):
        self.cxt = event.x
        self.cyt = event.y
        
    def on_drag(self, event):
        if self.cxt is not None and self.cyt is not None:
            self.width = event.x - self.cxt
            self.height = event.y - self.cyt
            self.canvas.delete("rectangle")
            # Ensure the rectangle stays within canvas bounds
            x0 = max(0, min(self.cxt, event.x))
            y0 = max(0, min(self.cyt, event.y))
            x1 = min(self.iwidth, max(self.cxt, event.x))
            y1 = min(self.iheight, max(self.cyt, event.y))
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", tags="rectangle")
        
    def on_release(self, event):
        if self.cxt is not None and self.cyt is not None:
            self.width = event.x - self.cxt
            self.height = event.y - self.cyt
            self.canvas.delete("rectangle")
            # Ensure the rectangle stays within canvas bounds
            x0 = max(0, min(self.cxt, event.x))
            y0 = max(0, min(self.cyt, event.y))
            x1 = min(self.iwidth, max(self.cxt, event.x))
            y1 = min(self.iheight, max(self.cyt, event.y))
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", tags="rectangle")
            # Calculate annotation values based on canvas coordinates
            cx = (x0 + x1) / (2 * self.iwidth)
            cy = (y0 + y1) / (2 * self.iheight)
            width = abs(x1 - x0) / self.iwidth
            height = abs(y1 - y0) / self.iheight
            if (height*self.iheight>10 and width*self.iwidth>10):
                annotation_text = f"cx: {cx*self.iwidth}, cy: {cy*self.iheight}, width: {width*self.iwidth}, height: {height*self.iheight}"
                print(annotation_text)
                # Add annotation button
                button_text = f"Annotation {len(self.right_buttons) + 1}: {annotation_text}"
                annotation_class = self.class_choice.get()
                annotation = {
                            'cx': cx,
                            'cy': cy,
                            'height': height,
                            'width': width,
                            'class': annotation_class,
                            'color': 'red'
                        }
                print(annotation)
                self.annotations.append(annotation)
                button = tk.Button(self.right_frame, text=button_text, width=50,command=lambda n=self.i : self.on_button_click(n))
                self.i+=1
                button.pack(side=tk.TOP, pady=5, fill=tk.X)
                self.right_buttons.append(button)
                clas = self.classes.index(annotation_class)
                with open(self.text_file_path, "a") as file:
                    file.write(f"{clas} {cx} {cy} {width} {height} \n")
                self.cxt = None
                self.cyt = None
                self.width = None
                self.height = None

    def update_annotation_values(self, event=None):
    # Update the selected annotation values based on the Spinbox and Combobox values
        if self.selected_annotation_index is not None:
            cx = float(self.cx_spinbox.get()) / self.iwidth
            cy = float(self.cy_spinbox.get()) / self.iheight
            width = float(self.w_spinbox.get()) / self.iwidth
            height = float(self.h_spinbox.get()) / self.iheight
            annotation_class = self.class_choice.get()

            # Update the annotation dictionary
            self.annotations[self.selected_annotation_index]['cx'] = cx
            self.annotations[self.selected_annotation_index]['cy'] = cy
            self.annotations[self.selected_annotation_index]['width'] = width
            self.annotations[self.selected_annotation_index]['height'] = height
            self.annotations[self.selected_annotation_index]['class'] = annotation_class

            # Write the updated lines back to the annotations file
            with open(self.text_file_path, "w") as file:
                for ann in self.annotations:
                    clas=self.classes.index(ann["class"])
                    if(ann["color"]=="invisible"):
                        continue
                    file.write(f"{clas} {ann['cx']} {ann['cy']} {ann['width']} {ann['height']} \n")


            # Redraw the image with updated annotations
            self.load_and_display_image()


    def load_and_display_image(self):
        self.canvas.delete("all")  # Clear existing items on the canvas
        
        img = Image.open(self.image_path)
        img = img.resize((837, 540))  # Adjust size as needed

        # Draw all annotations on the image
        img_with_annotations = self.draw_annotations(img, self.annotations)

        # Convert image to PhotoImage
        tk_img = ImageTk.PhotoImage(img_with_annotations)

        # Create a new Canvas widget for each image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        self.canvas.image = tk_img  # Save reference to prevent image from being garbage collected
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        # Highlight the selected annotation with a green border
        if self.selected_annotation_index is not None:
            self.highlight_selected_annotation()

        # Highlight the selected button with green
        self.highlight_selected_button()

    def read_annotation(self, file_path):
        annotations = []
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                pass
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split()
                if len(data) == 5:  # Assuming each line has cx, cy, height, width, and class
                    clas, cx, cy, width, height = map(float, data[:])
                    c = int(clas)
                    annotation = {
                        'cx': cx,
                        'cy': cy,
                        'height': height,
                        'width': width,
                        'class': self.classes[c],
                        'color': 'red'
                    }
                    annotations.append(annotation)
        return annotations

    def draw_annotations(self, image, annotations):
        # Get the size of the image
        img_width, img_height = image.size

        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Iterate through annotations and draw rectangles on the image
        for i, annotation in enumerate(annotations):
            if annotation['color'] == 'invisible':
                continue
            # Calculate rectangle coordinates based on the center point
            x_center, y_center = annotation['cx'] * img_width, annotation['cy'] * img_height
            width, height = annotation['width'] * img_width, annotation['height'] * img_height
            x, y = x_center - width / 2, y_center - height / 2

            # Draw the rectangle on the image
            border_color = 'green' if i == self.selected_annotation_index else annotation['color']
            draw.rectangle([x, y, x + width, y + height], outline=border_color, width=2)

        return image

    def on_button_click(self, button_index):
        # Update the selected annotation index
        self.selected_annotation_index = button_index

        # Fetch the annotation corresponding to the clicked button
        if self.selected_annotation_index is not None:
            annotation = self.annotations[self.selected_annotation_index]
            cx, cy, w, h = annotation['cx'], annotation['cy'], annotation['width'], annotation['height']
            annotation_class = annotation.get('class', '')  # Get the annotation class if it exists

            # Update the values in the spinboxes and class dropdown
            self.cx_spinbox.delete(0, tk.END)
            self.cx_spinbox.insert(0, str(cx * self.iwidth))
            self.cy_spinbox.delete(0, tk.END)
            self.cy_spinbox.insert(0, str(cy * self.iheight))
            self.w_spinbox.delete(0, tk.END)
            self.w_spinbox.insert(0, str(w * self.iwidth))
            self.h_spinbox.delete(0, tk.END)
            self.h_spinbox.insert(0, str(h * self.iheight))
            self.class_choice.set(annotation_class)

            # Reload and display the updated image with annotations
            self.load_and_display_image()

    def highlight_selected_annotation(self):
        # Highlight the selected annotation with a green border
        self.canvas.delete("highlight")  # Clear existing highlight items
        img = Image.open(self.image_path)
        img = img.resize((837, 540))  # Adjust size as needed
        img_with_highlight = self.draw_annotations(img, self.annotations)
        tk_img = ImageTk.PhotoImage(img_with_highlight)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img, tags="highlight")
        self.canvas.image = tk_img  # Save reference to prevent image from being garbage collected

    def highlight_selected_button(self):
        # Highlight the selected button with green
        for i, button in enumerate(self.right_buttons):
            button_color = 'green' if i == self.selected_annotation_index else 'SystemButtonFace'
            button.configure(bg=button_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()"""
    
"""import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk

from image_classifier import *
from image_downloader_gui import *
from annotate_image import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main


class MyApp:
    def __init__(self, root,imgdir):
        self.root = root
        self.root.title("Image Annotation Tool")
        self.root.geometry("1000x600")
        # Left Sidebar with six buttons
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        print(imgdir)
        self.classdir=os.path.dirname(os.path.dirname(os.path.dirname(imgdir)))
        new_path = self.classdir + ".txt"
        self.classdir=new_path.replace("Dataset","Class")
        if not os.path.isfile(self.classdir):
            with open(self.classdir, 'w') as file:
                pass
        with open(self.classdir, "r") as file:
            file_contents = file.read()
            lines = file_contents.splitlines()
        print("class",self.classdir)
        print(lines)
        self.classes = lines        
        self.classlen=len(lines)
        self.button_functions = {
            "Home": self.open_home_window,
            "Search": self.search,
            "Classify": self.classify,
            "Train": self.open_train_window,
            "Export": self.open_export_window,
            "Detect": self.open_detect_window
        }

        self.create_buttons()

        # Right Frame with buttons from 1 to n
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        self.text_file_path = imgdir.replace("Image","Label")
        image_extensions = [".jpg",".jpeg",".png"]
        
        for ext in image_extensions:
            self.text_file_path = self.text_file_path.replace(ext,".txt")
        print(self.text_file_path)
        # Example annotations with center points in relative coordinates (0 to 1)
        self.annotations = self.read_annotation(self.text_file_path)
        # Create buttons dynamically based on the number of annotations
        self.right_buttons = []
        self.image_path = imgdir         
        self.img = Image.open(self.image_path)
        self.img=self.img.resize((837,540))
        self.iwidth, self.iheight = self.img.size
        print(self.iwidth)
        print(self.iheight)
        self.i=0
        label_text = "             Annotations                                                       "
        label = tk.Label(self.right_frame, text=label_text)
        label.pack(side=tk.TOP, pady=5) 
        for self.i, annotation in enumerate(self.annotations, start=0):
            cx, cy, width, height = annotation['cx'], annotation['cy'], annotation['width'], annotation['height']
            button_text = f"(cx: {cx * self.iwidth}, cy: {cy * self.iheight}, w: {width * self.iwidth}, h: {height * self.iheight})"
            button = tk.Button(self.right_frame, text=button_text, width=50, command=lambda n=self.i : self.on_button_click(n))
            button.pack(side=tk.TOP, pady=5, fill=tk.X)
            self.right_buttons.append(button)
        self.i+=1
        if len(self.right_buttons) == 0:
            
            self.i=0  

        # Top Frame with image region
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, pady=10, fill=tk.BOTH, expand=True)
        
        self.cxt = None
        self.cyt = None
        self.width = None
        self.height = None

        # Bottom Frame with +/- buttons for values
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        spinbox_labels = ["cx :", "cy :", "w :", "h :"]
        spinboxes = []
        for label in spinbox_labels:
            tk.Label(self.bottom_frame, text=label, width=0).pack(side=tk.LEFT, padx=10)
            spinbox = tk.Spinbox(self.bottom_frame, from_=0, to=1000, width=5)
            spinbox.pack(side=tk.LEFT, padx=10)
            spinboxes.append(spinbox)

        # Assign the actual spinbox widgets
        self.cx_spinbox = spinboxes[0]
        self.cy_spinbox = spinboxes[1]
        self.w_spinbox = spinboxes[2]
        self.h_spinbox = spinboxes[3]
        for spinbox in spinboxes:
            spinbox.bind("<KeyRelease-Up>", self.update_annotation_values)
            spinbox.bind("<KeyRelease-Down>", self.update_annotation_values)
            
        tk.Label(self.bottom_frame, text="Class:").pack(side=tk.LEFT, padx=(20, 0))
        self.class_choice = StringVar()
        
        self.classes_dropdown = ttk.Combobox(self.bottom_frame, textvariable=self.class_choice, values=self.classes)
        if (self.classlen == 0):
            self.classes_dropdown.set('')
        else:
            self.classes_dropdown.set(self.classes[0])
        self.classes_dropdown.pack(side=tk.LEFT, padx=5)
        self.classes_dropdown.bind("<<ComboboxSelected>>", self.update_annotation_values)

        # Bind functions to Spinbox and Combobox widgets
        self.cx_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.cy_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.w_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.h_spinbox.bind("<FocusOut>", self.update_annotation_values)

        self.selected_annotation_index = None  # Variable to store the selected annotation index
        self.canvas = tk.Canvas(self.top_frame, width=self.iwidth, height=self.iheight)  # Resize canvas
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.load_and_display_image()

        # Allow frames to resize with the window
        self.root.update()
        self.left_frame.pack_propagate(0)
        self.right_frame.pack_propagate(0)
        self.top_frame.pack_propagate(0)
        self.bottom_frame.pack_propagate(0)
        self.text_box = tk.Entry(self.bottom_frame)
        self.text_box.pack(side=tk.LEFT, padx=10)
        add_class_button = tk.Button(self.bottom_frame, text="add class", command=self.add_class)
        add_class_button.pack(side=tk.RIGHT, padx=10)
        update_button = tk.Button(self.bottom_frame, text="Update", command=self.update_annotation_values)
        update_button.pack(side=tk.RIGHT, padx=10)
        delete_button = tk.Button(self.bottom_frame, text="Delete Annotation", command=self.delete_annotation)
        delete_button.pack(side=tk.RIGHT, padx=10)
        
    def create_buttons(self):
        for button_text, button_function in self.button_functions.items():
            button = tk.Button(self.left_frame, text=button_text, width=15, command=button_function)
            button.pack(side=tk.TOP, pady=5, fill=tk.X)

    def add_class(self):
        text=self.text_box.get()
        with open(self.classdir, "r") as file:
                    file_con=file.read()
                    lines=file_con.splitlines()
        text_l=text.lower()
        for word in lines:
            if text_l in word.lower():
                return True
        text=text_l.capitalize()
        with open(self.classdir, "a") as file:
                    file.write(f"{text}\n")
        self.classes.append(text)
        self.classes_dropdown['values'] = self.classes
        self.classes_dropdown.set(text)
        self.classlen+=1

    def open_home_window(self):
        self.root.destroy()
        vAnnotate_main()

    def search(self):
        train_folder_path = os.path.dirname(os.path.dirname(self.image_path))
        self.root.destroy()
        image_gui_main(train_folder_path)

    def classify(self):
        train_folder_path =os.path.dirname(self.image_path)
        self.root.destroy()
        classify_main(train_folder_path)

    def open_train_window(self):
        self.root.destroy()
        train_main()

    def open_export_window(self):
        self.root.destroy()
        export_main()

    def open_detect_window(self):
        self.root.destroy()
        detect_main()
    
    def delete_annotation(self):
        if self.selected_annotation_index is not None:
            # Update the button text to "Annotation deleted"
            self.right_buttons[self.selected_annotation_index].config(text="Annotation deleted", state="disabled")
            self.annotations[self.selected_annotation_index]['color'] = 'invisible'
            # Rewrite the annotations to the file without the deleted annotation
            with open(self.text_file_path, "r") as file:            
                lines = file.readlines()

            # Update the line corresponding to the selected annotation index
            del lines[self.selected_annotation_index]

            # Write the updated lines back to the annotations file
            with open(self.text_file_path, "w") as file:
                file.writelines(lines)

            # Reload the image to reflect the changes
            
            self.load_and_display_image()

    def on_click(self, event):
        self.cxt = event.x
        self.cyt = event.y
        
    def on_drag(self, event):
        if self.cxt is not None and self.cyt is not None:
            self.width = event.x - self.cxt
            self.height = event.y - self.cyt
            self.canvas.delete("rectangle")
            # Ensure the rectangle stays within canvas bounds
            x0 = max(0, min(self.cxt, event.x))
            y0 = max(0, min(self.cyt, event.y))
            x1 = min(self.iwidth, max(self.cxt, event.x))
            y1 = min(self.iheight, max(self.cyt, event.y))
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", tags="rectangle")
        
    def on_release(self, event):
        if self.cxt is not None and self.cyt is not None:
            self.width = event.x - self.cxt
            self.height = event.y - self.cyt
            self.canvas.delete("rectangle")
            # Ensure the rectangle stays within canvas bounds
            x0 = max(0, min(self.cxt, event.x))
            y0 = max(0, min(self.cyt, event.y))
            x1 = min(self.iwidth, max(self.cxt, event.x))
            y1 = min(self.iheight, max(self.cyt, event.y))
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", tags="rectangle")
            # Calculate annotation values based on canvas coordinates
            cx = (x0 + x1) / (2 * self.iwidth)
            cy = (y0 + y1) / (2 * self.iheight)
            width = abs(x1 - x0) / self.iwidth
            height = abs(y1 - y0) / self.iheight
            if self.classlen==0:
                return True
            if (height*self.iheight>10 and width*self.iwidth>10):
                annotation_text = f"cx: {cx*self.iwidth}, cy: {cy*self.iheight}, width: {width*self.iwidth}, height: {height*self.iheight}"
                print(annotation_text)
                # Add annotation button
                button_text = f"{annotation_text}"
                annotation_class = self.class_choice.get()
                annotation = {
                            'cx': cx,
                            'cy': cy,
                            'height': height,
                            'width': width,
                            'class': annotation_class,
                            'color': 'red'
                        }
                print(annotation)
                self.annotations.append(annotation)
                button = tk.Button(self.right_frame, text=button_text, width=50,command=lambda n=self.i : self.on_button_click(n))
                self.i+=1
                button.pack(side=tk.TOP, pady=5, fill=tk.X)
                self.right_buttons.append(button)
                clas = self.classes.index(annotation_class)
                with open(self.text_file_path, "a") as file:
                    file.write(f"{clas} {cx} {cy} {width} {height} \n")
                self.cxt = None
                self.cyt = None
                self.width = None
                self.height = None

    def update_annotation_values(self, event=None):
    # Update the selected annotation values based on the Spinbox and Combobox values
        if self.selected_annotation_index is not None:
            cx = float(self.cx_spinbox.get()) / self.iwidth
            cy = float(self.cy_spinbox.get()) / self.iheight
            width = float(self.w_spinbox.get()) / self.iwidth
            height = float(self.h_spinbox.get()) / self.iheight
            annotation_class = self.class_choice.get()

            # Update the annotation dictionary
            self.annotations[self.selected_annotation_index]['cx'] = cx
            self.annotations[self.selected_annotation_index]['cy'] = cy
            self.annotations[self.selected_annotation_index]['width'] = width
            self.annotations[self.selected_annotation_index]['height'] = height
            self.annotations[self.selected_annotation_index]['class'] = annotation_class

            # Write the updated lines back to the annotations file
            with open(self.text_file_path, "w") as file:
                for ann in self.annotations:
                    clas=self.classes.index(ann["class"])
                    if(ann["color"]=="invisible"):
                        continue
                    file.write(f"{clas} {ann['cx']} {ann['cy']} {ann['width']} {ann['height']} \n")


            # Redraw the image with updated annotations
            self.load_and_display_image()


    def load_and_display_image(self):
        self.canvas.delete("all")  # Clear existing items on the canvas
        
        img = Image.open(self.image_path)
        img = img.resize((837, 540))  # Adjust size as needed

        # Draw all annotations on the image
        img_with_annotations = self.draw_annotations(img, self.annotations)

        # Convert image to PhotoImage
        tk_img = ImageTk.PhotoImage(img_with_annotations)

        # Create a new Canvas widget for each image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        self.canvas.image = tk_img  # Save reference to prevent image from being garbage collected
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        # Highlight the selected annotation with a green border
        if self.selected_annotation_index is not None:
            self.highlight_selected_annotation()

        # Highlight the selected button with green
        self.highlight_selected_button()

    def read_annotation(self, file_path):
        annotations = []
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                pass
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split()
                if len(data) == 5:  # Assuming each line has cx, cy, height, width, and class
                    clas, cx, cy, width, height = map(float, data[:])
                    c = int(clas)
                    annotation = {
                        'cx': cx,
                        'cy': cy,
                        'height': height,
                        'width': width,
                        'class': self.classes[c],
                        'color': 'red'
                    }
                    annotations.append(annotation)
        return annotations

    def draw_annotations(self, image, annotations):
        # Get the size of the image
        img_width, img_height = image.size

        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Iterate through annotations and draw rectangles on the image
        for i, annotation in enumerate(annotations):
            if annotation['color'] == 'invisible':
                continue
            # Calculate rectangle coordinates based on the center point
            x_center, y_center = annotation['cx'] * img_width, annotation['cy'] * img_height
            width, height = annotation['width'] * img_width, annotation['height'] * img_height
            x, y = x_center - width / 2, y_center - height / 2

            # Draw the rectangle on the image
            border_color = 'green' if i == self.selected_annotation_index else annotation['color']
            draw.rectangle([x, y, x + width, y + height], outline=border_color, width=2)

        return image

    def on_button_click(self, button_index):
        # Update the selected annotation index
        self.selected_annotation_index = button_index

        # Fetch the annotation corresponding to the clicked button
        if self.selected_annotation_index is not None:
            annotation = self.annotations[self.selected_annotation_index]
            cx, cy, w, h = annotation['cx'], annotation['cy'], annotation['width'], annotation['height']
            annotation_class = annotation.get('class', '')  # Get the annotation class if it exists

            # Update the values in the spinboxes and class dropdown
            self.cx_spinbox.delete(0, tk.END)
            self.cx_spinbox.insert(0, str(cx * self.iwidth))
            self.cy_spinbox.delete(0, tk.END)
            self.cy_spinbox.insert(0, str(cy * self.iheight))
            self.w_spinbox.delete(0, tk.END)
            self.w_spinbox.insert(0, str(w * self.iwidth))
            self.h_spinbox.delete(0, tk.END)
            self.h_spinbox.insert(0, str(h * self.iheight))
            self.class_choice.set(annotation_class)

            # Reload and display the updated image with annotations
            self.load_and_display_image()

    def highlight_selected_annotation(self):
        # Highlight the selected annotation with a green border
        self.canvas.delete("highlight")  # Clear existing highlight items
        img = Image.open(self.image_path)
        img = img.resize((837, 540))  # Adjust size as needed
        img_with_highlight = self.draw_annotations(img, self.annotations)
        tk_img = ImageTk.PhotoImage(img_with_highlight)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img, tags="highlight")
        self.canvas.image = tk_img  # Save reference to prevent image from being garbage collected

    def highlight_selected_button(self):
        # Highlight the selected button with green
        for i, button in enumerate(self.right_buttons):
            button_color = 'green' if i == self.selected_annotation_index else 'SystemButtonFace'
            button.configure(bg=button_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()"""

import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk

from image_classifier import *
from image_downloader_gui import *
from annotate_image import *

from export_dataset import export_main
from train_dataset import train_main
from detect_object import detect_main


class MyApp:
    def __init__(self, root,imgdir):
        self.root = root
        self.root.title("Image Annotation Tool")
        self.root.geometry("1000x600")
        # Left Sidebar with six buttons
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        print(imgdir)
        self.classdir=os.path.dirname(os.path.dirname(os.path.dirname(imgdir)))
        new_path = os.path.join(self.classdir, "class")
        self.classdir = new_path+ ".txt"
        if not os.path.isfile(self.classdir):
            with open(self.classdir, 'w') as file:
                pass
        with open(self.classdir, "r") as file:
            file_contents = file.read()
            lines = file_contents.splitlines()
        print("class",self.classdir)
        print(lines)
        self.classes = lines        
        self.classlen=len(lines)
        self.button_functions = {
            "Home": self.open_home_window,
            "Search": self.search,
            "Classify": self.classify,
            "Train": self.open_train_window,
            "Export": self.open_export_window,
            "Detect": self.open_detect_window
        }

        self.create_buttons()

        # Right Frame with buttons from 1 to n
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        self.text_file_path = imgdir.replace("Image","Label")
        image_extensions = [".jpg",".jpeg",".png"]
        
        for ext in image_extensions:
            self.text_file_path = self.text_file_path.replace(ext,".txt")
        print(self.text_file_path)
        # Example annotations with center points in relative coordinates (0 to 1)
        self.annotations = self.read_annotation(self.text_file_path)
        # Create buttons dynamically based on the number of annotations
        self.right_buttons = []
        self.image_path = imgdir         
        self.img = Image.open(self.image_path)
        self.img=self.img.resize((837,540))
        self.iwidth, self.iheight = self.img.size
        print(self.iwidth)
        print(self.iheight)
        self.i=0
        label_text = "             Annotations                                                       "
        label = tk.Label(self.right_frame, text=label_text)
        label.pack(side=tk.TOP, pady=5) 
        for self.i, annotation in enumerate(self.annotations, start=0):
            cx, cy, width, height = annotation['cx'], annotation['cy'], annotation['width'], annotation['height']
            button_text = f"(cx: {cx * self.iwidth}, cy: {cy * self.iheight}, w: {width * self.iwidth}, h: {height * self.iheight})"
            button = tk.Button(self.right_frame, text=button_text, width=50, command=lambda n=self.i : self.on_button_click(n))
            button.pack(side=tk.TOP, pady=5, fill=tk.X)
            self.right_buttons.append(button)
        self.i+=1
        if len(self.right_buttons) == 0:
            
            self.i=0  

        # Top Frame with image region
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, pady=10, fill=tk.BOTH, expand=True)
        
        self.cxt = None
        self.cyt = None
        self.width = None
        self.height = None

        # Bottom Frame with +/- buttons for values
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        spinbox_labels = ["cx :", "cy :", "w :", "h :"]
        spinboxes = []
        for label in spinbox_labels:
            tk.Label(self.bottom_frame, text=label, width=0).pack(side=tk.LEFT, padx=10)
            spinbox = tk.Spinbox(self.bottom_frame, from_=0, to=1000, width=5)
            spinbox.pack(side=tk.LEFT, padx=10)
            spinboxes.append(spinbox)

        # Assign the actual spinbox widgets
        self.cx_spinbox = spinboxes[0]
        self.cy_spinbox = spinboxes[1]
        self.w_spinbox = spinboxes[2]
        self.h_spinbox = spinboxes[3]
        for spinbox in spinboxes:
            spinbox.bind("<KeyRelease-Up>", self.update_annotation_values)
            spinbox.bind("<KeyRelease-Down>", self.update_annotation_values)
            
        tk.Label(self.bottom_frame, text="Class:").pack(side=tk.LEFT, padx=(20, 0))
        self.class_choice = StringVar()
        
        self.classes_dropdown = ttk.Combobox(self.bottom_frame, textvariable=self.class_choice, values=self.classes)
        if (self.classlen == 0):
            self.classes_dropdown.set('')
        else:
            self.classes_dropdown.set(self.classes[0])
        self.classes_dropdown.pack(side=tk.LEFT, padx=5)
        self.classes_dropdown.bind("<<ComboboxSelected>>", self.update_annotation_values)

        # Bind functions to Spinbox and Combobox widgets
        self.cx_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.cy_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.w_spinbox.bind("<FocusOut>", self.update_annotation_values)
        self.h_spinbox.bind("<FocusOut>", self.update_annotation_values)

        self.selected_annotation_index = None  # Variable to store the selected annotation index
        self.canvas = tk.Canvas(self.top_frame, width=self.iwidth, height=self.iheight)  # Resize canvas
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.load_and_display_image()

        # Allow frames to resize with the window
        self.root.update()
        self.left_frame.pack_propagate(0)
        self.right_frame.pack_propagate(0)
        self.top_frame.pack_propagate(0)
        self.bottom_frame.pack_propagate(0)
        self.text_box = tk.Entry(self.bottom_frame)
        self.text_box.pack(side=tk.LEFT, padx=10)
        add_class_button = tk.Button(self.bottom_frame, text="add class", command=self.add_class)
        add_class_button.pack(side=tk.RIGHT, padx=10)
        update_button = tk.Button(self.bottom_frame, text="Update", command=self.update_annotation_values)
        update_button.pack(side=tk.RIGHT, padx=10)
        delete_button = tk.Button(self.bottom_frame, text="Delete Annotation", command=self.delete_annotation)
        delete_button.pack(side=tk.RIGHT, padx=10)
        
    def create_buttons(self):
        for button_text, button_function in self.button_functions.items():
            button = tk.Button(self.left_frame, text=button_text, width=15, command=button_function)
            button.pack(side=tk.TOP, pady=5, fill=tk.X)

    def add_class(self):
        text=self.text_box.get()
        with open(self.classdir, "r") as file:
                    file_con=file.read()
                    lines=file_con.splitlines()
        text_l=text.lower()
        for word in lines:
            if text_l in word.lower():
                return True
        text=text_l.capitalize()
        with open(self.classdir, "a") as file:
                    file.write(f"{text}\n")
        self.classes.append(text)
        self.classes_dropdown['values'] = self.classes
        self.classes_dropdown.set(text)
        self.classlen+=1

    def open_home_window(self):
        self.root.destroy()
        vAnnotate_main()

    def search(self):
        train_folder_path = os.path.dirname(os.path.dirname(self.image_path))
        self.root.destroy()
        image_gui_main(train_folder_path)

    def classify(self):
        train_folder_path =os.path.dirname(self.image_path)
        self.root.destroy()
        classify_main(train_folder_path)

    def open_train_window(self):
        self.root.destroy()
        train_main()

    def open_export_window(self):
        self.root.destroy()
        export_main()

    def open_detect_window(self):
        self.root.destroy()
        detect_main()
    
    def delete_annotation(self):
        if self.selected_annotation_index is not None:
            # Update the button text to "Annotation deleted"
            self.right_buttons[self.selected_annotation_index].config(text="Annotation deleted", state="disabled")
            self.annotations[self.selected_annotation_index]['color'] = 'invisible'
            # Rewrite the annotations to the file without the deleted annotation
            with open(self.text_file_path, "r") as file:            
                lines = file.readlines()

            # Update the line corresponding to the selected annotation index
            del lines[self.selected_annotation_index]

            # Write the updated lines back to the annotations file
            with open(self.text_file_path, "w") as file:
                file.writelines(lines)

            # Reload the image to reflect the changes
            
            self.load_and_display_image()

    def on_click(self, event):
        self.cxt = event.x
        self.cyt = event.y
        
    def on_drag(self, event):
        if self.cxt is not None and self.cyt is not None:
            self.width = event.x - self.cxt
            self.height = event.y - self.cyt
            self.canvas.delete("rectangle")
            # Ensure the rectangle stays within canvas bounds
            x0 = max(0, min(self.cxt, event.x))
            y0 = max(0, min(self.cyt, event.y))
            x1 = min(self.iwidth, max(self.cxt, event.x))
            y1 = min(self.iheight, max(self.cyt, event.y))
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", tags="rectangle")
        
    def on_release(self, event):
        if self.cxt is not None and self.cyt is not None:
            self.width = event.x - self.cxt
            self.height = event.y - self.cyt
            self.canvas.delete("rectangle")
            # Ensure the rectangle stays within canvas bounds
            x0 = max(0, min(self.cxt, event.x))
            y0 = max(0, min(self.cyt, event.y))
            x1 = min(self.iwidth, max(self.cxt, event.x))
            y1 = min(self.iheight, max(self.cyt, event.y))
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", tags="rectangle")
            # Calculate annotation values based on canvas coordinates
            cx = (x0 + x1) / (2 * self.iwidth)
            cy = (y0 + y1) / (2 * self.iheight)
            width = abs(x1 - x0) / self.iwidth
            height = abs(y1 - y0) / self.iheight
            if self.classlen==0:
                return True
            if (height*self.iheight>10 and width*self.iwidth>10):
                annotation_text = f"cx: {cx*self.iwidth}, cy: {cy*self.iheight}, width: {width*self.iwidth}, height: {height*self.iheight}"
                print(annotation_text)
                # Add annotation button
                button_text = f"{annotation_text}"
                annotation_class = self.class_choice.get()
                annotation = {
                            'cx': cx,
                            'cy': cy,
                            'height': height,
                            'width': width,
                            'class': annotation_class,
                            'color': 'red'
                        }
                print(annotation)
                self.annotations.append(annotation)
                button = tk.Button(self.right_frame, text=button_text, width=50,command=lambda n=self.i : self.on_button_click(n))
                self.i+=1
                button.pack(side=tk.TOP, pady=5, fill=tk.X)
                self.right_buttons.append(button)
                clas = self.classes.index(annotation_class)
                with open(self.text_file_path, "a") as file:
                    file.write(f"{clas} {cx} {cy} {width} {height} \n")
                self.cxt = None
                self.cyt = None
                self.width = None
                self.height = None

    def update_annotation_values(self, event=None):
    # Update the selected annotation values based on the Spinbox and Combobox values
        if self.selected_annotation_index is not None:
            cx = float(self.cx_spinbox.get()) / self.iwidth
            cy = float(self.cy_spinbox.get()) / self.iheight
            width = float(self.w_spinbox.get()) / self.iwidth
            height = float(self.h_spinbox.get()) / self.iheight
            annotation_class = self.class_choice.get()

            # Update the annotation dictionary
            self.annotations[self.selected_annotation_index]['cx'] = cx
            self.annotations[self.selected_annotation_index]['cy'] = cy
            self.annotations[self.selected_annotation_index]['width'] = width
            self.annotations[self.selected_annotation_index]['height'] = height
            self.annotations[self.selected_annotation_index]['class'] = annotation_class

            # Write the updated lines back to the annotations file
            with open(self.text_file_path, "w") as file:
                for ann in self.annotations:
                    clas=self.classes.index(ann["class"])
                    if(ann["color"]=="invisible"):
                        continue
                    file.write(f"{clas} {ann['cx']} {ann['cy']} {ann['width']} {ann['height']} \n")


            # Redraw the image with updated annotations
            self.load_and_display_image()


    def load_and_display_image(self):
        self.canvas.delete("all")  # Clear existing items on the canvas
        
        img = Image.open(self.image_path)
        img = img.resize((837, 540))  # Adjust size as needed

        # Draw all annotations on the image
        img_with_annotations = self.draw_annotations(img, self.annotations)

        # Convert image to PhotoImage
        tk_img = ImageTk.PhotoImage(img_with_annotations)

        # Create a new Canvas widget for each image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        self.canvas.image = tk_img  # Save reference to prevent image from being garbage collected
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        # Highlight the selected annotation with a green border
        if self.selected_annotation_index is not None:
            self.highlight_selected_annotation()

        # Highlight the selected button with green
        self.highlight_selected_button()

    def read_annotation(self, file_path):
        annotations = []
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                pass
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split()
                if len(data) == 5:  # Assuming each line has cx, cy, height, width, and class
                    clas, cx, cy, width, height = map(float, data[:])
                    c = int(clas)
                    annotation = {
                        'cx': cx,
                        'cy': cy,
                        'height': height,
                        'width': width,
                        'class': self.classes[c],
                        'color': 'red'
                    }
                    annotations.append(annotation)
        return annotations

    def draw_annotations(self, image, annotations):
        # Get the size of the image
        img_width, img_height = image.size

        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Iterate through annotations and draw rectangles on the image
        for i, annotation in enumerate(annotations):
            if annotation['color'] == 'invisible':
                continue
            # Calculate rectangle coordinates based on the center point
            x_center, y_center = annotation['cx'] * img_width, annotation['cy'] * img_height
            width, height = annotation['width'] * img_width, annotation['height'] * img_height
            x, y = x_center - width / 2, y_center - height / 2

            # Draw the rectangle on the image
            border_color = 'green' if i == self.selected_annotation_index else annotation['color']
            draw.rectangle([x, y, x + width, y + height], outline=border_color, width=2)

        return image

    def on_button_click(self, button_index):
        # Update the selected annotation index
        self.selected_annotation_index = button_index

        # Fetch the annotation corresponding to the clicked button
        if self.selected_annotation_index is not None:
            annotation = self.annotations[self.selected_annotation_index]
            cx, cy, w, h = annotation['cx'], annotation['cy'], annotation['width'], annotation['height']
            annotation_class = annotation.get('class', '')  # Get the annotation class if it exists

            # Update the values in the spinboxes and class dropdown
            self.cx_spinbox.delete(0, tk.END)
            self.cx_spinbox.insert(0, str(cx * self.iwidth))
            self.cy_spinbox.delete(0, tk.END)
            self.cy_spinbox.insert(0, str(cy * self.iheight))
            self.w_spinbox.delete(0, tk.END)
            self.w_spinbox.insert(0, str(w * self.iwidth))
            self.h_spinbox.delete(0, tk.END)
            self.h_spinbox.insert(0, str(h * self.iheight))
            self.class_choice.set(annotation_class)

            # Reload and display the updated image with annotations
            self.load_and_display_image()

    def highlight_selected_annotation(self):
        # Highlight the selected annotation with a green border
        self.canvas.delete("highlight")  # Clear existing highlight items
        img = Image.open(self.image_path)
        img = img.resize((837, 540))  # Adjust size as needed
        img_with_highlight = self.draw_annotations(img, self.annotations)
        tk_img = ImageTk.PhotoImage(img_with_highlight)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img, tags="highlight")
        self.canvas.image = tk_img  # Save reference to prevent image from being garbage collected

    def highlight_selected_button(self):
        # Highlight the selected button with green
        for i, button in enumerate(self.right_buttons):
            button_color = 'green' if i == self.selected_annotation_index else 'SystemButtonFace'
            button.configure(bg=button_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()