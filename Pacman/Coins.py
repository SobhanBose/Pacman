import pygame
from pygame.math import Vector2
import pygame.display
from .configs import *

class Coin:
    def __init__(self, pos: Vector2) -> None:
        self.__color = COIN_COLOR
        self.__radius = COIN_RADIUS
        self.__pos = pos
    
    def getColor(self) -> tuple:
        return self.__color


    def getPos(self) -> Vector2:
        return self.__pos


    def updateCoin(self) -> None:
        pass


    def drawCoin(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, COIN_COLOR, (self.__pos.x*CELL_WIDTH+CELL_WIDTH//2+SCREEN_SIZE_BUFFER, self.__pos.y*CELL_HEIGHT+CELL_HEIGHT//2+SCREEN_SIZE_BUFFER), 2)