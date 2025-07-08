"""FileImageSorter: GUI tool for copying and sorting PNG files by size."""

from pathlib import Path
import shutil
from tkinter import Tk, Button, Label, filedialog, messagebox, StringVar
from PIL import Image

def select_source_folder():
    """Opens a dialog to select the source folder"""
    folder = filedialog.askdirectory(title="Select a folder to search for PNGs")
    if folder:
        source_folder.set(folder)
        status_label.config(text=f"Folder selected: {folder}")

def select_destination_folder():
    """Open dialog to select the destination folder where images will be copied"""
    folder = filedialog.askdirectory(title="Select a folder to save the PNG")
    if folder:
        destination_folder.set(folder)
        status_label.config(text=f"PNGs will be saved in: {folder}")

def copy_png_file(src: Path, dst_dir: Path, file_count: dict):
    """Copies a PNG file to the destination folder, adding a number if the filename already exists."""
    base_name = src.stem
    ext = src.suffix
    if file_count.get(base_name, 0):
        file_count[base_name] += 1
        new_name = f"{base_name}_{file_count[base_name]}{ext}"
    else:
        file_count[base_name] = 0
        new_name = src.name

    dst_path = dst_dir / new_name
    shutil.copy2(src, dst_path)

def get_all_png_files(folder: Path):
    """Returns a list of all PNG files in the given folder and its subfolders."""
    return [p for p in folder.rglob("*.png") if p.is_file()]

def find_and_copy_png():
    """Search for PNG files and copy them to the selected destination folder, avoiding overwrites"""
    source = Path(source_folder.get())
    destination = Path(destination_folder.get())

    if not source or not destination:
        messagebox.showerror("Error", "Please select both folders")
        return

    destination.mkdir(parents=True, exist_ok=True)

    file_count = {}
    png_files = get_all_png_files(source)

    for file in png_files:
        copy_png_file(file, destination, file_count)

    if png_files:
        status_label.config(text=f"Found and copied {len(png_files)} PNG files")
    else:
        status_label.config(text="PNG files not found")

def sort_by_size():
    """Sort and copy PNG files into subfolders based on image dimensions."""
    source = Path(source_folder.get())
    destination = Path(destination_folder.get())

    if not source or not destination:
        messagebox.showerror("Error", "Please select both folders")
        return

    destination.mkdir(parents=True, exist_ok=True)

    png_files = get_all_png_files(source)
    sorted_count = 0

    for file in png_files:
        try:
            with Image.open(file) as img:
                size_folder = f"{img.width}x{img.height}"
                target_dir = destination / size_folder
                target_dir.mkdir(exist_ok=True)
                shutil.copy2(file, target_dir / file.name)
                sorted_count += 1
        except Exception as e:
            messagebox.showwarning("Error", f"Failed to process file {file.name}: {e}")

    if sorted_count:
        status_label.config(text=f"Found and sorted {sorted_count} PNG files")
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

