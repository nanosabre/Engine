import pygame
import csv

resolution = [768, 768]
pygame.init()

#cd D:\Files\Code\Python\Engine

font = pygame.font.SysFont(None, 24)

def renderText(text:str, size:tuple, pos:int = 0, b:pygame.Surface = None, border:int = 5, typef = font, color = (0,0,0)):
    print("TEXT RENDER CALL")
    background = b
    width = size[0] - 2*border
    height = size[1] - 2*border
    holdPos = 0
    start = 0
    subsurfs = []
    j = 0
    for i in range(len(text)):
        if text[i] == '\n':
            if j >= len(subsurfs):
                subsurfs.append(typef.render(text[start:i], True, color))
            else:
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
        background.blit(subsurfs[i], (border, 24*0.9*i - pos + border))
    return background, pos


class UIElement:
    def __init__(self, name, layer, pos, size, att = None, data = None):
        self.name = name
        self.layer = layer
        self.rect = pygame.Rect(pos, size)
        self.att = att

        if "image" in att:
            self.surf = self.loadImg(data[0])
        else:
            self.surf = pygame.Surface(size, pygame.SRCALPHA, (0, 0, 0, 0))
        if "text" in att:
            with open("Assets" + "\\" + data[1], 'r') as textFile:
                self.text = textFile.read()
            self.scrollpos = 0
            self.background = pygame.Surface(self.rect.size, pygame.SRCALPHA, (0, 0, 0, 0)) #CREATES BACKGROUND SURFFACE AND LOADS IMAGE
            self.loadText()
        
    def resize(self, size):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, size[0], size[1])
    
    def loadImg(self, file):
        return pygame.transform.scale(pygame.image.load("Assets" + "\\" + str(file)), (self.rect.width, self.rect.height))

    def loadText(self, dpos = 0):
        self.background = pygame.Surface(self.rect.size, pygame.SRCALPHA, (0, 0, 0, 0))
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA, (0, 0, 0, 0))
        self.surf, self.scrollpos = renderText(self.text, self.rect.size, self.scrollpos + dpos, self.background)


UIList = []
focused = []

with open("Main Menu.csv", newline='') as menuCSV:
    reader = csv.DictReader(menuCSV)
    for row in reader:
        data = [row['data1'], row['data2'], row['data3']]
        UIList.append(UIElement(row['name'], int(row['layer']),(int(row['x']), int(row['y'])), (int(row['width']), int(row['height'])), row['attributes'], data))


screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

running = True
waiting = False
while running:
    while waiting:
        pygame.time.Clock().tick(40)
        waiting = True
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if len(focused) > 0 and "text" in focused[0].att:
                    focused[0].loadText(-event.y * 10)
                    waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    esc = False
                    for layer in reversed(range(20)):
                        if len(focused) > 0:
                            if focused[0].rect.collidepoint(mousePos):
                                break
                        for UIE in UIList:
                            if UIE.layer == layer:
                                if UIE.rect.collidepoint(mousePos):
                                    focused = [UIE]
                                    waiting = False
                                    esc = True
                                    break
                        if esc:
                            break
                if event.button == 3:
                    focused = []
                    waiting = False
            elif event.type == pygame.QUIT:
                running = False
                waiting = False
        

    waiting = True
    screen.fill((255, 255, 255))
    print("tick")

    #DRAW
    for layer in range(20):
        for UIE in UIList:
            if UIE.layer == layer and UIE not in focused:
                screen.blit(UIE.surf, UIE.rect)
    if len(focused) > 0:
        screen.blit(focused[0].surf, focused[0].rect)


    #RENDER FRAME
    pygame.display.flip()


pygame.quit()