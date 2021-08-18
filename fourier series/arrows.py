from cmath import pi, exp, sqrt
import pygame
from svg.path import parse_path

i = sqrt(-1)
center_point = complex(0, 0)


class ErrorChecker:
    @staticmethod
    def check_complex(maybe_complex):
        if isinstance(maybe_complex, complex):
            return maybe_complex
        else:
            raise TypeError('The origin must be a complex number')

    @staticmethod
    def check_int(maybe_int):
        if isinstance(maybe_int, int):
            return maybe_int
        else:
            raise TypeError('The origin must be a int')


class Arrow(ErrorChecker):
    def __init__(self, origin, angular_speed, original_state):
        self._origin = self.check_complex(origin)
        self._angle_speed = self.check_int(angular_speed)
        self._original_state = original_state
        self._tip = self.rotation_equation(0)

    def change_origin(self, other):
        self._origin = self.check_complex(other.get_tip())

    def get_origin(self):
        return self._origin

    def rotation_equation(self, at_time):
        return self._origin + self._original_state * exp(self._angle_speed * 2 * pi * i * at_time)

    def change_tip(self, at_time):
        self._tip = self.rotation_equation(at_time)

    def get_tip(self):
        return self._tip

    def move(self, other, at_time):
        self.change_origin(other)
        self.change_tip(at_time)



class SVG:
    def __init__(self, path):
        self.path = parse_path(path)


class OriginalStateCal(SVG):
    def calculate_average_point(self, number):
        n = 30000
        dt = 1/n
        sum_of_points = complex(0, 0)
        for j in range(n+1):
            at_time = j/n
            sum_of_points += self.path.point(at_time) * exp(-number*2*pi*i*at_time) * dt
        return sum_of_points


class ArrowFactory(OriginalStateCal):
    def __init__(self, num_of_arrows, path):
        super().__init__(path)
        self.num_of_arrows = num_of_arrows

    def get_all_arrows(self):
        list_of_arrows = []
        for index, num in enumerate(range(-self.num_of_arrows, self.num_of_arrows)):
            if len(list_of_arrows) == 0:
                list_of_arrows.append(self.create_arrow(center_point,
                                                        num,
                                                        self.calculate_average_point(num)))
            else:
                list_of_arrows.append(self.create_arrow(list_of_arrows[index-1].get_tip(),
                                                        num,
                                                        self.calculate_average_point(num)))
        return list_of_arrows

    @staticmethod
    def create_arrow(origin, speed, original_state):
        return Arrow(origin, speed, original_state)


class DisplayConverter:
    def __init__(self, width=600, height=400, scale=0.5):
        self.height_half = height/4
        self.width_half = width/4
        self.scale = scale

    def convert(self, complex_point):
        return self.scale*complex_point.real + self.width_half, self.scale*complex_point.imag + self.height_half

    @staticmethod
    def round(float_point):
        return round(float_point[0]), round(float_point[1])



class Board(DisplayConverter):
    def __init__(self, width=600, height=400,  caption='Fourier series', scale=5):
        super().__init__(width, height, scale)
        self.__caption = caption
        self.__width = width
        self.__height = height
        self.__size = width, height
        self.White = (255, 255, 255)
        self.Yellow = (255, 255, 0)
        self.Black = (0, 0, 0)

        pygame.init()
        self.screen = pygame.display.set_mode(self.__size)
        pygame.display.set_caption(self.__caption)

        self.__running = None

    def set_up(self):
        self.__running = True

    def terminate(self):
        self.__running = False

    def is_running(self):
        return self.__running

    def draw(self, arrow):
        pygame.draw.line(self.screen, self.White, self.convert(arrow.get_origin()), self.convert(arrow.get_tip()))

    def fill(self, been_there):
        self.screen.fill(self.Black)
        for dot in been_there:
            dot = self.round(self.convert(dot))
            self.screen.set_at(dot, self.Yellow)




