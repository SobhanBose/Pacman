import pygame.display
from pygame.math import Vector2
import copy
from .configs import *

class Player:
    def __init__(self) -> None:
        self.__radius = PLAYER_RADIUS
        self.__speed = copy.copy(PLAYER_SPEED)
        self.__grid_pos = copy.copy(PLAYER_START_POS)
        self.__lives_left = copy.copy(PLAYER_LIVES_LEFT)
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
        self.__direction = Vector2(1, 0)
        self.__temp_direction = Vector2(1, 0)
        self.__is_able_to_move = True
        self.__score = 0

    
    def getPixPos(self) -> Vector2:
        return self.__pix_pos

    
    def getGridPos(self) -> Vector2:
        return self.__grid_pos
    

    def getScore(self) -> int:
        return self.__score
    

    def getLivesLeft(self) -> int:
        return self.__lives_left

    
    def getDirection(self) -> Vector2:
        return self.__direction
    

    def removeLife(self) -> None:
        self.__lives_left -= 1


    def canMove(self, walls: list) -> bool:
        if Vector2(self.__grid_pos+self.__direction) in walls:
            return False
        return True
    

    def isTimeToMove(self, walls: list) -> None:
        if int(self.__pix_pos.x) % CELL_WIDTH == 0:
            if self.__direction == Vector2(1, 0) or self.__direction == Vector2(-1, 0) or self.__direction == Vector2(0, 0):
                return True
        if int(self.__pix_pos.y) % CELL_HEIGHT == 0:
            if self.__direction == Vector2(0, 1) or self.__direction == Vector2(0, -1) or self.__direction == Vector2(0, 0):
                return True
        return False
    

    def isOnCoin(self, coins_dict: dict) -> bool:
        if (self.__grid_pos.x, self.__grid_pos.y) in coins_dict.keys() and not coins_dict[(self.__grid_pos.x, self.__grid_pos.y)].getHasBeenEaten():
            return True
        return False
    

    def eatCoin(self, grid_pos: Vector2, coins_dict: dict, enemies_dict: dict) -> None:
        if coins_dict[(grid_pos.x, grid_pos.y)].isSpecial():
            for enemy in enemies_dict.values():
                enemy.makeFrightened()
        coins_dict[(grid_pos.x, grid_pos.y)].eatCoin()


    def scorePlayer(self) -> None:
        self.__score += 1
    

    def resetPlayer(self) -> None:
        self.__grid_pos = copy.copy(PLAYER_START_POS)
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
        self.__direction = Vector2(0, 0)
        self.__temp_direction = Vector2(0, 0)


    def update(self, screen: pygame.display, walls: list, coins_dict: dict, enemies_dict: dict) -> None:
        if self.__is_able_to_move:
            self.__pix_pos += self.__direction * self.__speed
        if self.isTimeToMove(walls):
            if self.__temp_direction != None:
                self.__direction = self.__temp_direction
            self.__is_able_to_move = self.canMove(walls)
        
            if self.isOnCoin(coins_dict):
                self.eatCoin(self.__grid_pos, coins_dict, enemies_dict)
                self.scorePlayer()

        # self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER+CELL_WIDTH//2)//CELL_WIDTH-1
        # self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)//CELL_HEIGHT-1

        self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER)//CELL_WIDTH
        self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER)//CELL_HEIGHT


    def drawPlayer(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, PLAYER_COLOR, (self.__pix_pos.x, self.__pix_pos.y), self.__radius)

        # pygame.draw.rect(screen, RED, (self.__grid_pos[0]*CELL_WIDTH+SCREEN_SIZE_BUFFER, self.__grid_pos[1]*CELL_HEIGHT+SCREEN_SIZE_BUFFER, CELL_WIDTH, CELL_HEIGHT), 1)
    

    def movePlayer(self, vec: Vector2, walls: list) -> None:
        # if Vector2(self.__grid_pos + vec) not in walls:
        self.__temp_direction = vec