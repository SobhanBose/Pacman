import pygame
from pygame.math import Vector2
import pygame.display
from .configs import *

class Coin:
    def __init__(self, pos: Vector2, isSpecial=False) -> None:
        self.__color = COIN_COLOR
        self.__pos = pos
        self.__is_special = isSpecial
        if self.__is_special:
            self.__radius = COIN_SPECIAL_RADIUS
        else:
            self.__radius = COIN_RADIUS
        self.__has_been_eaten = False
    

    def isSpecial(self) -> bool:
        return self.__is_special


    def getColor(self) -> tuple:
        return self.__color


    def getPos(self) -> Vector2:
        return self.__pos


    def updateCoin(self) -> None:
        pass


    def getHasBeenEaten(self) -> bool:
        return self.__has_been_eaten
        

    def eatCoin(self) -> None:
        self.__has_been_eaten = True
    

    def resetCoin(self) -> None:
        self.__has_been_eaten = False


    def drawCoin(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, COIN_COLOR, (self.__pos.x*CELL_WIDTH+CELL_WIDTH//2+SCREEN_SIZE_BUFFER, self.__pos.y*CELL_HEIGHT+CELL_HEIGHT//2+SCREEN_SIZE_BUFFER), self.__radius)