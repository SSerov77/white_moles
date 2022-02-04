import requests

class Map:
    def __init__(self, x_cords=51.768205, y_cords=55.096964, zoom=10, type_map='map'):
        self.x_cords = x_cords
        self.y_cords = y_cords
        self.zoom = zoom
        self.type_map = type_map

    def load_map(self):
        map_request = f'https://static-maps.yandex.ru/1.x/?ll={self.x_cords},{self.y_cords}&spn=0.016457,0.00619&l={self.type_map}'

        res = requests.get(map_request)

        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(res.content)
        except IOError:
            pass
