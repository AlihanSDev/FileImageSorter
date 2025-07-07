# 🖼️ FileImageSorter

A simple and user-friendly Python app for organizing your PNG images.

This tool allows you to:

- 🔍 Find all PNG files in a selected folder (including subfolders)
- 📁 Copy them to another folder without overwriting
- 📐 Sort PNG files by their resolution into structured folders (like `1920x1080`, `128x128`, etc.)

---

## 🚀 How to Use

1. **Run the app**
2. Click **"Select a folder"** to choose a source folder with PNG files
3. Click **"Select a folder"** to choose a destination folder
4. Choose an action:
   - ✅ **"Find and copy PNG"** — copy all found PNGs to the destination
   - 🗂️ **"Sort PNGs by size"** — organize them into folders based on resolution

---

## 🧠 Features

- Works recursively through subdirectories
- Handles errors if image files are corrupted or unreadable
- Clean and intuitive GUI built with `tkinter`

---

## 📦 Requirements

- Python 3.7+
- [Pillow (PIL)](https://pypi.org/project/Pillow/)

Install dependencies:

```bash
pip install pillow
