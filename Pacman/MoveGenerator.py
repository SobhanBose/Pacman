from pygame.math import Vector2
import random
import copy
from .configs import *

class MoveGenerator:
    all_moves_in_sequence = [Vector2(0, -1), Vector2(-1, 0), Vector2(0, 1), Vector2(1, 0)]
    
    def __init__(self, ghost_id) -> None:
        self.__ghost_id = ghost_id
    

    def getBestMove(self, current_ghost_pos: Vector2, ghost_direction: Vector2, target: Vector2, behaviour_state: str, walls: list) -> Vector2:
        possible_moves = self.getPossibleMoves(current_ghost_pos, ghost_direction, behaviour_state, walls)
        if target:
            move = self.getShortestMove(current_ghost_pos, target, possible_moves)
        else:
            move = self.getFrightenedMove(possible_moves)
        
        return move
    

    def getShortestMove(self, ghost_pos: Vector2, target: Vector2, possible_moves: list) -> Vector2:
        for move in possible_moves:
            distance = ((ghost_pos.x+move.x)-target.x)**2 + ((ghost_pos.y+move.y) - target.y)**2
            try:
                if distance < min_dist:
                    min_dist = distance
                    shortest_move = move
            except:
                min_dist = distance
                shortest_move = move
        
        return shortest_move


    def getPossibleMoves(self, ghost_pos: Vector2, ghost_direction: Vector2, behaviour_state: str, walls: list) -> list:
        possible_moves = copy.copy(MoveGenerator.all_moves_in_sequence)
        possible_moves.remove(Vector2(ghost_direction.x*-1, ghost_direction.y*-1))
        if (behaviour_state == "inside_ghost_house") or (behaviour_state == "eaten"):
            for move in possible_moves[:]:
                if Vector2(ghost_pos + move) in walls:
                    possible_moves.remove(move)
        else:
            for move in possible_moves[:]:
                if Vector2(ghost_pos + move) in walls or Vector2(ghost_pos + move) in GHOST_HOUSE_ENTRY_POINTS:
                    possible_moves.remove(move)

        return possible_moves
    

    def getFrightenedMove(self, possible_moves) -> Vector2:
        return random.choice(possible_moves)