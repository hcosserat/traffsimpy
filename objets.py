from res import *
from mathsandutils import *


ids = {-1: None}


def new_id(obj, obj_id=None):
    if obj_id is None:
        obj_id = max(ids.keys()) + 1
    ids[obj_id] = obj
    return obj_id


class CarFactory:
    def __init__(self, crea_func, fact_func, obj_id=None):
        """
        Création de voitures à l'entrée d'une route.

        :param crea_func: fonction de choix de voiture à créer, "rand_color", "rand_length", "rand_width", "{'arg': val}"
        :param fact_func: fonction de fréquence de création de voiture
        """
        self.id = new_id(self, obj_id)

        self.crea_func = self.generic_creafunc(crea_func) if isinstance(crea_func, (str, list)) else crea_func
        self.fact_func = fact_func

    def __str__(self):
        return f"CarFactory(id={self.id})"

    def factory(self, args_crea, args_fact):
        """
        :param args_crea: args de choix de voiture
        :param args_fact: args de fréquence de création
        """
        if self.fact_func and self.fact_func(**args_crea):
            if self.crea_func is None:
                returning = Car()
            else:
                returning = self.crea_func(**args_fact)
            log(f"{self} is creating {returning}", 2)
            return returning

    @staticmethod
    def generic_creafunc(func_name):
        if isinstance(func_name, str):
            func_name = [func_name]

        kwargs = {"v": 200, "a": 0, "color": VOITURE_BLEUVERT, "w": 24, "l": 30}

        def crea_func(*a, **kw):
            car = Car(**kwargs)
            if "rand_color" in func_name:
                kwargs["color"] = np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)
            if "rand_length" in func_name:
                kwargs["l"] = np.random.randint(25, 45)
            if "rand_width" in func_name:
                kwargs["w"] = np.random.randint(18, 24)
            try:
                attrs_dic = json.loads(func_name[0].replace("'", '"'))
            except ValueError:
                attrs_dic = {}
            for attr in attrs_dic:
                setattr(car, attr, attrs_dic[attr])
            return car

        return crea_func


class CarSorter:
    def __init__(self, prob_dic: dict = None, sort_func=None):
        """
        Gestion des voitures à la sortie d'une route. Nécessite soit prob_dic, soit sort_func.

        :param prob_dic: Dictionnaire associant une probabilité à une autre route
        :param sort_func: Fonction de tri
        """
        if prob_dic:
            self.method = "probs"
            probs, roads = [], []
            for p in prob_dic:
                probs.append(prob_dic[p])
                roads.append(p)

            def sort_func(*args, **kwargs):
                return ids[np.random.choice(roads, p=probs)]

        elif sort_func is None:
            self.method = None

            def sort_func(*args, **kwargs):
                pass

        else:
            self.method = "func"

        self.sort_func = sort_func

    def sorter(self, *args, **kwargs):
        return self.sort_func(*args, **kwargs)


class Road:
    def __init__(self, start=(0, 0), end=(1, 1), width=32, car_factory: CarFactory = None, color=ROUTE_BLEU, obj_id=None):
        self.id = new_id(self, obj_id)
        self.start, self.end = start, end
        self.width = width
        self.color = color

        (startx, starty), (endx, endy) = self.start, self.end
        self.length = np.sqrt((startx - endx) * (startx - endx) + (starty - endy) * (starty - endy))
        self.vd = vect_dir(self.start, self.end)  # vecteur directeur de la route
        vnx, vny = vect_norm(self.vd, self.width / 2)  # vecteur normal pour les coord des coins
        self.coins = (startx + vnx, starty + vny), (startx - vnx, starty - vny), (endx - vnx, endy - vny), (
                      endx + vnx, endy + vny)
        self.angle = angle(self.vd)

        self.car_factory = car_factory if car_factory is not None else CarFactory("rand_colors", None)
        self.cars: list[Car] = []
        self.car_sorter = CarSorter()
        self.exiting_cars: list[Car] = []

    def __str__(self):
        return f"Route(id={self.id}, length={round(self.length, 2)}, coins={rec_round(self.coins, 2)}, color={self.color})"

    @property
    def arrows_coord(self):
        rarete = 100  # inverse de la fréquence des flèches
        num = int(self.length/rarete)  # nombre de flèches pour la route
        x, y = self.start
        vx, vy = self.vd
        x, y = x + vx * rarete / 2, y + vy * rarete / 2
        arrows = []
        for i in range(num):
            arrows.append((x, y))
            x, y = x + vx * rarete, y + vy * rarete
        log(f"{arrows=}", 3)
        return arrows

    def refresh_cars_coords(self, dt=1/60):
        """Bouge les voitures de la route à leurs position après dt."""
        for car in self.cars:
            d, v, a = coord_mvm_apres_dt(d=car.d, v=car.v, a=car.a, dt=dt)
            vdx, vdy = self.vd
            dx, dy = vdx * d, vdy * d

            car.d, car.v, car.a = d, v, a  # mise à jour des coords du mvm

            startx, starty = self.start
            car.x, car.y = startx + dx, starty + dy  # mise à jour des coords de pos

            vnx, vny = vect_norm(self.vd, car.width / 2)
            c1, c2 = (car.x + vnx, car.y + vny), (car.x - vnx, car.y - vny)
            c3, c4 = (car.x - vnx + car.length * vdx, car.y - vny + car.length * vdy), (
                      car.x + vnx + car.length * vdx, car.y + vny + car.length * vdy)

            car.coins = c1, c2, c3, c4

            log(f"Updating {car} of {self}", 3)

            if d + car.length*int(self.car_sorter.method is not None) >= self.length:  # si le sorter de la route est None, attendre
                self.exiting_cars.append(car)                                          # que la voiture soit totalement partie pour la retirer
                self.cars.remove(car)
                log(f"Removing {car} of {self}", 2)

    def new_car(self, car):
        if car is not None:
            vnx, vny = vect_norm(self.vd, car.width / 2)  # vecteur normal pour les coord des coins
            vdx, vdy = self.vd
            startx, starty = self.start
            endx, endy = startx + car.length * vdx, starty + car.length * vdy
            car.coins = (startx + vnx, starty + vny), (startx - vnx, starty - vny), (endx - vnx, endy - vny), (
                         endx + vnx, endy + vny)
            car.x, car.y = self.start
            car.d = 0
            self.cars.append(car)
            log(f"Creating {car} on road {self}", 2)


class Car:
    def __init__(self, v=200, a=0, color=VOITURE_BLEUVERT, l=30, w=24, obj_id=None):
        self.id = new_id(self, obj_id)
        self.color = color
        self.length, self.width = l, w

        self.d = 0  # distance du derrière depuis le début de la route
        self.x, self.y = 0, 0  # position du mileu du derrière dans la fenêtre
        self.v = v  # vitesse
        self.a = a  # acceleration
        self.coins = ((0, 0), (0, 0), (0, 0), (0, 0))  # coordonnées des coins, pour affichage

    def __str__(self):
        return f"Car(id={self.id}, x={self.x}, y={self.y}, d={self.d}, v={self.v}, a={self.a}, coins={rec_round(self.coins)}, color{self.color})"


class Feu:
    def __init__(self, x, y, state, obj_id=None):
        self.id = new_id(self, obj_id)
        self.x, self.y = x, y
        self.state = state

    def __str__(self):
        return f"Feu(id={self.id}, x={self.x}, y={self.y}, state={self.state})"