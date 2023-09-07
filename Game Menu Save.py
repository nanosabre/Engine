import pygame
import csv

resolution = [768, 768]
pygame.init()

#SETS WINDOW TO BE RESIZABLE
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

#cd D:\Files\Code\Python\Engine

#INITIALIZES DEFAULT PYGAME FONT
font = pygame.font.SysFont(None, 24)

def renderText(text:str, size:tuple, pos:int = 0, base:pygame.Surface = None, border:int = 5, typef:pygame.font = font, color:tuple = (0,0,0)):
    """ GENERATES SURFACE WITH BACKGROUND IMAGE AND TEXT BASED ON SCROLLED POSITION. RETURNS OUTPUT SURFACE AND ADJUSTED SCROLL POSITION
    TEXT:   STRING TEXT TO BE RENDERED
    SIZE:   INT TUPLE BEING WIDTH AND HEIGHT
    POS:    INT SCROLLING POSITION OF TEXT. SHOULD BE POSITIVE
    BASE:   SURFACE BACKGROUND IMAGE BEHIND TEXT
    BORDER: INT SETS MARGINS BETWEEN TEXT AND ELEMENT BORDER
    TYPEF:  FONT OBJECT FOR TEXT
    COLOR:  INT TUPLE FOR FONT COLOR
    """
    #TERRIFYING HACK TO INSANE BUG
    base = base.copy()              
    #EXTRACTS AND ADJUSTS TEXT AREA TO ELEMENT MARGINS
    width = size[0] - 2*border
    height = size[1] - 2*border
    
    #STORES THE LAST KNOWN SPACE CHARACTER INDEX
    holdPos = 0
    #STORES BEGINNING OF NEW LINE INDEX
    start = 0
    #LIST STORING EACH LINE OF TEXT AS A SEPARATE SUBSURFACE
    subsurfs = []
    #ITERATES THROUGH SUBSURFS LIST
    j = 0
    #ITERATES THROUGH TEXT STRING FOR RENDERING
    for i in range(len(text)):
        
        #SMALL OPTIMIZATION TO STOP RENDERING AFTER REACHING BOTTOM OF MARGIN
        if j*24*0.9 > pos + height:
            break
        
        #SEARCH FOR NEWLINE CHARACTER
        if text[i] == '\n':
            #IF NO SUBSURFACE EXISTS FOR THIS INDEX YET
            if j >= len(subsurfs):
                subsurfs.append(typef.render(text[start:i], True, color))
            else:
                subsurfs[j] = typef.render(text[start:i], True, color)
            #SETS NEWLINE POSITION AFTER NEWLINE CHARACTER
            start = i + 1
            #SETS NEW WORD POSITION AFTER NEWLINE CHARACTER
            holdPos = i + 1
            #SETS FOR NEW SUBSURFACE
            j += 1
        
        #SEARCH FOR SPACE CHARACTER
        if text[i] == ' ':
            #IF NO SUBSURFACE EXISTS FOR THIS INDEX YET
            if j >= len(subsurfs):
                subsurfs.append(typef.render(text[start:i], True, color))
            else:
                subsurfs[j] = typef.render(text[start:i], True, color)
            #CHECK IF SUBSURFACE IS WIDER THAN TEXT MARGINS
            if subsurfs[j].get_width() > width:
                #GOES BACK TO BEGINNING OF PREVIOUS WORD TO GENERATE SUBSURFACE
                subsurfs[j] = typef.render(text[start:holdPos], True, color)
                #SETS NEWLINE POSITION AFTER SPACE CHARACTER
                start = holdPos + 1
                #SETS NEW WORD POSITION AFTER SPACE CHARACTER
                i = holdPos + 1
                #SETS FOR NEW SUBSURFACE
                j += 1
            else:
                #SETS NEW WORD POSITION AT SPACE CHARACTER
                holdPos = i
    
    #CHECKS IF SCROLL POSITION IS VALID
    #24 IS FONT SIZE, 0.9 IS THE LINE HEIGHT CONSTANT. MAY MAKE VARIABLE IN FUTURE
    if pos > len(subsurfs)*24*0.9 - height and len(subsurfs)*24*0.9 > height:
        #CLAMPS SCROLL POSITION TO PREVENT SCROLLING TOO LOW
        pos = len(subsurfs)*24*0.9 - height
    elif pos < 0:
        #CLAMPS SCROLL POSITION TO PREVENT NEGATIVE SCROLL POSITION
        pos = 0
    
    #DRAWS ALL SUBSURFACES ON TO BACKGROUND SURFACE
    for i in range(len(subsurfs)):
        base.blit(subsurfs[i], (border, 24*0.9*i - pos + border))
    
    #RETURNS GENERATED SURFACE AND ADJUSTED SCROLL POSITION
    return base, pos


class UIElement:
    """ USER INTERFACE ELEMENT CLASS
    NAME:   STRING ELEMENT NAME
    LAYER:  INT
    POS:    INT TUPLE POSITION (X,Y)
    SIZE:   INT TUPLE SIZE (WIDTH, HEIGHT)
    ATT:    STRING CONTAINING OBJECT ATTRIBUTES
    DATA:   STRING LIST FOR LINKING
    """
    def __init__(self, name:str, layer:int, pos:tuple, size:tuple, att:str = None, data = None):
        #BASIC DATA MEMBER DEFINITIONS
        self.name = name
        self.layer = layer
        self.rect = pygame.Rect(pos, size)
        self.att = att

        #SETS ELEMENT SURFACE DEPENDING ON IMAGE ATTRIBUTE
        if "image" in att:
            self.surf = self.loadImg(data[0])
        else:
            self.surf = pygame.Surface(size, pygame.SRCALPHA, (0, 0, 0, 0))
        
        #INITIAL TEXT SURFACE RENDERING
        if "text" in att:
            #STORES TEXT FROM FILE
            with open("Assets" + "\\" + data[1], 'r') as textFile:
                self.text = textFile.read()
            #SETS DEFAULT SCROLL POSITION
            self.scrollpos = 0
            #CREATES BACKGROUND SURFFACE AND LOADS IMAGE
            self.background = self.surf 
            #INITIAL TEXT RENDER
            self.loadText()
    
    #RESIZES ELEMENT
    def resize(self, size):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, size[0], size[1])
    
    #LOADS IMAGE FROM FILE NAME
    def loadImg(self, file):
        return pygame.transform.scale(pygame.image.load("Assets" + "\\" + str(file)), (self.rect.width, self.rect.height))

    #RENDERS SURFACE USING DEFAULT BACKGROUND AND ELEMENT TEXT
    def loadText(self, dpos = 0):
        self.surf, self.scrollpos = renderText(self.text, self.rect.size, self.scrollpos + dpos, self.background)

#USER INTERFACT ELEMENT OBJECT CONTAINER
UIList = []

#"LIST" OF ONE ELEMENT REPRESENTING THE ELEMENT FOCUSED BY USER
# ITS A LIST SO PYTHON STORES JUST THE POINTER FOR LESS MEM USAGE I THINK?
focused = []

#PULLS OBJECT INFORMATION OUT OF CSV
with open("Main Menu.csv", newline='') as menuCSV:
    reader = csv.DictReader(menuCSV)
    for row in reader:
        #STORES DATA INTO LIST
        data = [row['data1'], row['data2'], row['data3']]

        #POPULATES UI LIST WITH INSTANCES CREATED FROM CSV FILE INFO
        UIList.append(UIElement(row['name'], 
                                int(row['layer']),
                                (int(row['x']), int(row['y'])), 
                                (int(row['width']), int(row['height'])), 
                                row['attributes'], data))



#GAME EXIT CONDITION VARIABLE
running = True

#GAME EXIT CONDITION VARIABLE
waiting = False

#MAIN GAME LOOP
while running:
    #THIS LOOP PREVENTS RENDER CALLS AND OTHER LOGIC FROM HAPPENING UNLESS AN EVENT IS DETECTED
    while waiting:
        #LOCKS GAME TO 30 FPS
        pygame.time.Clock().tick(30)
        #TRACKS MOUSE X, Y ABSOLUTE AND RELATIVE POSITION. ONLY DO ONCE PER CYCLE
        mousePos = pygame.mouse.get_pos()
        mouseRel = pygame.mouse.get_rel()

        #PYGAME EVENT SYSTEM LOOP
        for event in pygame.event.get():
            #SCROLL WHEEN INPUT
            if event.type == pygame.MOUSEWHEEL:
                #CHECKS TO SEE OF FOCUSED ELEMENT HAS TEXT
                if len(focused) > 0 and "text" in focused[0].att:
                    #SCROLLS TEXT BY RERENDERING TEXT
                    focused[0].loadText(-event.y * 10)
                    #EXITS WAITING LOOP
                    waiting = False
            #MOUSE CLICK EVENT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #IF LEFT CLICK
                if event.button == 1:
                    esc = False
                    #ITERATES THROUGH LAYERS FROM TOP TO BOTTOM SO TOPMOST ELEMENTS ARE SELECTED FIRST
                    for layer in reversed(range(20)):
                        #FOCUSED OBJECT ALWAYS ON TOP, SO IF MOUSE IS INSIDE NOTHING SHOULD HAPPEN
                        if len(focused) > 0 and focused[0].rect.collidepoint(mousePos):
                            break
                        #ITERATES THROUGH OBJECTS AND FINDS ELEMENTS ON CORRECT LAYER 
                        for UIE in UIList:
                            if UIE.layer == layer and UIE.rect.collidepoint(mousePos):
                                #SET SELECTED OBJECT TO BE FOCUSED
                                focused = [UIE]
                                #EXIT WAITING LOOP
                                waiting = False
                                #EXIT LAYER LOOP
                                esc = True
                                break
                        #FOR BREAKING OUTER LOOP
                        if esc:
                            break
                #IF RIGHT CLICK
                if event.button == 3:
                    #UNFOCUSES ALL ELEMENTS
                    focused = []
                    #EXIT WAITING LOOP
                    waiting = False
            #CLOSE GAME EVENT
            elif event.type == pygame.QUIT:
                running = False
                waiting = False
    #RESETS WAITING LOOP
    waiting = True

    #SCREEN BACKGROUND COLOR
    screen.fill((255, 255, 255))

    #CHEAP DEBUG THING
    print("tick")

    #DRAW ELEMENTS IN ORDER OF LAYER
    for layer in range(20):
        for UIE in UIList:
            #EXCLUDE FOCUSED OBJECT TO PREVENT DOUBLE-DRAWING
            if UIE.layer == layer and UIE not in focused:
                screen.blit(UIE.surf, UIE.rect)
    #DRAW FOCUSED OBJECT ON TOP
    if len(focused) > 0:
        screen.blit(focused[0].surf, focused[0].rect)


    #RENDER FRAME ON SCREEN
    pygame.display.flip()


pygame.quit()