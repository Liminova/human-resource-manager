class Position:
    def __init__(self, x: float, y: float, increment_by_x: float = 0, increment_by_y: float = 0):
        self.__x = x
        self.__y = y
        self.__increment_by_x = increment_by_x
        self.__increment_by_y = increment_by_y

    @property
    def x(self):
        self.__x += self.__increment_by_x
        return self.__x

    @property
    def y(self):
        self.__y += self.__increment_by_y
        return self.__y
