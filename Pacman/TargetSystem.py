from pygame.math import Vector2
import random
import copy
from .configs import *

class TargetSystem:
    scatter_targets = {'1': Vector2(NUM_COLUMNS-2, 1), '2': Vector2(1, 1), '3': Vector2(NUM_COLUMNS-2, NUM_ROWS-2), '4':Vector2(1, NUM_ROWS-2)}
    ghost_target = {'1': Vector2(0, 0), '2': Vector2(0, 0), '3': Vector2(0, 0), '4': Vector2(0, 0)}

    def __init__(self, ghost_id: str) -> None:
        self.__ghost_id = ghost_id
    

    def getTarget(self, current_ghost_pos: Vector2, player_pos: Vector2, player_direction: Vector2, mode: str) -> None:
        if mode == "scatter":
            target = self.getScatterTarget()
        elif mode == "chase":
            if self.__ghost_id == '1':
                target = self.getChaseTargetBlinky(player_pos)
            elif self.__ghost_id == '2':
                target = self.getChaseTargetPinky(player_pos, player_direction)
            elif self.__ghost_id == '3':
                target = self.getChaseTargetInky(current_ghost_pos, player_pos, player_direction)
            elif self.__ghost_id == '4':
                target = self.getChaseTargetClyde(current_ghost_pos, player_pos, player_direction)
        elif mode == "frightened":
            target = None
        elif mode == "eaten":
            target = self.getEatenTarget()
        elif mode == "inside_ghost_house":
            target = self.getInsideGhostHouseTarget()
        
        TargetSystem.ghost_target[self.__ghost_id] = target
        return target


    def getInsideGhostHouseTarget(self) -> Vector2:
        return Vector2(13, 11)


    def getScatterTarget(self) -> Vector2:
        return TargetSystem.scatter_targets[self.__ghost_id]


    def getEatenTarget(self) -> Vector2:
        return Vector2(13, 13)


    def getChaseTargetBlinky(self,player_pos: Vector2) -> Vector2:
        return player_pos


    def getChaseTargetPinky(self, player_pos: Vector2, player_direction: Vector2) -> Vector2:
        if player_direction != Vector2(0, -1):
            return Vector2(player_pos + player_direction*4)
        else:
            return Vector2(player_pos.x - 4, player_pos.y + player_direction.y*4)


    def getChaseTargetInky(self, current_ghost_pos: Vector2, player_pos: Vector2, player_direction: Vector2) -> Vector2:
        if player_direction != Vector2(0, -1):
            temp_target = Vector2(player_pos + player_direction*2)
        else:
            temp_target = Vector2(player_pos.x - 2, player_pos.y + player_direction.y*2)
        blinky_target = TargetSystem.ghost_target['1']
        target_x = 2*temp_target.x - blinky_target.x
        target_y = 2*temp_target.y - blinky_target.y

        return Vector2(target_x, target_y)


    def getChaseTargetClyde(self, current_ghost_pos: Vector2, player_pos: Vector2, player_direction: Vector2) -> Vector2:
        if abs(current_ghost_pos.x - player_pos.x) <= 8 and abs(current_ghost_pos.y-player_pos.y) <= 8:
            return self.getScatterTarget()
        else:
            return player_pos
