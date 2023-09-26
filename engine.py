import pygame

pygame.font.init()
pygame.init()
print("start")

#Font declarations
defaultFont = pygame.font.SysFont(None, 24)

#Parameters
path = "D:\Files\Code\Python\Engine"
resolution = [768, 768]
maxLayers = 20
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

LHold = pygame.event.Event(pygame.USEREVENT, attr1="LHold", rel=(0, 0), pos=(0, 0))
MHold = pygame.event.Event(pygame.USEREVENT, attr1="MHold", rel=(0, 0), pos=(0, 0))
RHold = pygame.event.Event(pygame.USEREVENT, attr1="RHold", rel=(0, 0), pos=(0, 0))

userEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.MOUSEBUTTONUP, pygame.KEYUP, pygame.MOUSEWHEEL, pygame.USEREVENT]

output = {"waiting" : True}

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

class UIElement():
    def __init__(self, rect, layer, att):
        self.rect = rect
        self.defLayer = layer
        self.layer = layer
        self.att = att

        self.active = True

        if "inactive " in att:
            self.active = False

    def userInput(self, event):
        return False
    
class UIBackground(UIElement):
    def __init__(self, rect, layer, att:str, imgFile):
        UIElement.__init__(self, rect, layer, att)

        if "image" in att:
            self.surf = loadImage(imgFile, rect.size, True)
        else:
            try:
                self.surf = pygame.Surface(rect.size, pygame.SRCALPHA, imgFile)
            except:
                self.surf = pygame.Surface(rect.size, 0, (255, 0, 128))
        
    def resize(self, size):
        self.rect.size = size
        self.surf = pygame.transform.scale(self.surf, size)
class UITextBox(UIElement):
    def __init__(self, rect, layer, att:str, imgFile = None, txt = None):
        UIElement.__init__(self, rect, layer, att)
        self.topBorderRect = pygame.Rect(self.rect.topleft, (self.rect.width, 20))
        self.botBorderRect = pygame.Rect((self.rect.bottomleft[0], self.rect.bottomleft[1] - 20), (self.rect.width, 20))
        self.focused = False
        self.moving = False
        self.resizing = False

        if "image" in att:
            self.background = loadImage(imgFile, rect.size, True)
        else:
            try:
                self.background = pygame.Surface(rect.size, pygame.SRCALPHA, imgFile)
            except:
                self.background = pygame.Surface(rect.size, 0, (255, 0, 128))
        #INITIAL TEXT SURFACE RENDERING
        if "textFile " in att:
            #STORES TEXT FROM FILE
            with open("Assets" + "\\" + txt, 'r') as textFile:
                self.text = textFile.read()
            #SETS DEFAULT SCROLL POSITION
            self.scrollpos = 0
            #INITIAL TEXT RENDER
            self.loadText()

        else:
            self.text = txt
            textSurf = defaultFont.render(self.text, True, (0, 0, 0))
            self.surf.blit(textSurf, (5, 5))

    #RENDERS SURFACE USING DEFAULT BACKGROUND AND ELEMENT TEXT
    def loadText(self, dpos = 0):
        if not (self.scrollpos == 0 and dpos < 0):
            self.surf, self.scrollpos = renderText(self.text, self.rect.size, self.scrollpos + dpos, self.background)

    def resize(self, size, inc = False): ##TODO TODO
        if inc == True:
            size = (self.rect.size[0] + size[0], self.rect.size[1] + size[1])
        if size[0] < 10:
            size = (10, size[1])
        if size[1] < 10:
            size = (size[0], 10)
        self.rect.size = size

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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.focused = True
                    self.layer = maxLayers-1
                    print("focused")
                else:
                    print("release")
                    self.focused = False
                    self.layer = self.defLayer
            elif event.button == 3:
                self.focused = False
                self.layer = self.defLayer
        if not self.focused:
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.moving = False
                self.resizing = False
        elif event.type == pygame.MOUSEWHEEL:
            self.loadText(-event.y*20)
        elif event.type == pygame.USEREVENT:
            if event == LHold:
                if self.moving:
                    self.nudge(event.rel)
                if self.resizing:
                    self.resize((0, event.rel[1]), True)
                    self.loadText()
                if self.botBorderRect.collidepoint(event.pos):
                    self.resizing = True
                elif self.topBorderRect.collidepoint(event.pos):
                    self.moving = True
        else:
            return False
        return True

def inputStep(UIList):
    pygame.time.Clock().tick(30)
        
    #TRACKS MOUSE X, Y ABSOLUTE AND RELATIVE POSITION. ONLY DO ONCE PER CYCLE
    mousePos = pygame.mouse.get_pos()
    mouseRel = pygame.mouse.get_rel()

    LHPost = False
    MHPost = False
    RHPost = False

    update = False

    for event in pygame.event.get():

        if event.type in userEvents:
            for layer in reversed(range(maxLayers)):
                for UIE in UIList:
                    if UIE.layer == layer and UIE.active:
                        update += UIE.userInput(event)
        if event == LHold:
            LHPost = True
        elif event == MHold:
            MHPost = True
        elif event == RHold:
            RHPost = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #IF LEFT CLICK
            if event.button == 1:
                LHPost = True
                pygame.event.post(LHold)
                LHold.rel = mouseRel
                LHold.pos = mousePos
            #IF SCROLL CLICK
            elif event.button == 2:
                MHPost = True
                pygame.event.post(MHold)
                MHold.rel = mouseRel
                MHold.pos = mousePos
            #IF RIGHT CLICK
            elif event.button == 3:
                RHPost = True
                pygame.event.post(RHold)
                RHold.rel = mouseRel
                RHold.pos = mousePos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                LHPost = False
            elif event.button == 2:
                MHPost = False
            elif event.button == 3:
                RHPost = False
        elif event.type == pygame.VIDEORESIZE or event.type == pygame.VIDEOEXPOSE:
            for UIE in UIList:
                if "winScale" in UIE.att:
                    UIE.resize(screen.get_size())
                    return True, False
                    #MOUSE CLICK EVENT
        elif event.type == pygame.QUIT:
            return False, False
    if LHPost:
        pygame.event.post(LHold)
        LHold.rel = mouseRel
        LHold.pos = mousePos
    if MHPost:
        pygame.event.post(MHold)
        LHold.rel = mouseRel
        LHold.pos = mousePos
    if RHPost:
        pygame.event.post(RHold)
        RHold.rel = mouseRel
        RHold.pos = mousePos
    
    if update:
        return True, False

    return True, True

def renderStep(UIList):
    #SCREEN BACKGROUND COLOR
    screen.fill((0, 255, 255))

    for layer in range(maxLayers):
        for UIE in UIList:
            if UIE.layer == layer and UIE.active:
                screen.blit(UIE.surf, UIE.rect)
    #RENDER FRAME ON SCREEN
    pygame.display.flip()