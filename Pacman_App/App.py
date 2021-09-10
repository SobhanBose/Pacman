import pygame
import sys
from .Pacman import Pacman
from .configs import *

pygame.init()

vec = pygame.math.Vector2()

class App:
    def __init__(self) -> None:
        self.__width = SCREEN_WIDTH
        self.__height = SCREEN_HEIGHT
        self.__mazeWidth = MAZE_WIDTH
        self.__mazeHeight = MAZE_HEIGHT
        self.__fps = FPS
        self.__running = True
        self.__currentscore = 0
        self.__highscore = 0
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__clock = pygame.time.Clock()
        self.__gamestate = "intro_screen"
        self.__cellWidth = self.__mazeWidth//28
        self.__cellHeight = self.__mazeHeight//30
        self.load()
    
    
    def getWidth(self) -> int:
        return self.__width
    

    def getHeight(self) -> int:
        return self.__height
    

    def getGameState(self) -> str:
        return self.__gamestate
    

    def setGameState(self) -> str:
        return self.__gamestate


    def load(self) -> None:
        self.__background = pygame.image.load(r'Pacman_App\res\images\maze.png')
        self.__background = pygame.transform.scale(self.__background, (self.__mazeWidth, self.__mazeHeight))


    def draw_text(self, msg: str, screen: pygame.display, align: str, size: int, color: tuple, font_face: str) -> None:
        """
            align ([string]): [space separated strings - center_horizontal, right, left center_vertucal, top, bottom or absolute positions in format 'horizontal_position <space> vertical_position']
        """  

        font = pygame.font.SysFont(font_face, size)
        text = font.render(msg, False, color)
        align = align.split(" ")
        pos = [0, 0]
        if align[0].isnumeric():
            pos[0] = eval(align[0])
        elif align[0] == 'center_horizontal':
            pos[0] = self.__width//2-text.get_width()//2
        elif align[0] == 'left':
            pos[0] = 10
        elif align[0] == 'right':
            pos[0] = self.__width-text.get_width()-10
        if align[1].isnumeric():
            pos[1] = eval(align[1])
        if align[1] == 'center_vertical':
            pos[1] = self.__height//2-text.get_height()//2
        elif align[1] == 'top':
            pos[1] = 10
        elif align[1] == 'bottom':
            pos[1] = self.__height-text.get_height()-10
        screen.blit(text, pos)
    

    def draw_grid(self) -> None:
        for cols in range(self.__mazeWidth//self.__cellWidth):
            pygame.draw.line(self.__screen, GRAY, (cols*self.__cellWidth+SCREEN_SIZE_BUFFER, SCREEN_SIZE_BUFFER), (cols*self.__cellWidth+SCREEN_SIZE_BUFFER, self.__mazeHeight+SCREEN_SIZE_BUFFER))
        for rows in range(self.__mazeHeight//self.__cellHeight):
            pygame.draw.line(self.__screen, GRAY, (SCREEN_SIZE_BUFFER, rows*self.__cellHeight+SCREEN_SIZE_BUFFER), (self.__mazeWidth+SCREEN_SIZE_BUFFER, rows*self.__cellHeight+SCREEN_SIZE_BUFFER))


    def run(self) -> None:
        while self.__running:
            if self.__gamestate == "intro_screen":
                self.intro_events()
                self.intro_update()
                self.intro_draw()
            elif self.__gamestate == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            self.__clock.tick(self.__fps)
        pygame.quit()
        sys.exit(0)


    def intro_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__gamestate = "playing"
    

    def intro_update(self) -> None:
        pass


    def intro_draw(self) -> None:
        self.__screen.fill(BLACK)
        self.draw_text("PACMAN", self.__screen, f'center_horizontal {self.__height//2-150}' ,FONT_SIZE_TITLE, FONT_COLOR_ORANGE, FONT_FACE_INTRO)
        self.draw_text("PRESS SPACEBAR TO PLAY", self.__screen, 'center_horizontal center_vertical' ,FONT_SIZE_INTRO, FONT_COLOR_ORANGE, FONT_FACE_INTRO)
        self.draw_text("SINGLE PLAYER", self.__screen, f'center_horizontal {self.__height//2+50}' ,FONT_SIZE_INTRO, FONT_COLOR_BLUE, FONT_FACE_INTRO)
        self.draw_text("HIGH SCORE: ", self.__screen, f'center_horizontal bottom' ,FONT_SIZE_INTRO, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        pygame.display.update()
    

    def playing_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
    

    def playing_update(self) -> None:
        pass


    def playing_draw(self) -> None:
        self.__screen.fill(BLACK)
        self.__screen.blit(self.__background, (SCREEN_SIZE_BUFFER, SCREEN_SIZE_BUFFER))
        self.draw_grid()
        self.draw_text(f"HIGH SCORE: {self.__highscore}", self.__screen, f'left top' , 16, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        self.draw_text(f"CURRENT SCORE: {self.__currentscore}", self.__screen, f'right top' , 16, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        pygame.display.update()