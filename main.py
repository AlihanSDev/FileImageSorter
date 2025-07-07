import os
import shutil
from tkinter import Tk, Button, Label, filedialog, messagebox, StringVar
from PIL import Image

def select_source_folder():
    folder = filedialog.askdirectory(title="Select a folder to search for PNGs")
    if folder:
        source_folder.set(folder)
        status_label.config(text=f"Folder selected: {folder}")

def select_destination_folder():
    folder = filedialog.askdirectory(title="Select a folder to save the PNG")
    if folder:
        destination_folder.set(folder)
        status_label.config(text=f"PNGs will be saved in: {folder}")

def find_and_copy_png():
    source = source_folder.get()
    destination = destination_folder.get()

    if not source or not destination:
        messagebox.showerror("Error", "Please select both folders")
        return

    os.makedirs(destination, exist_ok=True)

    file_count = {}

    png_files_found = 0
    for root, _, files in os.walk(source):
        for file in files:
            if file.lower().endswith(".png"):
                source_file_path = os.path.join(root, file)
                base_name, ext = os.path.splitext(file)

                if base_name in file_count:
                    file_count[base_name] += 1
                    new_file_name = f"{base_name}_{file_count[base_name]}{ext}"
                else:
                    file_count[base_name] = 0
                    new_file_name = file

                destination_file_path = os.path.join(destination, new_file_name)

                # Копируем файл
                shutil.copy2(source_file_path, destination_file_path)
                png_files_found += 1

    if png_files_found > 0:
        status_label.config(text=f"Found and copied {png_files_found} PNG files")
    else:
        status_label.config(text="PNG files not found")

def sort_by_size():
    source = source_folder.get()
    destination = destination_folder.get()

    if not source or not destination:
        messagebox.showerror("Error", "Please select both folders")
        return

    os.makedirs(destination, exist_ok=True)

    size_folders = {}

    png_files_found = 0
    for root, _, files in os.walk(source):
        for file in files:
            if file.lower().endswith(".png"):
                source_file_path = os.path.join(root, file)
                try:
                    with Image.open(source_file_path) as img:
                        width, height = img.size
                        size_key = f"{width}x{height}"

                        if size_key not in size_folders:
                            size_folder_path = os.path.join(destination, size_key)
                            os.makedirs(size_folder_path, exist_ok=True)
                            size_folders[size_key] = size_folder_path

                        destination_file_path = os.path.join(size_folders[size_key], file)
                        shutil.copy2(source_file_path, destination_file_path)
                        png_files_found += 1
                except Exception as e:
                    messagebox.showwarning("Error", f"Failed to process file {file}: {e}")

    if png_files_found > 0:
        status_label.config(text=f"Found and sorted {png_files_found} PNG files")
    else:
        status_label.config(text="PNG files not found")

root = Tk()
root.title("FileImageSorter")

source_folder = StringVar()
destination_folder = StringVar()

Label(root, text="Select a folder to search for PNGs:").pack(pady=5)
Button(root, text="Select a folder", command=select_source_folder).pack(pady=5)

Label(root, text="Select a folder to save the PNG:").pack(pady=5)
Button(root, text="Select a folder", command=select_destination_folder).pack(pady=5)

Button(root, text="Find and copy PNG", command=find_and_copy_png).pack(pady=10)

Button(root, text="Sort PNGs by size", command=sort_by_size).pack(pady=10)

status_label = Label(root, text="Waiting for action...", fg="blue")
status_label.pack(pady=10)

root.mainloop()