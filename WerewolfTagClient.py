import pygame
import GameState
from MainMenu import MainMenu
from Game import Game

'''
Created on Nov 10, 2014

@author: Jon, Angel
'''

class WerewolfTagClient:
    
    mainMenu = MainMenu()
    game = None
    window = None
    display = pygame.display
    event = pygame.event
    mixer = pygame.mixer #for sound
    frameRate = 60
    screenWidth = 640
    screenHeight = 480
    fullScreen = False
    currentState = GameState.GAME

    
    def __init__(self):
        pygame.init()
        self.window=self.display.set_mode([self.screenWidth, self.screenHeight], pygame.FULLSCREEN if self.fullScreen else pygame.RESIZABLE)
        pygame.mouse.set_visible(False)
        self.mixer.init()
        self.game = Game(self)
        self.game.init()
        
    def run(self):
        isDone = False
        while isDone == False: 
            self.window.fill((0, 0, 0))
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    isDone = True
                    
            if self.currentState == GameState.MENU:
                self.mainMenu.run()
            elif self.currentState == GameState.GAME:
                self.game.update(key)
                
                    
            elif self.currentState == GameState.EXIT:
                isDone = True
        
            if self.currentState == GameState.MENU:
                self.mainMenu.draw()
            elif self.currentState == GameState.GAME:
                self.game.draw()
            
            self.display.flip()
            
    def setState(self, state):
        #end current state
        if self.currentState == GameState.MENU:
            self.mainMenu.end()
        elif self.currentState == GameState.GAME:
            self.game.end()
            
        #initialize next state
        if state == GameState.MENU:
            state = self.mainMenu.init()
        elif state == GameState.GAME:
            state = self.game.init()
        
        #update current state
        self.currentState = state
    
    def end(self):   
        self.mixer.quit()
        self.display.quit()
        pygame.quit()
    
    
    
    