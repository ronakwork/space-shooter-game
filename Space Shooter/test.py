import pygame
from os.path import join

# create a display window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Tutorial')

# load button images
start_img = pygame.image.load(join('images', 'player.png')).convert_alpha()
exit_img = pygame.image.load(join('images', 'meteor.png')).convert_alpha()

# button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        display_screen.blit(self.image, self.rect)

# create button instances
start_button = Button(100, 200, start_img)
exit_button = Button(450, 200, exit_img)

# game loop
running = True
while running:

    display_screen.fill((202, 228))

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()