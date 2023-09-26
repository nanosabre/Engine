import pygame

pygame.font.init()

#Font declarations
defaultFont = pygame.font.SysFont(None, 24)
path = "D:\Files\Code\Python\Engine"
maxLayers = 20

LHold = pygame.event.Event(pygame.USEREVENT, attr1="LHold", rel=(0, 0), pos=(0, 0))
MHold = pygame.event.Event(pygame.USEREVENT, attr1="MHold", rel=(0, 0), pos=(0, 0))
RHold = pygame.event.Event(pygame.USEREVENT, attr1="RHold", rel=(0, 0), pos=(0, 0))

userEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.MOUSEBUTTONUP, pygame.KEYUP, pygame.MOUSEWHEEL, pygame.USEREVENT]

#Function Delcarations
def renderText(text:str, size:tuple, pos:int = 0, base:pygame.Surface = None, border:int = 5, typef:pygame.font = defaultFont, color:tuple = (0,0,0)):
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
def button1(target, UIList):
    for UIE in UIList:
        if target in UIE.name:
            if UIE.hidden:
                print("revealed")
                UIE.hidden = False
            else:
                print("hidden")
                UIE.hidden = True



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
        self.defLayer = layer
        self.rect = pygame.Rect(pos, size)
        self.att = att
        self.hidden = False
    
        if "hidden " in att:
            self.hidden = True

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
                self.surf = pygame.Surface(size, 0, (128, 0, 64))
        
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
            textSurf = defaultFont.render(self.text, True, (0, 0, 0))
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
        if self.rect.y < 0:
            self.rect.y = 0
            self.topBorderRect.y = 0
            self.botBorderRect.x = 0

    def userInput(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.loadText(-event.y*20)
        elif event.type == pygame.USEREVENT:
            if event == LHold:
                if self.moving:
                    self.nudge(LHold.rel)
                if self.resizing:
                    self.resize((0, LHold.rel[1]), True)
                    self.loadText()
                if self.botBorderRect.collidepoint(LHold.pos):
                    self.resizing = True
                elif self.topBorderRect.collidepoint(LHold.pos):
                    self.moving = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.focused = True
                    self.layer = maxLayers-1
                else:
                    print("release")
                    self.focused = False
                    self.layer = self.defLayer
            elif event.button == 3:
                self.focused = False
                self.layer = self.defLayer
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

        self.focused = False
        self.target = data[3]

        if "image " in att:
            self.surf = loadImage(data[0], size, True)
        else:
            try:
                self.surf = pygame.Surface(size, pygame.SRCALPHA, data[0])
            except:
                self.surf = pygame.Surface(size, 0, (255, 0, 128))

        if "text " in att:
            self.text = data[1]
            textSurf = defaultFont.render(self.text, True, (0, 0, 0))
            self.surf.blit(textSurf, (5, 5))

    def userInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.focused = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    button1(self.target)
                    self.focused = False
        else:
            return True
        return False