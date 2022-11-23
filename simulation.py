import pygame
from objets import *
from draw_tools import *
from res import *


class Simulation:
    def __init__(self, taille_x=1400, taille_y=800, bg_color=FOND_BLEU, logging_level=0):
        """
        Simulation du traffic.

        :param taille_x: largeur de la fenêtre
        :param taille_y: hauteur de la fenêtre
        :param bg_color: couleur de l'arrière plan
        :param logging_level: niveau de logging, 0 = essentiel, 1 = erreur, 2 = info, 3 = debug
        """
        self.id = 0  # identifiant
        ids[0] = self
        globvar["logging_level"] = logging_level  # donne le niveau de log à mathsandutils.py
        self.size = taille_x, taille_y
        self.t = 0.0
        self.frame_count = 0
        self.FPS = 60
        self.dt = 1/self.FPS
        self.over = False

        self.roads: list[Road] = []
        self.road_graph = {}

        pygame.init()

        self.surface = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.surfrect = self.surface.get_rect()
        self.bg_color = bg_color
        self.surface.fill(bg_color)
        self.font = pygame.font.Font("ressources/jbmono.ttf", 15)
        arrow = pygame.image.load("/Users/hippolytecosserat/PycharmProjects/tipe-ts/ressources/arrow.png").convert_alpha()
        self.ARROW = pygame.transform.smoothscale(arrow, (20, 20))

    def start_loop(self):
        """Ouvre une fenêtre et lance la simulation."""
        while not self.over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.over = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.over = True

            self.surface.fill(self.bg_color)  # efface tout

            self.print_infos(f"t = {round(self.t, 2)}")  # affiche l'horloge

            self.show_roads(self.roads)  # affiche les routes

            for road in self.roads:
                road.refresh_cars_coords(dt=self.dt)
                road.new_car(road.car_factory.factory({"t": self.t}, {"t": self.t}))

                for car in road.cars:
                    self.show_car(car)

                for car in road.exiting_cars:
                    new_road = road.car_sorter.sorter(t=self.t)
                    if new_road is not None:
                        new_road.new_car(car)

                road.exiting_cars = []

            pygame.display.flip()
            self.t += self.dt
            self.clock.tick(self.FPS)

    def print_infos(self, info, bg_color=FOND_BLEU):
        """Affiche des infos en haut à gauche de la fenêtre."""
        draw_rect(self.surface, bg_color, (0, 0), 100, 30)
        print_text(self.surface, BLACK, (10, 10), info, self.font)

    def show_car(self, car: Car):
        """Dessine une voiture."""
        draw_polygon(self.surface, car.color, car.coins)

    def show_roads(self, road_list):
        """Affiche des routes."""
        for road in road_list:
            draw_polygon(self.surface, road.color, road.coins)

            rotated_arrow = pygame.transform.rotate(self.ARROW, road.angle)

            for arrow_coord in road.arrows_coords:
                x, y, _ = arrow_coord
                draw_image(self.surface, rotated_arrow, (x, y))

    def create_road(self, start, end, car_factory: CarFactory = None, color=ROUTE_BLEU, w=32, obj_id=None):
        """Créer une route."""
        road = Road(start, end, width=w, color=color, car_factory=car_factory, obj_id=obj_id)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        """Créer des routes droites, renvoie la liste des routes."""
        return [self.create_road(**road) for road in road_list]

    def set_road_graph(self, graph):
        self.road_graph = graph
        for road in self.roads:
            if isinstance(graph[road.id], CarSorter):
                car_sorter = graph[road.id]
            else:
                car_sorter = CarSorter(method=graph[road.id])

            road.car_sorter = car_sorter
