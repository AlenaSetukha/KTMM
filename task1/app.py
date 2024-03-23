import sys

from Main_Window import MainWindow
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
    return


if __name__ == "__main__":
    main()
