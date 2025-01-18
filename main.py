import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.filname = None
        self.current_dir = ''
        self.save_dir = 'Modified/'
        self.extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        self.resize(700, 500)
        self.setWindowTitle('Easy Editor')

        self.lb_image = QLabel("Картинка")
        self.lb_image.setAlignment(Qt.AlignCenter)
        self.btn_dir = QPushButton("Папка")
        self.lw_files = QListWidget()
        self.btn_left = QPushButton("Вліво")
        self.btn_right = QPushButton("Вправо")
        self.btn_flip = QPushButton("Дзеркало")
        self.btn_sharp = QPushButton("Різкість")
        self.btn_bw = QPushButton("Ч/Б")

        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(self.btn_dir)
        col1.addWidget(self.lw_files)

        col2.addWidget(self.lb_image, 95)
        row_tools = QHBoxLayout()
        row_tools.addWidget(self.btn_left)
        row_tools.addWidget(self.btn_right)
        row_tools.addWidget(self.btn_flip)
        row_tools.addWidget(self.btn_sharp)
        row_tools.addWidget(self.btn_bw)
        col2.addLayout(row_tools)

        row.addLayout(col1, 20)
        row.addLayout(col2, 80)
        self.setLayout(row)
    
    def setup_connections(self):
        self.btn_dir.clicked.connect(self.show_filename_list)
        self.lw_files.currentRowChanged.connect(self.show_chosen_image)
        self.btn_left.clicked.connect(self.do_left)
        self.btn_right.clicked.connect(self.do_right)
        self.btn_flip.clicked.connect(self.do_flip)
        self.btn_sharp.clicked.connect(self.do_sharpen)
        self.btn_bw.clicked.connect(self.do_bw)

    def filter_files(self, files):
        result = []
        for filename in files:
            for ext in self.extensions:
                if filename.endswith(ext):
                    result.append(filename)
        return result
    
    def show_filename_list(self):
        self.current_dir = QFileDialog.getExistingDirectory()

        if self.current_dir:
            filenames = self.filter_files(os.listdir(self.current_dir))
            self.lw_files.clear()
            for filename in filenames:
                self.lw_files.addItem(filename)

    def show_image(self, path):
        self.lb_image.hide()
        pixmap_image = QPixmap(path)

        w, h = self.lb_image.width(), self.lb_image.height()

        pixmap_image = pixmap_image.scaled(w, h, Qt.KeepAspectRatio)
        self.lb_image.setPixmap(pixmap_image)
        self.lb_image.show()

    def load_image(self, filename):
        self.filename = filename
        image_path = os.path.join(self.current_dir, filename)
        self.image = Image.open(image_path)
        
    def show_chosen_image(self):
        if self.lw_files.currentRow() >= 0:
            filename = self.lw_files.currentItem().text()
            self.load_image(filename)
            self.show_image(os.path.join(self.current_dir, filename))


    def save_Image(self):
        path = os.path.join(self.current_dir, self.save_dir)

        if not(os.path.exists(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        return image_path
    
    def do_bw(self):
        if self.image:
            self.image = self.image.convert('L')
            saved_path = self.save_Image()

    def do_right(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_270)
            saved_path = self.save_image()
            self.show_image(saved_path)

    def do_sharpen(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            saved_path = self.save_image()
            self.show_image(saved_path)

    def do_flip(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            saved_path = self.save_image()
            self.show_image(saved_path)

 

if __name__ == '__main__':
    app = QApplication([])
    editor = ImageEditor()
    editor.show()
    app.exec()