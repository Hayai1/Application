import pygame

screen = pygame.display.set_mode((800, 600))
rect = pygame.Rect(0, 0, 100, 100)
while True:
    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
