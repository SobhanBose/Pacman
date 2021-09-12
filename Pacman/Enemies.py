from pygame.math import Vector2
import pygame.display
import random
import copy
from .configs import *

class Enemy:
    color_dict = {'2': ENEMY_COLOR_BLUE, '3': ENEMY_COLOR_PINK, '4': ENEMY_COLOR_YELLOW, '5': ENEMY_COLOR_RED}
    personality_dict = {'2': 'speedy', '3': 'slow', '4': 'random', '5': 'scared'}
    def __init__(self, pos: Vector2, type: str) -> None:
        self.__radius = ENEMY_RADIUS
        self.__type = copy.copy(type)
        self.__color = self.updateEnemyColor(self.__type)
        self.__personality = self.updateEnemyPersonality(self.__type)
        self.__start_pos = copy.copy(pos)
        self.__grid_pos = copy.copy(pos)
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
        self.__direction = Vector2(0, 0)
        self.__speed = self.setSpeed()
        self.__target = None

        # self.__type might be written as id later
    

    def getGridPos(self) -> Vector2:
        return self.__grid_pos
    

    def resetEnemy(self) -> None:
        self.__grid_pos = copy.copy(self.__start_pos)
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
        self.__direction = Vector2(0, 0)


    def setTarget(self, player_grid_pos: Vector2) -> Vector2:
        if self.__personality == "speedy" or self.__personality == "slow":
            return player_grid_pos
        elif self.__personality == "scared":
            if player_grid_pos.x > NUM_COLUMNS//2:
                if player_grid_pos.y > NUM_ROWS//2:
                    return Vector2(1, 1)
                else:
                    return Vector2(1, NUM_ROWS-2)
            else:
                if player_grid_pos.y > NUM_ROWS//2:
                    return Vector2(NUM_COLUMNS-2, 1)
                else:
                    return Vector2(NUM_COLUMNS-2, NUM_ROWS-2)
        else:
            pass
    

    def setSpeed(self) -> int:
        if self.__personality in ["speedy", "scared"]:
            return 2
        return 1
    

    def updateEnemyColor(self, type: str) -> tuple:
        return Enemy.color_dict[type]
    

    def updateEnemyPersonality(self, type: str) -> str:
        return Enemy.personality_dict[type]


    def isTimeToMove(self):
        if int(self.__pix_pos.x) % CELL_WIDTH == 0:
            if self.__direction == Vector2(1, 0) or self.__direction == Vector2(-1, 0) or self.__direction == Vector2(0, 0):
                return True
        if int(self.__pix_pos.y) % CELL_HEIGHT == 0:
            if self.__direction == Vector2(0, 1) or self.__direction == Vector2(0, -1) or self.__direction == Vector2(0, 0):
                return True
        return False
    

    def move(self, walls: list, player_grid_pos: Vector2) -> None:
        if self.__personality == "random":
            self.__direction = self.getRandomDirection(walls)
        elif self.__personality == "speedy":
            self.__direction = self.getNextPathDirection(walls, player_grid_pos, self.__target)
        elif self.__personality == "slow":
            self.__direction = self.getNextPathDirection(walls, player_grid_pos, self.__target)
        elif self.__personality == "scared":
            self.__direction = self.getNextPathDirection(walls, player_grid_pos, self.__target)
    

    def getRandomDirection(self, walls: list) -> Vector2:
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            if Vector2(self.__grid_pos.x+x_dir, self.__grid_pos.y+y_dir) not in walls:
                break
        return Vector2(x_dir, y_dir)
    

    def getNextPathDirection(self, walls: int, player_grid_pos: Vector2, target: Vector2) -> Vector2:
        next_cell = self.findNextCellInPath(walls, player_grid_pos, target)
        x_dir = next_cell[0] - self.__grid_pos[0]
        y_dir = next_cell[1] - self.__grid_pos[1]
        return Vector2(x_dir, y_dir)
    

    def findNextCellInPath(self, walls: list, player_grid_pos: Vector2, target: Vector2) -> Vector2:
        path = self.BFS([int(self.__grid_pos.x), int(self.__grid_pos.y)], [int(target.x), int(target.y)], walls)
        return path[1]
    

    def BFS(self, current_pos: list, target_pos: list, walls: list) -> list:
        grid = [[0 for cols in range(28)] for rows in range(30)]
        for cell in walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [current_pos]
        path = []
        visited = []
        while queue:
            current_cell = queue.pop(0)
            visited.append(current_cell)
            if current_cell == target_pos:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current_cell[0] >= 0 and neighbour[0] + current_cell[0] < len(grid[0]):
                        if neighbour[1] + current_cell[1] >= 0 and neighbour[1] + current_cell[1] < len(grid): 
                            next_cell = [neighbour[0] + current_cell[0], neighbour[1] + current_cell[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"current_cell": current_cell, "next_cell": next_cell})
        shortest = [target_pos]
        while target_pos != current_pos:
            for step in path:
                if step["next_cell"] == target_pos:
                    target_pos = step["current_cell"]
                    shortest.insert(0, step["current_cell"])
        return shortest


    def updateEnemy(self, walls: list, player_grid_pos: Vector2) -> None:
        self.__target = self.setTarget(player_grid_pos)
        if self.__target != self.__grid_pos:
            self.__pix_pos += self.__direction * self.__speed
            if self.isTimeToMove():
                self.move(walls, player_grid_pos)
        self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER)//CELL_WIDTH
        self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER)//CELL_HEIGHT


    def drawEnemy(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, self.__color, (self.__pix_pos.x, self.__pix_pos.y), self.__radius)