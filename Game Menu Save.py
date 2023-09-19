import pygame
import csv

#Parameters
resolution = [768, 768]
path = "D:\Files\Code\Python\Engine"

pygame.init()
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

#Font declarations
font = pygame.font.SysFont(None, 24)

#Function Delcarations
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
    if pos < 0:
        pos = 0     
    
    width = size[0] - 2*border
    height = size[1] - 2*border
    
    base = pygame.transform.scale(base.copy(), size)
    textPlate = pygame.Surface((width, height), pygame.SRCALPHA, (0, 0, 0, 0))

    lineHeight = typef.get_height()
    holdPos = 0
    start = 0
    subsurfs = []
    j = 0
 
    for i in range(len(text)):

        if j*lineHeight > pos + height:
            break
        
        if text[i] == '\n' or i == len(text) - 1:
            subsurfs.append(typef.render(text[start:i + (i == len(text) - 1)], True, color))
            start = i + 1
            holdPos = i + 1
            j += 1
        elif text[i] == ' ':
            lineSize = typef.size(text[start:i])
            if lineSize[0] > width:
                j += 1
                if (j)*lineHeight < pos and (j)*lineHeight + height < pos:
                    subsurfs.append(None)
                else:
                    subsurfs.append(typef.render(text[start:holdPos], True, color)) 
                start = holdPos + 1
                i = holdPos + 1   
            else:
                holdPos = i

    if pos > (len(subsurfs) + 1)*lineHeight - height and len(subsurfs)*lineHeight > height:
        pos = (len(subsurfs) + 1)*lineHeight - height
    
    #count = 0
    for i in range(len(subsurfs)):
        if subsurfs[i] is not None:
            textPlate.blit(subsurfs[i], (0, lineHeight*i - pos))
    #        count += 1
    #print(count)
    
    base.blit(textPlate, (border, border))
    return base, pos
def loadImage(file:str, size:tuple = None, alpha:bool = False):
    if alpha:
        surf = pygame.image.load(path + "\\Assets\\" + file).convert_alpha()
    else:
        surf = pygame.image.load(path + "\\Assets\\" + file)
    if size is not None:
        surf = pygame.transform.scale(surf, size) 
    return surf


#"LIST" OF ONE ELEMENT REPRESENTING THE ELEMENT FOCUSED BY USER
# ITS A LIST SO PYTHON STORES JUST THE POINTER FOR LESS MEM USAGE I THINK?
focused = []



#Class Declarations
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
        self.hidden = False
    
    def resize(self, size):
        self.rect.size = size
        self.surf = pygame.transform.scale(self.surf, size)
    
    def userInput(self, event):
        return True

class UIBackground(UIElement):
    def __init__(self, name:str, layer:int, pos:tuple, size:tuple, att:str, data):
        UIElement.__init__(self, name, layer, pos, size, att, data)

        if "image" in att:
            self.surf = loadImage(data[0], size, True)
        else:
            try:
                self.surf = pygame.Surface(size, pygame.SRCALPHA, data[0])
            except:
                self.surf = pygame.Surface(size, 0, (255, 0, 128))
        
        if "winScale" in att:
            def update(self, screensize):
                self.resize(screensize)

class UITextbox(UIElement):
    def __init__(self, name:str, layer:int, pos:tuple, size:tuple, att:str, data):
        UIElement.__init__(self, name, layer, pos, size, att, data)

        self.topBorderRect = pygame.Rect(self.rect.topleft, (self.rect.width, 20))
        self.botBorderRect = pygame.Rect((self.rect.bottomleft[0], self.rect.bottomleft[1] - 20), (self.rect.width, 20))
        self.focused = False
        self.moving = False
        self.resizing = False

        if "image " in att:
            self.background = loadImage(data[0], size, True)
        else:
            try:
                self.surf = pygame.Surface(size, pygame.SRCALPHA, data[0])
            except:
                self.surf = pygame.Surface(size, 0, (255, 0, 128))
        
        #INITIAL TEXT SURFACE RENDERING
        if "textFile " in att:
            #STORES TEXT FROM FILE
            with open("Assets" + "\\" + data[1], 'r') as textFile:
                self.text = textFile.read()
            #SETS DEFAULT SCROLL POSITION
            self.scrollpos = 0
            #INITIAL TEXT RENDER
            self.loadText()

        else:
            self.text = data[1]
            textSurf = font.render(self.text, True, (0, 0, 0))
            self.surf.blit(textSurf, (5, 5))

    #RENDERS SURFACE USING DEFAULT BACKGROUND AND ELEMENT TEXT
    def loadText(self, dpos = 0):
        if not (self.scrollpos == 0 and dpos < 0):
            self.surf, self.scrollpos = renderText(self.text, self.rect.size, self.scrollpos + dpos, self.background)

    def resize(self, size, inc = False):
        if inc == True:
            size = (self.rect.size[0] + size[0], self.rect.size[1] + size[1])
        if size[0] < 10:
            size = (10, size[1])
        if size[1] < 10:
            size = (size[0], 10)
        self.rect.size = size
        self.topBorderRect.width = size[0]
        self.botBorderRect.width = size[0]
        self.botBorderRect.y = self.rect.bottomleft[1] - 20
        self.surf = pygame.transform.scale(self.surf, size)
        #self.background = pygame.transform.scale(self.background, size)      
    
    def nudge(self, relPos):
        self.rect.x += relPos[0]
        self.rect.y += relPos[1]
        self.topBorderRect.x += relPos[0]
        self.topBorderRect.y += relPos[1]
        self.botBorderRect.x += relPos[0]
        self.botBorderRect.y += relPos[1]
        if self.rect.x < 0:
            self.rect.x = 0
            self.topBorderRect.x = 0
            self.botBorderRect.x = 0
        elif self.rect.x > screen.get_size()[0]:
            self.rect.x = screen.get_size()[0] - 5
            self.topBorderRect.x =screen.get_size()[0] - 5
            self.botBorderRect.x =screen.get_size()[0] - 5
        if self.rect.y < 0:
            self.rect.y = 0
            self.topBorderRect.y = 0
            self.botBorderRect.x =screen.get_size()[0] - 5
        elif self.rect.y > screen.get_size()[1]:
            self.rect.y = screen.get_size()[1] - 5
            self.topBorderRect.y = screen.get_size()[1] - 5
            self.botBorderRect.y = screen.get_size()[1] - 5

    def userInput(self, event):
        if self.moving:
            self.nudge(LHold.rel)
        if self.resizing:
            self.resize((0, LHold.rel[1]), True)
            self.loadText()
        if event.type == pygame.MOUSEWHEEL:
            self.loadText(-event.y*20)
        elif event.type == pygame.USEREVENT:
            if event == LHold:
                if self.botBorderRect.collidepoint(LHold.pos):
                    self.resizing = True
                elif self.topBorderRect.collidepoint(LHold.pos):
                    self.moving = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.focused = True
            elif event.button == 3:
                self.focused = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.moving = False
                self.resizing = False
        else:
            return True
        return False

class UIButton(UIElement):
    def __init__(self, name:str, layer:int, pos:tuple, size:tuple, att:str, data):
        UIElement.__init__(self, name, layer, pos, size, att, data)

        focused = False

        if "image " in att:
            self.surf = loadImage(data[0], size, True)
        else:
            try:
                self.surf = pygame.Surface(size, pygame.SRCALPHA, data[0])
            except:
                self.surf = pygame.Surface(size, 0, (255, 0, 128))

        if "text " in att:
            self.text = data[1]
            textSurf = font.render(self.text, True, (0, 0, 0))
            self.surf.blit(textSurf, (5, 5))

    def userInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.focused = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.focused = False
                if self.rect.collidepoint(event.pos):
                    print("click!")
        else:
            return True
        return False



#Class UILabel:

#USER INTERFACT ELEMENT OBJECT CONTAINER
UIList = []

#PULLS OBJECT INFORMATION OUT OF CSV
with open("Main Menu.csv", newline='') as menuCSV:
    reader = csv.DictReader(menuCSV)
    for row in reader:
        #STORES DATA INTO LIST
        data = [row['data0'], row['data1'], row['data2'], row['data3']]

        #POPULATES UI LIST WITH INSTANCES CREATED FROM CSV FILE INFO
        if "background" in row['name']:
            UIList.append(UIBackground(
                row['name'],
                int(row['layer']),
                (int(row['x']), int(row['y'])),
                (int(row['height']), int(row['height'])),
                 row['attributes'],
                 data
            ))
        elif "textbox" in row['name']:
            UIList.append(UITextbox(
                row['name'],
                int(row['layer']),
                (int(row['x']), int(row['y'])),
                (int(row['height']), int(row['height'])),
                 row['attributes'],
                 data
            ))
        elif "button" in row['name']:
            UIList.append(UIButton(
                row['name'],
                int(row['layer']),
                (int(row['x']), int(row['y'])),
                (int(row['height']), int(row['height'])),
                 row['attributes'],
                 data
            ))

#GAME EXIT CONDITION VARIABLE
running = True

#GAME EXIT CONDITION VARIABLE
waiting = False
mouseLHold = False
mouseMHold = False
mouseRHold = False

LHold = pygame.event.Event(pygame.USEREVENT, attr1="LHold", rel=(0, 0), pos=(0, 0))
MHold = pygame.event.Event(pygame.USEREVENT, attr1="MHold", rel=(0, 0), pos=(0, 0))
RHold = pygame.event.Event(pygame.USEREVENT, attr1="RHold", rel=(0, 0), pos=(0, 0))

userEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.MOUSEBUTTONUP, pygame.KEYUP, pygame.MOUSEWHEEL, pygame.USEREVENT]

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

            if event.type in userEvents:
                skip = False
                for UIE in focused:
                    waiting = UIE.userInput(event)
                    if UIE.rect.collidepoint(mousePos):
                        skip = True
                if not skip and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for layer in reversed(range(20)):
                        esc = False
                        for UIE in reversed(UIList):
                            if UIE.layer == layer and UIE.rect.collidepoint(mousePos) and UIE not in focused:
                                waiting = UIE.userInput(event)
                                if hasattr(UIE, 'focused'):
                                    if UIE.focused:
                                        focused = [UIE]
                                    else:
                                        focused = []
                                esc = True
                                break
                        if esc:
                            break


            #MOUSE CLICK EVENT
            if event.type == pygame.MOUSEBUTTONDOWN:
                #IF LEFT CLICK
                if event.button == 1:
                    mouseLHold = True
                #IF SCROLL CLICK
                elif event.button == 2:
                    mouseMHold = True
                #IF RIGHT CLICK
                elif event.button == 3:
                    #UNFOCUSES ALL ELEMENTS
                    focused = []
                    #EXIT WAITING LOOP
                    waiting = False
                    mouseRHold = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouseLHold = False
                elif event.button == 2:
                    mouseMHold = False
                elif event.button == 3:
                    mouseRHold = False
            elif event.type == pygame.VIDEORESIZE or event.type == pygame.VIDEOEXPOSE:
                for UIE in UIList:
                    if "winScale" in UIE.att:
                        UIE.resize(screen.get_size())
                waiting = False
            #CLOSE GAME EVENT
            elif event.type == pygame.QUIT:
                running = False
                waiting = False

        if mouseLHold:
            pygame.event.post(LHold)
            LHold.rel = mouseRel
            LHold.pos = mousePos
        if mouseMHold:
            pygame.event.post(MHold)
            LHold.rel = mouseRel
            LHold.pos = mousePos
        if mouseRHold:
            pygame.event.post(RHold)
            RHold.rel = mouseRel
            RHold.pos = mousePos
    
    #RESETS WAITING LOOP
    waiting = True

    #SCREEN BACKGROUND COLOR
    screen.fill((255, 255, 255))

    #CHEAP DEBUG THING
    #print("tick")

    #DRAW ELEMENTS IN ORDER OF LAYER
    for layer in range(20):
        for UIE in UIList:
            #EXCLUDE FOCUSED OBJECT TO PREVENT DOUBLE-DRAWING
            if UIE.layer == layer and not UIE.hidden and UIE not in focused:
                screen.blit(UIE.surf, UIE.rect)
    #DRAW FOCUSED OBJECT ON TOP
    for UIE in focused:
        screen.blit(UIE.surf, UIE.rect)


    #RENDER FRAME ON SCREEN
    pygame.display.flip()


pygame.quit()