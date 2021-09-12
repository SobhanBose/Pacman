import pygame
import sys
import pickle
from .Player import Player
from .Enemies import Enemy
from .Coins import Coin
from .configs import *

pygame.init()

class App:
    def __init__(self) -> None:
        self.__player = Player()
        self.__enemies = []
        self.__walls = []
        self.__coins_dict = {}
        self.__width = SCREEN_WIDTH
        self.__height = SCREEN_HEIGHT
        self.__mazeWidth = MAZE_WIDTH
        self.__mazeHeight = MAZE_HEIGHT
        self.__fps = FPS
        self.__running = True
        self.__highscore = self.getHighScore()
        pygame.display.set_caption("PacMan")
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__clock = pygame.time.Clock()
        self.__gamestate = "intro_screen"       # intro_screen   playing    gameover
        self.__cellWidth = CELL_WIDTH
        self.__cellHeight = CELL_HEIGHT

        self.load()
    
    
    def getWidth(self) -> int:
        return self.__width
    

    def getHeight(self) -> int:
        return self.__height
    

    def getGameState(self) -> str:
        return self.__gamestate
    

    def setGameState(self) -> str:
        return self.__gamestate
    

    def getHighScore(self) -> int:
        with open(r'Pacman\highscore.txt', 'rb') as highcore_file:
            return pickle.load(highcore_file)
    

    def setHighScore(self, score: int) -> None:
         with open(r'Pacman\highscore.txt', 'wb') as highcore_file:
            pickle.dump(score, highcore_file)
            self.__highscore = score
    

    def makeEnemy(self, pos: Vector2, behaviour: str) -> None:
        return Enemy(pos, behaviour)


    def load(self) -> None:
        self.__background = pygame.image.load(r'Pacman\res\images\maze.png')
        self.__background = pygame.transform.scale(self.__background, (self.__mazeWidth, self.__mazeHeight))

        with open(r'Pacman\map.txt') as wall_file:
            for y_index, line in enumerate(wall_file):
                for x_index, character in enumerate(line):
                    if character == '1':
                        self.__walls.append(Vector2(x_index, y_index))
                    elif character == 'C':
                        self.__coins_dict[(x_index, y_index)] = Coin(Vector2(x_index, y_index))
                    elif character in ['2', '3', '4', '5']:
                        self.__enemies.append(self.makeEnemy(Vector2(x_index, y_index), character))
                    elif character == 'B':
                        pygame.draw.rect(self.__background, BLACK, (x_index*self.__cellWidth, y_index*self.__cellHeight, self.__cellWidth, self.__cellHeight))

        # for wall in self.__walls:
        #     pygame.draw.rect(self.__background, GREEN, (wall.x*CELL_WIDTH, wall.y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

        # for coin in self.__coins:
        #     pygame.draw.rect(self.__background, COIN_COLOR, (coin.x*self.__cellWidth, coin.y*self.__cellHeight, self.__cellWidth, self.__cellHeight))
    

    def drawBackground(self) -> None:
        self.__screen.blit(self.__background, (SCREEN_SIZE_BUFFER, SCREEN_SIZE_BUFFER))


    def drawText(self, msg: str, screen: pygame.display, align: str, size: int, color: tuple, font_face: str) -> None:
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
    

    def drawGrid(self) -> None:
        for cols in range(self.__mazeWidth//self.__cellWidth):
            pygame.draw.line(self.__screen, GRAY, (cols*self.__cellWidth+SCREEN_SIZE_BUFFER, SCREEN_SIZE_BUFFER), (cols*self.__cellWidth+SCREEN_SIZE_BUFFER, self.__mazeHeight+SCREEN_SIZE_BUFFER))
        for rows in range(self.__mazeHeight//self.__cellHeight):
            pygame.draw.line(self.__screen, GRAY, (SCREEN_SIZE_BUFFER, rows*self.__cellHeight+SCREEN_SIZE_BUFFER), (self.__mazeWidth+SCREEN_SIZE_BUFFER, rows*self.__cellHeight+SCREEN_SIZE_BUFFER))


    def drawCoins(self) -> None:
        for coin in self.__coins_dict.values():
            if not coin.getHasBeenEaten():
                coin.drawCoin(self.__screen)


    def run(self) -> None:
        while self.__running:
            if self.__gamestate == "intro_screen":
                self.introEvents()
                self.introUpdate()
                self.introDraw()
            elif self.__gamestate == "playing":
                self.playingEvents()
                self.playingUpdate()
                self.playingDraw()
            elif self.__gamestate == "gameover":
                self.gameoverEvents()
                self.gameoverDraw()
            self.__clock.tick(self.__fps)
        pygame.quit()
        sys.exit(0)


    def introEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__gamestate = "playing"
    

    def introUpdate(self) -> None:
        pass


    def introDraw(self) -> None:
        self.__screen.fill(BLACK)
        self.drawText("PACMAN", self.__screen, f'center_horizontal {self.__height//2-150}' ,FONT_SIZE_TITLE, FONT_COLOR_ORANGE, FONT_FACE_INTRO)
        self.drawText("PRESS SPACEBAR TO PLAY", self.__screen, 'center_horizontal center_vertical' ,FONT_SIZE_INTRO, FONT_COLOR_ORANGE, FONT_FACE_INTRO)
        self.drawText("SINGLE PLAYER", self.__screen, f'center_horizontal {self.__height//2+50}' ,FONT_SIZE_INTRO, FONT_COLOR_BLUE, FONT_FACE_INTRO)
        self.drawText(f"HIGH SCORE: {self.__highscore}", self.__screen, f'center_horizontal bottom' ,FONT_SIZE_INTRO, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        pygame.display.update()
    

    def checkPlayerEnemyCollision(self) -> bool:
        for enemy in self.__enemies:
            if enemy.getGridPos() == self.__player.getGridPos():
                return True
        return False
    

    def resetPositions(self) -> bool:
        self.__player.resetPlayer()
        for enemy in self.__enemies:
            enemy.resetEnemy()
    

    def playingEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__player.movePlayer(pygame.math.Vector2(-1, 0), self.__walls)
                elif event.key == pygame.K_RIGHT:
                    self.__player.movePlayer(pygame.math.Vector2(1, 0), self.__walls)
                elif event.key == pygame.K_UP:
                    self.__player.movePlayer(pygame.math.Vector2(0, -1), self.__walls)
                elif event.key == pygame.K_DOWN:
                    self.__player.movePlayer(pygame.math.Vector2(0, 1), self.__walls)

    
    def playingUpdate(self) -> None:
        self.__player.update(self.__screen, self.__walls, self.__coins_dict)
        for enemy in self.__enemies:
            enemy.updateEnemy(self.__walls, self.__player.getGridPos())
        
        if self.checkPlayerEnemyCollision():
            if self.__player.getLivesLeft() == 0:
                self.__gamestate = "gameover"
                self.gameoverUpdate()
            else:
                self.__player.removeLife()
                self.resetPositions()


    def playingDraw(self) -> None:
        self.__screen.fill(BLACK)
        self.drawBackground()
        # self.drawGrid()
        self.drawCoins()
        self.drawText(f"HIGH SCORE: {self.__highscore}", self.__screen, f'left top' , 16, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        self.drawText(f"CURRENT SCORE: {self.__player.getScore()}", self.__screen, f'right top' , 16, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        self.drawText(f"LIVES LEFT: {self.__player.getLivesLeft()}", self.__screen, f'left bottom' , 16, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        self.__player.drawPlayer(self.__screen)
        for enemy in self.__enemies:
            enemy.drawEnemy(self.__screen)
        pygame.display.update()
    

    def resetGame(self) -> None:
        self.__player = Player()
        for enemy in self.__enemies:
            enemy.resetEnemy()
        for coin in self.__coins_dict.values():
            coin.resetCoin()


    def gameoverEvents(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.resetGame()
                    self.__gamestate = "playing"
                elif event.key == pygame.K_ESCAPE:
                    self.__running = False
    

    def gameoverUpdate(self) -> None:
        if self.__player.getScore() > self.__highscore:
            self.setHighScore(self.__player.getScore())


    def gameoverDraw(self) -> None:
        self.__screen.fill(BLACK)
        self.drawText("PACMAN", self.__screen, f'center_horizontal {self.__height//2-150}' ,FONT_SIZE_TITLE, FONT_COLOR_TITLE, FONT_FACE_INTRO)
        self.drawText("GAME - OVER", self.__screen, 'center_horizontal center_vertical' ,FONT_SIZE_INTRO, FONT_COLOR_RED, FONT_FACE_INTRO)
        self.drawText("PRESS SPACEBAR TO PLAY AGAIN", self.__screen, f'center_horizontal {self.__height//2+50}' ,FONT_SIZE_INTRO, FONT_COLOR_BLUE, FONT_FACE_INTRO)
        self.drawText("PRESS ESCAPE TO QUIT", self.__screen, f'center_horizontal {self.__height//2+85}' ,FONT_SIZE_INTRO, FONT_COLOR_ORANGE, FONT_FACE_INTRO)
        self.drawText(f"HIGH SCORE: {self.__highscore}", self.__screen, f'center_horizontal bottom' ,FONT_SIZE_INTRO, FONT_COLOR_WHITE, FONT_FACE_INTRO)
        pygame.display.update()