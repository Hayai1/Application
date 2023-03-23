import pygame
class SpriteSheet:
    def __init__(self,spriteSheetFile):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(spriteSheetFile).convert()#load the spritesheet
        except pygame.error as e:#if the spritesheet can't be loaded
            print(f"Unable to load spritesheet image: {spriteSheetFile}")#print an error message
            raise SystemExit(e)#exit the program
    def image_at(self, rectangle, colorkey = None):#load a specific image from a specific rectangle
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)#create a rectangle from the rectangle
        image = pygame.Surface(rect.size).convert()#create a surface from the rectangle
        image.blit(self.sheet, (0, 0), rect)#blit the spritesheet onto the surface
        if colorkey is not None:#if there is a colorkey
            if colorkey == -1:#if the colorkey is -1
                colorkey = image.get_at((0,0))#set the colorkey to the color of the pixel at (0,0)
            image.set_colorkey(colorkey, pygame.RLEACCEL)#set the colorkey
        return image#return the image

    def images_at(self, rects, colorkey = None):#load a bunch of images from a bunch of rectangles
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]#return a list of images

    def load_strip(self, rect, image_count, colorkey = None):#load a whole strip of images
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])#create a list of rectangles
                for x in range(image_count)]#for each image in the strip
        return self.images_at(tups, colorkey)#return a list of images