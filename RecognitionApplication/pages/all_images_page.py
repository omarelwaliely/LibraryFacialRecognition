from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
import os

class AllImagesWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('All Images')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(100, 100))
        self.listWidget.setStyleSheet("QListWidget { margin: 10px; }")

        self.load_images_from_folder('uploaded_images')
        
        self.layout.addWidget(self.listWidget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("QPushButton { margin: 10px; }")
        self.layout.addWidget(back_button)

        show_button = QPushButton("Show")
        show_button.clicked.connect(self.show_item)
        self.layout.addWidget(show_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_item)
        self.layout.addWidget(delete_button)

        # Connect double-click signal to the slot
        self.listWidget.itemDoubleClicked.connect(self.item_double_clicked)

    def load_images_from_folder(self, folder_path):
        # Load all images from a folder and display them in the list widget
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                item = QListWidgetItem()
                pixmap = QPixmap(os.path.join(folder_path, filename))
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                item.setIcon(QIcon(pixmap))
                item.setText(filename)
                self.listWidget.addItem(item)

    def show_item(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            item_text = current_item.text()
            print(f"Selected item text: {item_text}")
            # Optionally, show a message box with the selected item's text
            QMessageBox.information(self, "Selected Item", f"Selected item: {item_text}")

    def delete_item(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            item_text = current_item.text()
            reply = QMessageBox.question(self, 'Delete Confirmation',
                                         f"Are you sure you want to delete {item_text}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Delete the file from the folder
                folder_path = 'uploaded_images'
                file_path = os.path.join(folder_path, item_text)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.listWidget.takeItem(self.listWidget.row(current_item))
                    QMessageBox.information(self, "Delete", f"{item_text} has been deleted.")
                else:
                    QMessageBox.warning(self, "Delete", f"{item_text} not found.")

    def item_double_clicked(self, item):
        current_item = self.listWidget.currentItem()
        if current_item:
            item_text = current_item.text()
            print(f"Double-clicked on: {item_text}")

            from .labeling_picture_page import LabellingPic
            self.label_image = LabellingPic(item_text)
            self.label_image.show()

    def go_back(self):
        self.close()
