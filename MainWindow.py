import os
import time
import threading

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from IconCreator import IconCreator
from Crawler import DsgoMealCrawler
from Utils import get_year_month_day

WIDTH_SIZE = 320
HEIGHT_SIZE = 240
HOUR_MILLI = 1000 * 60 * 60


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.crawler = DsgoMealCrawler()
        self.move_flag = False
        self.tray_icon = None
        self.updater = None

        self.__set_background()
        self.__set_tray_icon()
        self.__update_permanently()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedSize(WIDTH_SIZE, HEIGHT_SIZE)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)

        self.lunch_box = QLabel("lunch", self)
        self.lunch_box.setAlignment(Qt.AlignHCenter)
        self.lunch_box.font().setBold(True)
        self.lunch_box.move(6, 110)
        self.lunch_box.resize(150, 120)

        self.dinner_box = QLabel("dinner", self)
        self.dinner_box.setAlignment(Qt.AlignHCenter)
        self.dinner_box.font().setBold(True)
        self.dinner_box.move(164, 110)
        self.dinner_box.resize(150, 120)

        self.to_tray_button = QPushButton('', self)
        self.to_tray_button.setIcon(QIcon(f'res/to_tray.png'))
        self.to_tray_button.setIconSize(QSize(32, 32))
        self.to_tray_button.resize(32, 32)
        self.to_tray_button.move(284, 16)
        self.to_tray_button.clicked.connect(self.__move_to_tray)

    def __set_background(self):
        bg_img = QImage(f'res/background.jpg') \
            .scaled(QSize(WIDTH_SIZE, HEIGHT_SIZE))

        palette = QPalette()
        palette.setBrush(10, QBrush(bg_img))
        self.setPalette(palette)

    def __set_tray_icon(self):
        self.tray_icon = IconCreator('dsgoMeal', '오늘의 메뉴')\
            .set_icon(f'res/icon.png')\
            .add_menu('열기', self.__restore_from_tray, is_onclick=True)\
            .add_menu('종료', lambda: os._exit(1))

    def __restore_from_tray(self):
        self.show()
        self.tray_icon.stop()

    def __move_to_tray(self):
        self.hide()
        self.tray_icon.run()

    def __update_permanently(self):
        self.updater = threading.Thread(target=self.__update)
        self.updater.start()

    def __update(self):
        date = get_year_month_day()
        lunch, dinner = self.crawler.get_meal_info(date)

        self.lunch_box.setText(lunch)
        self.dinner_box.setText(dinner)
        time.sleep(HOUR_MILLI)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.move_flag = True
            self.origin_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.move_flag:
            self.move(QMouseEvent.globalPos() - self.origin_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.move_flag = False
