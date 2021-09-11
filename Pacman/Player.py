import pygame.display
from pygame.math import Vector2
from .configs import *

class Player:
    def __init__(self) -> None:
        self.__radius = PLAYER_RADIUS
        self.__speed = PLAYER_SPEED
        self.__grid_pos = PLAYER_START_POS
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
        self.__direction = Vector2(1, 0)
        self.__temp_direction = None
        self.__is_able_to_move = True
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
    

    def isTimeToMove(self):
        if int(self.__pix_pos.x) % CELL_WIDTH == 0:
            if self.__direction == Vector2(1, 0) or self.__direction == Vector2(-1, 0) or self.__direction == Vector2(0, 0):
                return True
        if int(self.__pix_pos.y) % CELL_HEIGHT == 0:
            if self.__direction == Vector2(0, 1) or self.__direction == Vector2(0, -1) or self.__direction == Vector2(0, 0):
                return True
        return False
    

    def isOnCoin(self, coins: list) -> bool:
        if self.__grid_pos in coins:
            return True
        return False
    

    def eatCoin(self, grid_pos: Vector2, coins: list) -> None:
        coins.remove(grid_pos)


    def scorePlayer(self) -> None:
        self.__score += 1


    def update(self, screen: pygame.display, walls: list, coins: list) -> None:
        if self.__is_able_to_move:
            self.__pix_pos += self.__direction * self.__speed
        if self.isTimeToMove():
            if self.__temp_direction != None:
                self.__direction = self.__temp_direction
            self.__is_able_to_move = self.canMove(walls)
        
            if self.isOnCoin(coins):
                self.eatCoin(self.__grid_pos, coins)
                self.scorePlayer()

        # self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER+CELL_WIDTH//2)//CELL_WIDTH-1
        # self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)//CELL_HEIGHT-1

        self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER)//CELL_WIDTH
        self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER)//CELL_HEIGHT


    def drawPlayer(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, PLAYER_COLOR, (self.__pix_pos.x, self.__pix_pos.y), self.__radius)

        # pygame.draw.rect(screen, RED, (self.__grid_pos[0]*CELL_WIDTH+SCREEN_SIZE_BUFFER, self.__grid_pos[1]*CELL_HEIGHT+SCREEN_SIZE_BUFFER, CELL_WIDTH, CELL_HEIGHT), 1)
    

    def movePlayer(self, vec: Vector2) -> None:
        self.__temp_direction = vec