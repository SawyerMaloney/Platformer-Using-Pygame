import pygame


class HighscoreWindow:
    def __init__(self):
        pygame.init()
        self.SCREEN = (300, 100)
        self.highscore_screen = pygame.display.set_mode(self.SCREEN)
        pygame.display.set_caption("Highscore!")
