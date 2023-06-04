from colorama import Fore, Style
from importlib.resources import files

INF = float("+inf")

DEF_FONT_PATH = files("traffsimpy.resources").joinpath("jbmono.ttf")
DEF_ARROW_PATH = files("traffsimpy.resources").joinpath("chevron.svg")

TXT_RED = Fore.RED
TXT_BOLD = Style.BRIGHT
TXT_RESET = Style.RESET_ALL

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BLUE_BG = (237, 254, 249)
BLUE_GRAY_BG = (236, 239, 241)

BLUE_TXT_BG = (227, 249, 242)
BLUE_GRAY_TXT_BG = (176, 190, 197)

BLUE_ROAD = (193, 205, 205)
BLUE_GRAY_ROAD = (207, 216, 220)

BLUE_GREEN_CAR = (143, 188, 143)

RED_TL = (221, 44, 0)
ORANGE_TL = (255, 145, 0)
GREEN_TL = (100, 221, 23)

RED_SS = (198, 40, 40)

PURPLE_SENSOR = (124, 77, 255)
UNITS_OF_ATTR = {"t": "s", "date_of_birth": "s", "age": "s", "v": "m/s", "a": "m/s²", "length": "m", "width": "m", "total_d": "m", "d(t)": "m", "v(t)": "m/s", "a(t)": "m/s²"}

ROGB_GRADIENT = [(183, 28, 28), (186, 35, 28), (190, 43, 29), (193, 50, 29), (197, 57, 30), (200, 65, 30), (204, 72, 31), (207, 80, 31), (211, 87, 32), (214, 94, 32), (218, 102, 33), (221, 109, 33), (225, 116, 34), (228, 124, 34), (232, 131, 35), (235, 139, 35), (239, 146, 36), (242, 153, 36), (246, 161, 37), (249, 168, 37), (249, 168, 37), (246, 170, 38), (243, 172, 38), (240, 173, 39), (237, 175, 40), (234, 177, 41), (231, 179, 41), (228, 181, 42), (225, 182, 43), (222, 184, 44), (219, 186, 44), (216, 188, 45), (213, 189, 46), (210, 191, 47), (207, 193, 47), (204, 195, 48), (201, 197, 49), (198, 198, 50), (195, 200, 50), (192, 202, 51), (192, 202, 51), (189, 202, 52), (186, 201, 53), (184, 201, 55), (181, 201, 56), (178, 200, 57), (175, 200, 58), (172, 199, 59), (170, 199, 61), (167, 199, 62), (164, 198, 63), (161, 198, 64), (159, 198, 66), (156, 197, 67), (153, 197, 68), (150, 196, 69), (147, 196, 70), (145, 196, 72), (142, 195, 73), (139, 195, 74), (139, 195, 74), (132, 193, 82), (125, 191, 90), (118, 189, 98), (110, 187, 107), (103, 184, 115), (96, 182, 123), (89, 180, 131), (82, 178, 139), (75, 176, 147), (67, 174, 156), (60, 172, 164), (53, 170, 172), (46, 168, 180), (39, 166, 188), (32, 163, 196), (24, 161, 205), (17, 159, 213), (10, 157, 221), (3, 155, 229)]
