from shutil import move
import pygame
from world import World
from player import Player
WINDOW_SIZE = (1920,1080)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
surface = pygame.Surface((300,200))
worldgen = World(50)
player = Player(0,0)
 
done = False
true_scroll = [0,0]


print(worldgen.WorldIn01)

pygame.quit()
# -------- Main Program Loop -----------
while not done:
    screen.fill(BLACK)
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left = True
            if event.key == pygame.K_RIGHT:
                player.right = True
            if event.key == pygame.K_UP:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left = False
            if event.key == pygame.K_RIGHT:
                player.right= False
            if event.key == pygame.K_UP:
                player.jump = False
                
    true_scroll[0] += (player.rect.x-true_scroll[0]-152)/20 
    true_scroll[1] += (player.rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    surface.fill(BLACK)
    rects = []
    for room in worldgen.rooms:
        surface.blit(room.roomImg,(room.x-scroll[0],room.y-scroll[1]))
        for rect in room.rects:
            pygame.draw.rect(surface,RED,pygame.Rect(rect.x-scroll[0],rect.y-scroll[1],rect.width,rect.height))
            rects.append(rect)
    
    player.move(rects)
    player.drawPlayer(surface,scroll)

    screen.blit(pygame.transform.scale(surface,WINDOW_SIZE),(0,0))
    
    # --- Limit to 60 frames per second
    pygame.display.update()
    clock.tick(60)
    
# Close the window and quit.
pygame.quit()
