# 🖼️ FileImageSorter

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=15&pause=1000&color=38F79C&width=435&lines=%F0%9F%93%82+Select+a+folder+containing+PNG+images+;%F0%9F%96%B1%EF%B8%8F+Choose+where+to+save+the+results+;%F0%9F%A7%B9+Copy+or+sort+images+by+their+resolution)](https://git.io/typing-svg)

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
- Clean and intuitive GUI built with `PyQt5`

---

## 📦 Requirements

- Python 3.7+
- [PyQt5](https://pypi.org/project/PyQt5/)
- [Pillow (PIL)](https://pypi.org/project/Pillow/)

Install dependencies:

```bash
pip install pyqt5 pillow
