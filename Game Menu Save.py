import pygame
import csv

resolution = [768, 768]
pygame.init()

class UIElement:
    def __init__(self, name, pos, size, att = None, file = None):
        self.name = name
        self.rect = pygame.Rect(pos, size)
        self.att = att

        if "image" in att:
            self.loadImg(file)


    def resize(self, size):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, size[0], size[1])
    
    def loadImg(self, file):
        self.surf = pygame.transform.scale(pygame.image.load("Assets" + "\\" + str(file)), (self.rect.width, self.rect.height))
        print(self.rect.width, self.rect.height)


UIList = []

with open('Main Menu.csv', newline='') as menuCSV:
    reader = csv.DictReader(menuCSV)
    for row in reader:
        UIList.append(UIElement(row['name'], (int(row['x']), int(row['y'])), (int(row['width']), int(row['height'])), row['attributes'], row['file']))


screen = pygame.display.set_mode(resolution)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))


    #DRAW
    for UIE in UIList:
        screen.blit(UIE.surf, UIE.rect)


    #RENDER FRAME
    pygame.display.flip()


pygame.quit()