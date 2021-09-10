import pygame
from pygame.math import Vector2
from .configs import *

class Player:
    def __init__(self) -> None:
        self.__grid_pos = PLAYER_START_POS
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
        self.__direction = Vector2(1, 0)
        self.__temp_direction = None
        self.__able_to_move = True
        self.__score = 0

    
    def getPixPos(self) -> Vector2:
        return self.__pix_pos

    
    def getGridPos(self) -> Vector2:
        return self.__grid_pos
    

    def getScore(self) -> int:
        return self.__score


    def canMove(self, walls: list) -> bool:
        if Vector2(self.__grid_pos+self.__direction) in walls:
            return False
        return True
    

    def time_to_move(self):
        if int(self.__pix_pos.x) % CELL_WIDTH == 0:
            if self.__direction == Vector2(1, 0) or self.__direction == Vector2(-1, 0) or self.__direction == Vector2(0, 0):
                return True
        if int(self.__pix_pos.y) % CELL_HEIGHT == 0:
            if self.__direction == Vector2(0, 1) or self.__direction == Vector2(0, -1) or self.__direction == Vector2(0, 0):
                return True
        return False


    def update(self, screen: pygame.display, walls: list) -> None:
        if self.__able_to_move:
            self.__pix_pos += self.__direction
        if self.time_to_move():
            if self.__temp_direction != None:
                self.__direction = self.__temp_direction
            self.__able_to_move = self.canMove(walls)

        # self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER+CELL_WIDTH//2)//CELL_WIDTH-1
        # self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)//CELL_HEIGHT-1

        self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER)//CELL_WIDTH
        self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER)//CELL_HEIGHT


    def drawPlayer(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, PLAYER_COLOR, (self.__pix_pos.x, self.__pix_pos.y), CELL_WIDTH//2-2)

        # pygame.draw.rect(screen, RED, (self.__grid_pos[0]*CELL_WIDTH+SCREEN_SIZE_BUFFER, self.__grid_pos[1]*CELL_HEIGHT+SCREEN_SIZE_BUFFER, CELL_WIDTH, CELL_HEIGHT), 1)
    

    def movePlayer(self, vec: Vector2) -> None:
        self.__temp_direction = vec