import sys

from Main_Window import MainWindow
from PyQt6.QtWidgets import QApplication

# Для запуска необходимо скачать пакет
# xcb-cursor0 или libxcb-cursor0 (чеерез sudo)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
    return


if __name__ == "__main__":
    main()
