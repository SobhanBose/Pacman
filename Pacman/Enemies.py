from pygame.math import Vector2
import pygame.display
from .configs import *

class Enemy:
    color_dict = {'2': ENEMY_COLOR_BLUE, '3':ENEMY_COLOR_PINK, '4':ENEMY_COLOR_YELLOW, '5':ENEMY_COLOR_RED}
    def __init__(self, pos: Vector2, behaviour: str) -> None:
        self.__radius = ENEMY_RADIUS
        self.__behaviour = behaviour
        self.__color = self.updateEnemyColor(self.__behaviour)
        self.__grid_pos = pos
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)


    def updateEnemyColor(self, behaviour: str) -> None:
        return Enemy.color_dict[behaviour]


    def updateEnemy(self) -> None:
        pass


    def drawEnemy(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, self.__color, (self.__pix_pos.x, self.__pix_pos.y), self.__radius)