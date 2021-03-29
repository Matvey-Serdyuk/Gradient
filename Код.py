import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QMessageBox
from PIL import Image
from os import system


class Example(QWidget):
    def __init__(self):
        # Что-то
        super().__init__()
        # Создание окна
        self.setWindowTitle('Шедевр')
        # Виджеты
        # Ввод Широта
        self.input_width = QLineEdit()
        self.input_width.setText("width")
        # Ввод Высота
        self.input_height = QLineEdit()
        self.input_height.setText("height")
        # Кнопка Сохранения
        self.save = QPushButton()
        self.save.setText("Сохранить")
        self.save_boolean = False
        self.save.clicked.connect(self.get_image)
        # Ввод сида
        self.input_seed = QLineEdit()
        self.input_seed.setText("Seed")
        # кнопка Ввода
        self.input_button = QPushButton()
        self.input_button.setText("Ввести Seed")
        self.input_button.clicked.connect(self.get_mini_image)
        # Изображение
        self.pixmap = QPixmap()
        self.image = QLabel()
        # Layouts
        self.main_layout = QVBoxLayout()
        self.hw_layout = QHBoxLayout()
        # Расположение в Layout
        self.hw_layout.addWidget(self.input_width)
        self.hw_layout.addWidget(self.input_height)
        self.main_layout.addLayout(self.hw_layout)
        self.main_layout.addWidget(self.save)
        self.main_layout.addWidget(self.input_seed)
        self.main_layout.addWidget(self.input_button)
        self.main_layout.addWidget(self.image)
        self.setLayout(self.main_layout)

    def get_mini_image(self):
        boolean = True
        while boolean:
            try:
                self.seed = int(self.input_seed.text())
                boolean = False
            except ValueError:
                QMessageBox.about(self, "Не правильный формат ввода",
                                  "Не правильно указан Seed")
                return 0
        s = 0
        # Подбираем r, g, b и  r1, g1, b1
        # подбор r
        for i in range(15408):
            s = (self.seed * s + 12) % 27326
        s1 = 0
        for i in range(s):
            s1 = (self.seed * s1 + 31) % 14386
        self.r = 0
        for i in range(s1):
            self.r = (s * self.r + self.seed) % 25568
        # подбор g
        s = 0
        for i in range(14383):
            s = (73 * s + self.seed) % 23813
        s1 = 0
        for i in range(s):
            s1 = (self.seed * s1 + 58) % 12638
        self.g = 0
        for i in range(s1):
            self.g = (s * self.g + self.seed) % 25524
        # подбор b
        s = 0
        for i in range(18432):
            s = (self.seed * s + 198) % 30231
        s1 = 0
        for i in range(s):
            s1 = (32 * s1 + self.seed) % 18632
        self.b = 0
        for i in range(s1):
            self.b = (self.seed * self.b + s) % 25587
        # подбор r1
        s = 0
        for i in range(10842):
            s = (198 * s + self.seed) % 8793
        s1 = 0
        for i in range(s):
            s1 = (163 * s1 + self.seed) % 5432
        self.r1 = 0
        for i in range(s1):
            self.r1 = (self.seed * self.r1 + s) % 25575
        # подбор g1
        s = 0
        for i in range(16328):
            s = (321 * s + self.seed) % 19742
        s1 = 0
        for i in range(s):
            s1 = (self.seed * s1 + 93) % 16893
        self.g1 = 0
        for i in range(s):
            self.g1 = (s1 * self.g1 + self.seed) % 25531
        # подбор b1
        s = 0
        for i in range(23941):
            s = (self.seed * s + 231) % 18932
        s1 = 0
        for i in range(s):
            s1 = (421 * s1 + self.seed) % 9871
        self.b1 = 0
        for i in range(s):
            self.b1 = (self.seed * self.b1 + s1) % 25583
        # Делаем так что бы числа стали <= 255
        self.r //= 100
        self.g //= 100
        self.b //= 100
        self.r1 //= 100
        self.g1 //= 100
        self.b1 //= 100
        # Задаем размеры изображения
        width = 256
        height = 128
        # Создаем Изображение
        self.im = Image.new("RGB", (width, height), (self.r, self.g, self.b))
        pix = self.im.load()
        a = self.r - self.r1
        s = self.g - self.g1
        s1 = self.b - self.b1
        if a < 0:
            a1 = -1
        else:
            a1 = 1

        if s < 0:
            s2 = -1
        else:
            s2 = 1

        if s1 < 0:
            s3 = -1
        else:
            s3 = 1
        if a != 0:
            a = width // abs(a)
        else:
            a = width
        if s != 0:
            s = width // abs(s)
        else:
            s = width
        if s1 != 0:
            s1 = width // abs(s1)
        else:
            s1 = width
        for i in range(height):
            r1 = 0
            g1 = 0
            b1 = 0
            for j in range(width):
                r, g, b = pix[j, i]
                if j % a == 0:
                    r1 += a1
                if j % s == 0:
                    g1 += s2
                if j % s1 == 0:
                    b1 += s3
                r -= r1
                g -= g1
                b -= b1
                pix[j, i] = r, g, b
        self.im.save("res.jpg")
        self.pixmap = QPixmap("res.jpg")
        self.image.setPixmap(self.pixmap)
        self.save_boolean = True

    def get_image(self):
        # Проверка правильно ли все введино
        if not self.save_boolean:
            QMessageBox.about(self, "Ошибка", "Вы еще не создали изображение")
            return 0
        boolean = True
        while boolean:
            try:
                width = int(self.input_width.text())
                boolean = False
            except ValueError:
                QMessageBox.about(self, "Не правильный формат ввода",
                                  "Не правильно указан Width")
                return 0
        boolean = True
        while boolean:
            try:
                height = int(self.input_height.text())
                boolean = False
            except ValueError:
                QMessageBox.about(self, "Не правильный формат ввода",
                                  "Не правильно указан Height")
                return 0
        # Выбор папки
        f = QFileDialog.getExistingDirectory(self, "Выбрать папку", "")
        if f == "":
        	return 0
        im = Image.new("RGB", (width, height), (self.r, self.g, self.b))
        pix = im.load()
        a = self.r - self.r1
        s = self.g - self.g1
        s1 = self.b - self.b1
        if a < 0:
            a1 = -1
        else:
            a1 = 1
        if s < 0:
            s2 = -1
        else:
            s2 = 1
        if s1 < 0:
            s3 = -1
        else:
            s3 = 1
        if a != 0:
            a = width // abs(a)
        else:
            a = width
        if s != 0:
            s = width // abs(s)
        else:
            s = width
        if s1 != 0:
            s1 = width // abs(s1)
        else:
            s1 = width
        for i in range(height):
            r1 = 0
            g1 = 0
            b1 = 0
            for j in range(width):
                r, g, b = pix[j, i]
                if j % a == 0:
                    r1 += a1
                if j % s == 0:
                    g1 += s2
                if j % s1 == 0:
                    b1 += s3
                r -= r1
                g -= g1
                b -= b1
                pix[j, i] = r, g, b
        print(f + "/image_seed:" + str(self.seed) + ".jpg")
        im.save(f + "/image_seed_" + str(self.seed) + ".jpg")
        QMessageBox.about(self, "Уведомление",
                          "Все готово)")


# Запуск моего шедевра
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
