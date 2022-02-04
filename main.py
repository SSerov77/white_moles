import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_one import Ui_Form
# from geocoder import get_coordinates
# from mapapi_PG import show_map


# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def main(self):
        toponym_to_find = ' '.join(sys.argv[1:])
        if toponym_to_find:
            lat, lon = get_coordinates(toponym_to_find)
            ll_spn = f'll={lat},{lon}&spn=0.005,0.005'
            show_map(ll_spn, map)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
