import sys
import os
from PIL import Image
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.text_state = "Надпись"
        self.image_index = -1
        self.images = [] 
        self.is_vertical_layout = False
        
        self.load_images()
        
        self.initial_width = 520
        self.initial_height = 320
        
        self.init_ui()
        
    def load_images(self):
        """Загружает список изображений из папки 'images'"""
        images_dir = Path("images")
        if not images_dir.exists():
            print("Не найдена папка images")
            sys.exit(1)
        
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        self.images = sorted([
            str(f) for f in images_dir.iterdir() 
            if f.suffix.lower() in supported_formats
        ])
        
        if not self.images:
            print("Не найдена папка images")
            sys.exit(1)
    
    def init_ui(self):
        """Инициализирует интерфейс"""
        self.setGeometry(100, 100, self.initial_width, self.initial_height)
        self.setMinimumSize(240, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        
        self.label = QLabel(self.text_state)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(160, 40)
        self.label.setMaximumSize(160, 40)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("border: 1px solid black;")
        
        self.button1 = QPushButton("Кнопка 1")
        self.button1.setFixedSize(160, 40)
        self.button1.clicked.connect(self.on_button1_clicked)
        
        self.button2 = QPushButton("Кнопка 2")
        self.button2.setFixedSize(160, 40)
        self.button2.clicked.connect(self.on_button2_clicked)
        
        self.update_layout()
    
    def update_layout(self):
        """Обновляет макет в зависимости от размера окна"""
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        
        window_width = self.width()
        
        if window_width < 440 and window_width >= 240:
            self.create_vertical_layout()
            self.is_vertical_layout = True
        else:
            self.create_horizontal_layout()
            self.is_vertical_layout = False
    
    def create_horizontal_layout(self):
        """Создаёт горизонтальный макет"""
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.label)
        top_layout.addStretch()
        
        middle_layout = QHBoxLayout()
        middle_layout.addSpacing(40)
        middle_layout.addWidget(self.button1)
        middle_layout.addSpacing(120)
        middle_layout.addWidget(self.button2)
        middle_layout.addSpacing(40)
        
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(top_layout)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(middle_layout)
        self.main_layout.addStretch()
    
    def create_vertical_layout(self):
        """Создаёт вертикальный макет"""
        self.main_layout.addStretch()
        
        label_layout = QHBoxLayout()
        label_layout.addStretch()
        label_layout.addWidget(self.label)
        label_layout.addStretch()
        self.main_layout.addLayout(label_layout)
        
        self.main_layout.addSpacing(40)
        
        button1_layout = QHBoxLayout()
        button1_layout.addSpacing(40)
        button1_layout.addWidget(self.button1)
        button1_layout.addSpacing(40)
        self.main_layout.addLayout(button1_layout)
        
        self.main_layout.addSpacing(40)
        
        button2_layout = QHBoxLayout()
        button2_layout.addSpacing(40)
        button2_layout.addWidget(self.button2)
        button2_layout.addSpacing(40)
        self.main_layout.addLayout(button2_layout)
        
        self.main_layout.addStretch()
    
    def on_button1_clicked(self):
        """Обработчик нажатия Кнопки 1"""
        if self.text_state == "Надпись":
            self.text_state = "Привет"
        else:
            self.text_state = "Надпись"
        self.label.setText(self.text_state)
    
    def on_button2_clicked(self):
        """Обработчик нажатия Кнопки 2"""
        if not self.images:
            print("Нет изображений в папке 'images'")
            return
        
        self.image_index = (self.image_index + 1) % (len(self.images) + 1)
        
        if self.image_index == len(self.images):
            self.reset_to_initial()
        else:
            self.load_and_display_image(self.images[self.image_index])
    
    def load_and_display_image(self, image_path):
        """Загружает изображение и подстраивает размер окна"""
        try:
            img = Image.open(image_path)
            img_width, img_height = img.size
            
            screen = QApplication.primaryScreen().geometry()
            max_width = screen.width()
            max_height = screen.height()
            
            if img_width > max_width or img_height > max_height:
                ratio = min(max_width / img_width, max_height / img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img_width, img_height = new_width, new_height
                
                temp_image_path = image_path.replace('.png', '_temp.png').replace('.jpg', '_temp.jpg')
                img.save(temp_image_path)
            else:
                temp_image_path = image_path
            
            min_ui_width = 240
            min_ui_height = 200
            
            new_window_width = max(img_width, min_ui_width)
            new_window_height = max(img_height, min_ui_height)
            
            self.resize(new_window_width, new_window_height)
            
            pixmap = QPixmap(temp_image_path)
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-image: url("{temp_image_path.replace(chr(92), '/')}");
                    background-repeat: no-repeat;
                    background-position: center;
                }}
            """)
            
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            self.reset_to_initial()
    
    def reset_to_initial(self):
        """Возвращает окно в начальное состояние"""
        self.setStyleSheet("")
        self.resize(self.initial_width, self.initial_height)
    
    def resizeEvent(self, event):
        """Обработчик события изменения размера окна"""
        super().resizeEvent(event)
        self.update_layout()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
