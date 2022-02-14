import math
import os
import sys

import requests

from PyQt5.QtCore import Qt

LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.02
coord_to_geo_x = 0.0000428  # Пропорции пиксельных и географических координат.
coord_to_geo_y = 0.0000428


# Структура для хранения результатов поиска:
# координаты объекта, его название и почтовый индекс, если есть.
class SearchResult(object):
    def __init__(self, point, address, postal_code=None):
        self.point = point
        self.address = address
        self.postal_code = postal_code

    def __str__(self):
        return f'{self.address}, {self.postal_code}'


class MapParams:
    # Параметры по умолчанию.
    def __init__(self, lat=55.096955, lon=51.768199, zoom=13, type='map'):
        self.lat = lat  # Координаты центра карты на старте.
        self.lon = lon
        self.zoom = zoom  # Масштаб карты на старте.
        self.type = type  # Тип карты на старте.

        self.search_result = None  # Найденный объект для отображения на карте.
        # self.use_postal_code = False

    # Обновление параметров карты по нажатой клавише.
    def update(self, event):
        print(event.key)
        if event.key() == Qt.Key_PageUp and self.zoom < 19:  # PG_UP
            self.zoom += 1
        elif event.key == Qt.Key_PageDown and self.zoom > 2:  # PG_DOWN
            self.zoom -= 1
        elif event.key == Qt.Key_Left:  # LEFT_ARROW
            self.lon -= LON_STEP * math.pow(2, 13 - self.zoom)
        elif event.key == Qt.Key_Right:  # RIGHT_ARROW
            self.lon += LON_STEP * math.pow(2, 13 - self.zoom)
        elif event.key == Qt.Key_Up and self.lat < 85:  # UP_ARROW
            self.lat += LAT_STEP * math.pow(2, 13 - self.zoom)
        elif event.key == Qt.Key_Down and self.lat > -85:  # DOWN_ARROW
            self.lat -= LAT_STEP * math.pow(2, 13 - self.zoom)
        elif event.key == 49:  # 1
            self.type = "map"
        elif event.key == 50:  # 2
            self.type = "sat"
        elif event.key == 51:  # 3
            self.type = "sat,skl"

        if self.lon > 180: self.lon -= 360
        if self.lon < -180: self.lon += 360

    # Преобразование экранных координат в географические.
    def screen_to_geo(self, pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lx = self.lon + dx * coord_to_geo_x * math.pow(2, 15 - self.zoom)
        ly = self.lat + dy * coord_to_geo_y * math.cos(math.radians(self.lat)) * math.pow(2,
                                                                                          15 - self.zoom)
        return lx, ly


# Создание карты с соответствующими параметрами.
def load_map(MapParams):
    mp = MapParams()

    map_request = f"https://static-maps.yandex.ru/1.x/?ll={mp.lat},{mp.lon}&size=450,450&z={mp.zoom}&l={mp.type}&pt=55.096955,70.753630,pmwtm1~37.64,55.76363,pmwtm99"

    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file
