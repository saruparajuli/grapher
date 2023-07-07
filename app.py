# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = 'white'
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 5
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def collisions(self, platform):
        player_rect = pygame.Rect(self.x+self.velocity_x, self.y+self.velocity_y, self.width, self.height)
        if player_rect.colliderect(platform):
            self.velocity_x = 0
            self.velocity_y = 0
        if self.y > screen.get_height():
            self.gravity = 0
        else:
            self.gravity = 5
        self.velocity_y += self.gravity
            

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.velocity_x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = 5
        else:
            self.velocity_x = 0

        if keys[pygame.K_UP]:
            self.velocity_y = -5
        else:
            self.velocity_y = 0
        self.x += self.velocity_x
        self.y += self.velocity_y
    
p1 = Player(0, 720-50, 50, 50)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    plat1 = pygame.draw.rect(screen, 'blue', (100,720-50,500,10))
    # RENDER YOUR GAME HERE
    p1.collisions(plat1)
    p1.move(pygame.key.get_pressed())
    p1.draw(screen)

    
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()