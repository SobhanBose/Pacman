import pygame
from .configs import *

class Player:
    def __init__(self) -> None:
        self.__grid_pos = PLAYER_START_POS
        self.__pix_pos = pygame.math.Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
    
    
    def update(self, screen) -> None:
        pass


    def drawPlayer(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, PLAYER_COLOR, (self.__pix_pos.x, self.__pix_pos.y), CELL_WIDTH//2-2)