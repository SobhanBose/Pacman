from pygame.math import Vector2
import pygame.display
import random
import copy
from .TargetSystem import TargetSystem
from .MoveGenerator import MoveGenerator
from .configs import *


class Ghost:
    ghost_id = {'1': 'blinky', '2': 'pinky', '3': 'inky', '4': 'clyde'}
    ghost_image = {'1': 'blinky', '2': 'pinky', '3': 'inky', '4': 'clyde'}
    ghost_initial_direction = {'1': Vector2(1, 0), '2': Vector2(-1, 0), '3': Vector2(1, 0), '4': Vector2(-1, 0)}
    ghost_color = {'1': ENEMY_COLOR_RED, '2': ENEMY_COLOR_PINK, '3': ENEMY_COLOR_BLUE, '4': ENEMY_COLOR_YELLOW}
    behaviour_states = ["inside_ghost_house", "chase", "scatter", "frightened", "eaten"]

    def __init__(self, pos: Vector2, ghost_id: str) -> None:
        self.__ghost_id = ghost_id
        self.__target_system = TargetSystem(self.__ghost_id)
        self.__move_generator = MoveGenerator(self.__ghost_id)
        self.__start_pos = copy.copy(pos)
        self.__grid_pos = copy.copy(pos)
        self.__pix_pos = Vector2(self.__grid_pos.x*CELL_WIDTH+SCREEN_SIZE_BUFFER+CELL_WIDTH//2, self.__grid_pos.y*CELL_HEIGHT+SCREEN_SIZE_BUFFER+CELL_HEIGHT//2)
        self.__direction = Ghost.ghost_initial_direction[self.__ghost_id]
        self.__behaviour_state = "inside_ghost_house"
        self.__ghost_image = Ghost.ghost_image[self.__ghost_id]
        self.__ghost_color = Ghost.ghost_color[self.__ghost_id]
        self.__radius = ENEMY_RADIUS
        self.__speed = ENEMY_SPEED
    

    def getGhostID(self) -> int:
        return self.__ghost_id
    

    def getGridPos(self) -> Vector2:
        return self.__grid_pos
    

    def getBehaviourState(self) -> str:
        return self.__behaviour_state
    

    def isTimeToMove(self) -> bool:
        if int(self.__pix_pos.x) % CELL_WIDTH == 0:
            if self.__direction == Vector2(1, 0) or self.__direction == Vector2(-1, 0) or self.__direction == Vector2(0, 0):
                return True
        if int(self.__pix_pos.y) % CELL_HEIGHT == 0:
            if self.__direction == Vector2(0, 1) or self.__direction == Vector2(0, -1) or self.__direction == Vector2(0, 0):
                return True
        return False


    def updateGhostBehaviour(self, behaviour_state: str) -> None:
        self.__behaviour_state = behaviour_state
        print(f"{Ghost.ghost_id[self.__ghost_id]}: {self.__behaviour_state}")
    

    def makeFrightened(self) -> None:
        self.updateGhostBehaviour("frightened")
    

    def makeScatter(self) -> None:
        self.updateGhostBehaviour("scatter")
    

    def makeChase(self) -> None:
        self.updateGhostBehaviour("chase")
    

    def makeEaten(self) -> None:
        self.__ghost_color = WHITE
        self.updateGhostBehaviour("eaten")


    def updateGhost(self, player_pos: Vector2, player_direction: Vector2, walls: list) -> None:
        self.__target = self.__target_system.getTarget(self.__grid_pos, player_pos, player_direction, self.__behaviour_state)
        if self.__grid_pos != self.__target:
            self.__pix_pos += self.__direction * self.__speed
            if self.isTimeToMove():
                self.__direction = self.__move_generator.getBestMove(self.__grid_pos, self.__direction, self.__target, self.__behaviour_state, walls)

        self.__grid_pos[0] = (self.__pix_pos[0]-SCREEN_SIZE_BUFFER)//CELL_WIDTH
        self.__grid_pos[1] = (self.__pix_pos[1]-SCREEN_SIZE_BUFFER)//CELL_HEIGHT

        if self.__behaviour_state == "inside_ghost_house" and self.__target == self.__grid_pos:
            self.updateGhostBehaviour("scatter")
        elif self.__behaviour_state == "eaten" and self.__target == self.__grid_pos:
            self.__ghost_color = Ghost.ghost_color[self.__ghost_id]
            self.updateGhostBehaviour("inside_ghost_house")


    def drawGhost(self, screen: pygame.display) -> None:
        pygame.draw.circle(screen, self.__ghost_color, (self.__pix_pos.x, self.__pix_pos.y), self.__radius)
