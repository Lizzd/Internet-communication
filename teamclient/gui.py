import pygame


class Gui(object):
    """
    class to render the gui
    """

    def __init__(self, hight, width):
        self.screen = pygame.display.set_mode((hight, width))
        pygame.font.init()
        self.font = pygame.font.SysFont("Times", 50)

    def render_screen(self, players_rectangles_and_colors, ball, scores, mode='BASIC'):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), ball)
        if mode == 'BASIC':
            self.screen.blit(self.font.render(str(scores[0]), -1, (255, 255, 255)), (200, 25))
            self.screen.blit(self.font.render(str(scores[1]), -1, (255, 255, 255)), (600, 25))
        else:
            distance = 100
            self.screen.blit(self.font.render(str(scores[0]), -1, (255, 255, 255)),
                             (distance, 400))  # left
            self.screen.blit(self.font.render(str(scores[1]), -1, (255, 255, 255)),
                             (800 - distance, 400))  # right
            self.screen.blit(self.font.render(str(scores[2]), -1, (255, 255, 255)),
                             (400, distance))  # top
            self.screen.blit(self.font.render(str(scores[3]), -1, (255, 255, 255)),
                             (400, 800 - distance))  # bottom

        self._draw_players(players_rectangles_and_colors)
        pygame.display.flip()

    def _draw_players(self, players_rectangles_and_colors):
        for playerRects, Colour in players_rectangles_and_colors:
            for pRect in playerRects:
                pygame.draw.rect(self.screen, Colour, playerRects[pRect])
