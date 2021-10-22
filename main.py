from PyQt5.QtWidgets import *
from MainWindow import MainWindow

def main():
    app = QApplication([])
    window = MainWindow()
    app.exec()

if __name__ == '__main__':
    main()