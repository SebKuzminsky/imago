"""Display images with debug info"""

from PIL import ImageDraw
import pygame

from geometry import l2ad, line, intersection

class UserQuitError(Exception):
    pass

class Screen:
    # TODO isn't this a duplicate of something?
    def __init__(self, res, image=None):
        if image:
            res = image.size
        pygame.init()
        pygame.display.set_mode(res)
        pygame.display.set_caption("Imago manual mode")
        self._screen = pygame.display.get_surface()
        if image:
            self.draw = ImageDraw.Draw(image)

    def display_picture(self, img):
        pg_img = pygame.image.frombuffer(img.tobytes(), img.size, img.mode)
        self._screen.blit(pg_img, (0, 0))
        pygame.display.flip()

    def wait_for_click_or_keypress(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise UserQuitError 
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    return 

