import pygame
import csv

resolution = [768, 768]
pygame.init()


font = pygame.font.SysFont(None, 24)

def renderText(text, size, pos:int = 0, typef = font, color = (0,0,0), background = None):
    width = size[0]
    height = size[1]
    holdPos = 0
    start = 0
    surf = pygame.Surface((width, height), pygame.SRCALPHA, (255, 0, 0, 255))
    subsurfs = []
    j = 0
    for i in range(len(text)):
        if text[i] == '\n':
            subsurfs[j] = typef.render(text[start:i], True, color)
            start = i + 1
            holdPos = i + 1
            j += 1
        if text[i] == ' ':
            if j >= len(subsurfs):
                subsurfs.append(typef.render(text[start:i], True, color))
            else:
                subsurfs[j] = typef.render(text[start:i], True, color)
            if subsurfs[j].get_width() > width:
                subsurfs[j] = typef.render(text[start:holdPos], True, color)
                start = holdPos + 1
                i = holdPos + 1
                j += 1
            else:
                holdPos = i

    if pos > len(subsurfs)*24*0.9 - height and len(subsurfs)*24*0.9 > height:
        pos = len(subsurfs)*24*0.9 - height
    elif pos < 0:
        pos = 0
    for i in range(len(subsurfs)):
        surf.blit(subsurfs[i], (0, 24*0.9*i - pos))
    return surf


class UIElement:
    def __init__(self, name, pos, size, att = None, file = None):
        self.name = name
        self.rect = pygame.Rect(pos, size)
        self.att = att

        if "image" in att:
            self.loadImg(file)
        if "text" in att:
            with open("Assets" + "\\" + file, 'r') as textFile:
                self.text = textFile.read()
            self.loadText(self.text)

    def resize(self, size):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, size[0], size[1])
    
    def loadImg(self, file):
        self.surf = pygame.transform.scale(pygame.image.load("Assets" + "\\" + str(file)), (self.rect.width, self.rect.height))
        print(self.rect.width, self.rect.height)

    def loadText(self, pos):
        self.surf = renderText(self.text, self.rect.size, 200)


UIList = []

with open("Main Menu.csv", newline='') as menuCSV:
    reader = csv.DictReader(menuCSV)
    for row in reader:
        UIList.append(UIElement(row['name'], (int(row['x']), int(row['y'])), (int(row['width']), int(row['height'])), row['attributes'], row['file']))


screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

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