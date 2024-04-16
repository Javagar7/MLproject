import os
import sys
import tkinter as tk
from tkinter import ttk
import subprocess
import platform

from list_images import *

def main():
    def callCreateFunction():
        dataset_name = e1.get()

        # Set the parent folder
        parent_folder = 'Parent'

        # Create 'class' and 'dataset' folders under the parent folder
        class_folder_path = os.path.join(parent_folder, 'Class')
        dataset_folder_path = os.path.join(parent_folder, 'Dataset')

        if os.path.exists(os.path.join(dataset_folder_path, dataset_name)):
            print("Folders already exist.")
            return
        else:
            os.makedirs(class_folder_path, exist_ok=True)
            os.makedirs(dataset_folder_path, exist_ok=True)
            print("Directory structure created successfully.")

        dataset_path = os.path.join(dataset_folder_path, dataset_name)

        # Create the dataset folder if it doesn't exist
        os.makedirs(dataset_path, exist_ok=True)

        # Create subfolders 'img' and 'label' under the dataset folder
        img_folder_path = os.path.join(dataset_path, 'Image')
        label_folder_path = os.path.join(dataset_path, 'Label')

        os.makedirs(img_folder_path, exist_ok=True)
        os.makedirs(label_folder_path, exist_ok=True)

        # Create subdirectories (train, val, test) under 'img' and 'label'
        for sub_directory in ['Train', 'Valid', 'Test']:
            img_sub_folder_path = os.path.join(img_folder_path, sub_directory)
            label_sub_folder_path = os.path.join(label_folder_path, sub_directory)

            os.makedirs(img_sub_folder_path, exist_ok=True)
            os.makedirs(label_sub_folder_path, exist_ok=True)

        print(f"Directory structure created successfully in: {dataset_path}")

    def display_dataset_directory(dataset_name):
        parent_folder = 'Parent'
        dataset_folder_path = os.path.join(parent_folder, 'Dataset')
        dataset_path = os.path.join(dataset_folder_path, dataset_name)
        print(f"Dataset directory path: {dataset_path}")
        root.destroy()
        call_main(dataset_path)

    def delete_dataset():
        dataset_name = delete_entry.get()
        parent_folder = 'Parent'
        dataset_folder_path = os.path.join(parent_folder, 'Dataset')
        dataset_path = os.path.join(dataset_folder_path, dataset_name)

        if os.path.exists(dataset_path):
            # Remove the dataset directory
            try:
                os.rmdir(dataset_path)
                print(f"Dataset '{dataset_name}' deleted successfully.")
            except OSError as e:
                print(f"Error: {dataset_path} : {e.strerror}")
        else:
            print(f"Dataset '{dataset_name}' does not exist.")

    def delete_dataset_current_tab():
        dataset_name = delete_entry_current_tab.get()
        parent_folder = 'Parent'
        dataset_folder_path = os.path.join(parent_folder, 'Dataset')
        dataset_path = os.path.join(dataset_folder_path, dataset_name)

        if os.path.exists(dataset_path):
            # Remove the dataset directory
            try:
                os.rmdir(dataset_path)
                print(f"Dataset '{dataset_name}' deleted successfully.")
                refresh_current_tab()  # Refresh current tab after deletion
            except OSError as e:
                print(f"Error: {dataset_path} : {e.strerror}")
        else:
            print(f"Dataset '{dataset_name}' does not exist.")

    def refresh():
        # Clear existing buttons
        for button in f1.grid_slaves():
            if button.cget("text") != "Search" and button.cget("text") != "Download" and button.cget("text") != "Remove":
                button.grid_forget()    

        # Recreate buttons with updated dataset names
        b = []
        for i, dataset_name in enumerate(os.listdir("./Parent/Dataset")):
            dataset_button = ttk.Button(f1, text=dataset_name, command=lambda name=dataset_name: display_dataset_directory(name))
            b.append(dataset_button)

        for i, button in enumerate(b):
            button.grid(row=int(i/4) + 1, column=int(i%4), sticky=tk.W, padx=15, pady=15)

    def refresh_current_tab():
        # Clear existing buttons
        for button in notebook.tabs(notebook.select()).grid_slaves():
            if button.cget("text") != "Search" and button.cget("text") != "Download" and button.cget("text") != "Remove":
                button.grid_forget()    

        # Recreate buttons with updated dataset names
        current_tab = notebook.tabs(notebook.select())['text']
        for i, dataset_name in enumerate(os.listdir("./Parent/Dataset")):
            dataset_button = ttk.Button(current_tab, text=dataset_name, command=lambda name=dataset_name: display_dataset_directory(name))
            dataset_button.grid(row=int(i/4) + 1, column=int(i%4), sticky=tk.W, padx=15, pady=15)

    def delete_dataset_frame2():
        dataset_name = delete_entry_frame2.get()
        parent_folder = 'Parent'
        dataset_folder_path = os.path.join(parent_folder, 'Dataset')
        dataset_path = os.path.join(dataset_folder_path, dataset_name)

        if os.path.exists(dataset_path):
            # Remove the dataset directory
            try:
                os.rmdir(dataset_path)
                print(f"Dataset '{dataset_name}' deleted successfully.")
                refresh_frame2()  # Refresh frame2 after deletion
            except OSError as e:
                print(f"Error: {dataset_path} : {e.strerror}")
        else:
            print(f"Dataset '{dataset_name}' does not exist.")

    def refresh_frame2():
        pass  # You can define the refresh function for frame2 if needed

    # create a root window
    root = tk.Tk()

    # set the title of the window
    root.title("vAnnotate")

    # create a notebook widget
    notebook = ttk.Notebook(root)

    # create a frame for the first tab
    f1 = ttk.Frame(notebook)

    # create a label widget for the dataset name
    l1 = ttk.Label(f1, text="DataSet Name:")

    # create an entry widget for the dataset name
    e1 = ttk.Entry(f1)

    # create a button widget for creating a new dataset
    b1 = ttk.Button(f1, text="Create DataSet", command=callCreateFunction)

    # create a button widget for refreshing
    refresh_button = ttk.Button(f1, text="Refresh", command=refresh)

    # create a label widget for deleting dataset
    delete_label = ttk.Label(f1, text="Delete DataSet:")

    # create an entry widget for deleting dataset
    delete_entry = ttk.Entry(f1)

    # create a button widget for deleting dataset
    delete_button = ttk.Button(f1, text="Delete DataSet", command=delete_dataset)

    # create a label widget for deleting dataset from current tab

    # create an entry widget for deleting dataset from current tab
    delete_entry_current_tab = ttk.Entry(f1)

    # create a button widget for deleting dataset from current tab

    delete_button_current_tab = ttk.Button(f1, text="Delete DataSet", command=delete_dataset_current_tab)

    # use the grid geometry manager to place the widgets
    l1.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
    e1.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
    b1.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
    refresh_button.grid(row=0, column=3, sticky=tk.E, padx=10, pady=10)
    delete_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
    delete_entry.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)
    delete_button.grid(row=1, column=2, sticky=tk.E, padx=10, pady=10) 

    b = []
    for i in os.listdir("./Parent/Dataset"):
        dataset_name = i
        dataset_button = ttk.Button(f1, text=dataset_name, command=lambda name=dataset_name: display_dataset_directory(name))
        b.append(dataset_button)

    for i, button in enumerate(b):
        button.grid(row=int(i/4) + 3, column=int(i%4), sticky=tk.W, padx=15, pady=15)

    # add the frame to the notebook as the first tab
    notebook.add(f1, text="DataSets")

    # create a frame for the second tab
    frame2 = ttk.Frame(notebook)

    # create a label widget for the search term
    label2 = ttk.Label(frame2, text="Search Term:")

    # create an entry widget for the search term
    entry2 = ttk.Entry(frame2)

    # create a button widget for searching
    button5 = ttk.Button(frame2, text="Search")

    # create a button widget for downloading
    button6 = ttk.Button(frame2, text="Download")

    # create three buttons for selecting the search criteria
    button7 = ttk.Radiobutton(frame2, text="image")
    button8 = ttk.Radiobutton(frame2, text="selected txt/image")
    button9 = ttk.Radiobutton(frame2, text="txt/image")

    # use the grid geometry manager to place the widgets
    label2.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
    entry2.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
    button5.grid(row=0, column=2, sticky=tk.E, padx=10, pady=10)
    button6.grid(row=1, column=2, sticky=tk.E, padx=10, pady=10)
    button7.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
    button8.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)
    button9.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

    # add the frame to the notebook as the second tab
    notebook.add(frame2, text="Search Screen")

    # pack the notebook into the root window
    notebook.pack(padx=10, pady=10)

    # start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
