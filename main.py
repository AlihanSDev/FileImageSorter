"""FileImageSorter: GUI tool for copying and sorting PNG files by size, using PyQt5"""

from pathlib import Path
import shutil
from PIL import Image
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush
from PyQt5.QtCore import Qt
import sys


class FileImageSorter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FileImageSorter")
        self.setFixedWidth(400)

        self.source_folder = None
        self.destination_folder = None

        self.layout = QVBoxLayout()

        self.label1 = QLabel("Select a folder to search for PNGs:")
        self.layout.addWidget(self.label1)

        self.select_source_btn = QPushButton("Select a folder")
        self.select_source_btn.clicked.connect(self.select_source_folder)
        self.layout.addWidget(self.select_source_btn)

        self.label2 = QLabel("Select a folder to save the PNG:")
        self.layout.addWidget(self.label2)

        self.select_destination_btn = QPushButton("Select a folder")
        self.select_destination_btn.clicked.connect(self.select_destination_folder)
        self.layout.addWidget(self.select_destination_btn)

        self.copy_btn = QPushButton("Find and copy PNG")
        self.copy_btn.clicked.connect(self.find_and_copy_png)
        self.layout.addWidget(self.copy_btn)

        self.sort_btn = QPushButton("Sort PNGs by size")
        self.sort_btn.clicked.connect(self.sort_by_size)
        self.layout.addWidget(self.sort_btn)

        self.status_label = QLabel("Waiting for action...")
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def paintEvent(self, event):
        """Draws a vertical gradient background"""
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#e0f7fa"))
        gradient.setColorAt(1, QColor("#ffffff"))
        painter.fillRect(self.rect(), QBrush(gradient))

    def select_source_folder(self):
        """Opens a folder dialog to select the source directory"""
        folder = QFileDialog.getExistingDirectory(self, "Select a folder to search for PNGs")
        if folder:
            self.source_folder = Path(folder)
            self.status_label.setText(f"Folder selected: {folder}")

    def select_destination_folder(self):
        """Opens a folder dialog to select the destination directory"""
        folder = QFileDialog.getExistingDirectory(self, "Select a folder to save the PNG")
        if folder:
            self.destination_folder = Path(folder)
            self.status_label.setText(f"PNGs will be saved in: {folder}")

    def get_all_png_files(self, folder: Path):
        """Returns a list of all PNG files in the given folder and its subfolders"""
        return [p for p in folder.rglob("*.png") if p.is_file()]

    def ensure_folders_selected(self):
        """Returns True if both folders are selected, otherwise shows an error"""
        if not self.source_folder or not self.destination_folder:
            QMessageBox.critical(self, "Error", "Please select both folders")
            return False
        return True

    def copy_png_file(self, src: Path, dst_dir: Path, file_count: dict):
        """Copies a PNG file to the destination folder, renames if file exists"""
        base_name = src.stem
        ext = src.suffix

        if base_name in file_count:
            file_count[base_name] += 1
            new_name = f"{base_name}_{file_count[base_name]}{ext}"
        else:
            file_count[base_name] = 0
            new_name = src.name

        dst_path = dst_dir / new_name
        while dst_path.exists():
            file_count[base_name] += 1
            new_name = f"{base_name}_{file_count[base_name]}{ext}"
            dst_path = dst_dir / new_name

        shutil.copy2(src, dst_path)

    def find_and_copy_png(self):
        """Finds PNG files and copies them to destination folder without overwriting"""
        if not self.ensure_folders_selected():
            return

        self.destination_folder.mkdir(parents=True, exist_ok=True)
        file_count = {}
        png_files = self.get_all_png_files(self.source_folder)

        for file in png_files:
            self.copy_png_file(file, self.destination_folder, file_count)

        if png_files:
            self.status_label.setText(f"Found and copied {len(png_files)} PNG files")
        else:
            self.status_label.setText("PNG files not found")

    def sort_by_size(self):
        """Sorts PNG files into subfolders based on image dimensions"""
        if not self.ensure_folders_selected():
            return

        self.destination_folder.mkdir(parents=True, exist_ok=True)
        png_files = self.get_all_png_files(self.destination_folder)
        sorted_count = 0

        for file in png_files:
            try:
                with Image.open(file) as img:
                    size_folder = f"{img.width}x{img.height}"
                    target_dir = self.destination_folder / size_folder
                    target_dir.mkdir(exist_ok=True)

                    dst_path = target_dir / file.name
                    count = 1
                    while dst_path.exists():
                        dst_path = target_dir / f"{file.stem}_{count}{file.suffix}"
                        count += 1

                    shutil.copy2(file, dst_path)
                    sorted_count += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to process file {file.name}:\n{e}")

        if sorted_count:
            self.status_label.setText(f"Found and sorted {sorted_count} PNG files")
        else:
            self.status_label.setText("PNG files not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileImageSorter()
    window.show()
    sys.exit(app.exec_())
