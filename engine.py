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
winsize = screen.get_rect().size

LHold = pygame.event.Event(pygame.USEREVENT, attr1="LHold", rel=(0, 0), pos=(0, 0))
MHold = pygame.event.Event(pygame.USEREVENT, attr1="MHold", rel=(0, 0), pos=(0, 0))
RHold = pygame.event.Event(pygame.USEREVENT, attr1="RHold", rel=(0, 0), pos=(0, 0))

userEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.MOUSEBUTTONUP, pygame.KEYUP, pygame.MOUSEWHEEL, pygame.USEREVENT]

#output = {"waiting" : True}

def activateMenu(UIC, active):
    if active is not None:
        active.deactivate()
    UIC.activate()
    return UIC

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
        self.parent = None
        self.surf = None

        self.active = False
    def nudge(self, relpos):
        self.rect.topleft = (self.rect.x + relpos[0], self.rect.y + relpos[1])

    def resize(self, size, inc = False): ##TODO TODO
        if inc:
            size = (self.rect.size[0] + size[0], self.rect.size[1] + size[1])
        self.rect.size = size

        if self.surf is not None:
            self.surf = pygame.transform.scale(self.surf, size)

    def load(self):
        self.active = True

    def unload(self):
        self.active = False

    def userInput(self, event):
        return False

class UIBackground(UIElement):
    def __init__(self, rect, layer, att:str, imgFile):
        UIElement.__init__(self, rect, layer, att)
        self.imgFile = imgFile
        
    def load(self):
        self.active = True
        if "image" in self.att:
            self.surf = loadImage(self.imgFile, self.rect.size, True)
        else:
            try:
                self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA, self.imgFile)
            except:
                self.surf = pygame.Surface(self.rect.size, 0, (255, 0, 128))
class UITextBox(UIElement):
    def __init__(self, rect, layer, att:str, imgFile = None, txt = None):
        UIElement.__init__(self, rect, layer, att)
        self.focused = False
        self.imgFile = imgFile
        self.textRead = txt
        self.scrollpos = 0
    
    def resize(self, size, inc = False):
        if inc:
            size = (self.rect.size[0] + size[0], self.rect.size[1] + size[1])
        self.rect.size = size

        if self.surf is not None:
            self.background = pygame.transform.scale(self.background, size)

        self.loadText(self.scrollpos)        

    def load(self):
        self.active = True
        if "image" in self.att:
            self.background = loadImage(self.imgFile, self.rect.size, True)
        else:
            try:
                self.background = pygame.Surface(self.rect.size, pygame.SRCALPHA, self.imgFile)
            except:
                self.background = pygame.Surface(self.rect.size, 0, (255, 0, 128))
            #INITIAL TEXT SURFACE RENDERING
        if "textFile " in self.att:
            #STORES TEXT FROM FILE
            with open("Assets" + "\\" + self.textRead, 'r') as textFile:
                self.text = textFile.read()
            #SETS DEFAULT SCROLL POSITION
            self.scrollpos = 0
            #INITIAL TEXT RENDER
            self.loadText()
        else:
            textSurf = defaultFont.render(self.text, True, (0, 0, 0))
            self.surf.blit(textSurf, (5, 5))

    def addText(self, text):
        self.text = text
        self.loadText()

    def unload(self):
        self.active = False
        self.background = None
        self.surf = None

    #RENDERS SURFACE USING DEFAULT BACKGROUND AND ELEMENT TEXT
    def loadText(self, dpos = 0):
        if not (self.scrollpos == 0 and dpos < 0):
            self.surf, self.scrollpos = renderText(self.text, self.rect.size, self.scrollpos + dpos, self.background)

    def userInput(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.loadText(-event.y*20)
        else:
            return False
        return True
class UIButton(UIElement):
    def __init__(self, rect, layer, att:str, func, imgFile = None, txt = None):
        UIElement.__init__(self, rect, layer, att)
        self.text = txt
        self.pressed = False
        self.func = func
        self.focused = False
        self.imgFile = imgFile

    def load(self):
        self.active = True
        if "image" in self.att:
            self.surf = loadImage(self.imgFile, self.rect.size, True)
        else:
            try:
                self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                self.surf.fill(self.imgFile)
            except:
                self.surf = pygame.Surface(self.rect.size, 0, (255, 0, 128))
        
        if "text" in self.att:
            self.surf.blit(defaultFont.render(self.text, True, (0, 0, 0)), (5, 5))

    def unload(self):
        self.active = False
        self.surf = None
    
    def userInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if not self.focused:
                    self.focused = True
                    return False
                else:
                    self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.rect.collidepoint(event.pos) and self.focused:
                self.pressed = False
                self.func()
        else:
            return False
        return True
class UIPanelMover(UIElement):
    def __init__(self, rect, layer, att):
        UIElement.__init__(self, rect, layer, att)
        self.focused = False
        self.moving = False

    def userInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.focused = True
                else:
                    self.focused = False
        if not self.focused:
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.moving = False
                self.focused = False
        elif event.type == pygame.USEREVENT:
            if event == LHold:
                if self.moving:
                    self.parent.nudge(event.rel)
                elif self.rect.collidepoint(event.pos):
                    self.moving = True
                else:
                    return False
        else:
            return False
        return True
class UIPanelResizer(UIElement):
    def __init__(self, rect, layer, att):
        UIElement.__init__(self, rect, layer, att)
        self.focused = False
        self.resizing = False

    def userInput(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.focused = True
                else:
                    self.focused = False
        if not self.focused:
            return False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.resizing = False
                self.focused = False
        elif event.type == pygame.USEREVENT:
            if event == LHold:
                if self.resizing:
                    self.parent.resize(event.rel, True)
                elif self.rect.collidepoint(event.pos):
                    self.resizing = True
                else:
                    return False
        else:
            return False
        return True
class UIPanelCloser(UIButton):
    def __init__(self, rect, layer, imgFile = None):
        UIButton.__init__(self, rect, layer, "imag right ", self.func, imgFile)

    def func(self):
        #self.focused = False
        self.parent.deactivate()

class Panel(UIElement):
    def __init__(self, rect, layer, att):
        UIElement.__init__(self, rect, layer, att)
        self.UIList = []
        self.bounds = screen.get_rect()
        self.focused = False

    def nudge(self, relpos):
        if self.rect.left + relpos[0] < self.bounds.left:
            relpos = (self.bounds.left - self.rect.left, relpos[1])
        elif self.rect.right + relpos[0] > self.bounds.right:
            relpos = (self.bounds.right - self.rect.right, relpos[1]) 
        self.rect.x += relpos[0]   
                
        if self.rect.top + relpos[1] < self.bounds.top:
            relpos = (relpos[0], self.bounds.top - self.rect.top)
        elif self.rect.bottom + relpos[1] > self.bounds.bottom:
            relpos = (relpos[0],self.bounds.bottom -  self.rect.bottom)
        self.rect.y += relpos[1]

        for UIE in self.UIList:
            UIE.nudge(relpos)
        
    def resize(self, size, inc = False):
        if inc:
            relsize = size
            size = (self.rect.size[0] + size[0], self.rect.size[1] + size[1])
        else:
            relsize = (size[0] - self.rect.size[0], size[1] - self.rect.size[1])
        if size[0] < 20:
            size = (20, size[1])
        if size[1] < 20:
            size = (size[0], 20)

        for UIE in self.UIList:
            if "right " in UIE.att:
                UIE.rect.right *= size[0]/self.rect.size[0]
            else:
                UIE.rect.left *= size[0]/self.rect.size[0]
            if "bot" in UIE.att:
                UIE.rect.bot *= size[1]/self.rect.size[1]
            else:
                UIE.rect.top *= size[1]/self.rect.size[1]
            if "scale " in UIE.att:
                UIE.resize(relsize, True)

        self.rect.size = size



    def addUIE(self, UIE):
        if UIE not in self.UIList:
            UIE.parent = self
            UIE.nudge(self.rect.topleft)
            self.UIList.append(UIE)
    
    def remUIE(self, UIE):
        if UIE in self.UIList:
            self.UIList.remove(UIE)

    def activate(self):
        self.active = True
        for UIE in self.UIList:
            if hasattr(UIE, "focused"):
                UIE.focused = False
            UIE.load()
    
    def deactivate(self):
        self.active = False
        for UIE in self.UIList:
            UIE.unload()

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
        update = 0
        if event.type in userEvents:
            hasFocus = False
            for layer in reversed(range(maxLayers)):
                for UIE in reversed(self.UIList):
                    if UIE.layer == layer and UIE.active:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hasattr(UIE, "focused"):
                            if not hasFocus:
                                update += UIE.userInput(event)
                                hasFocus = UIE.focused
                            else:
                                UIE.focused = False
                        else:
                            update += UIE.userInput(event)
        return update



def inputStep(UICs):
    pygame.time.Clock().tick(30)
    global winsize
        
    #TRACKS MOUSE X, Y ABSOLUTE AND RELATIVE POSITION. ONLY DO ONCE PER CYCLE
    mousePos = pygame.mouse.get_pos()
    mouseRel = pygame.mouse.get_rel()

    LHPost = False
    MHPost = False
    RHPost = False

    update = False

    for event in pygame.event.get():
        for UIC in UICs:
            if not UIC.active:
                continue
            update += UIC.userInput(event)
        
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
        elif event.type == pygame.WINDOWRESIZED or event.type == pygame.WINDOWRESTORED:
            for UIC in UICs:
                if UIC.active and "winscale " in UIC.att:
                    relsize = (screen.get_rect().width - winsize[0], screen.get_rect().height - winsize[1])
                    if "xwinscale " in UIC.att and "ywinscale " in UIC.att:
                        UIC.resize(relsize, True)
                    elif "xwinscale " in UIC.att:
                        UIC.resize((relsize[0], UIC.rect.height), True)
                    elif "ywinscale " in UIC.att:
                        UIC.resize((UIC.rect.width, relsize[1]), True)
                    UIC.bounds = screen.get_rect()
                    winsize = screen.get_rect().size
            return False, False
        elif event.type == pygame.QUIT:
            return True, False
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
        return False, False

    return False, True

def renderStep(UICs):
    #SCREEN BACKGROUND COLOR
    screen.fill((0, 255, 255))
    for panelLayer in range(maxLayers):
        for UIC in UICs:
            if UIC.layer == panelLayer:
                if not UIC.active:
                    continue
                for layer in range(maxLayers):
                    for UIE in UIC.UIList:
                        if UIE.layer == layer and UIE.active and UIE.surf is not None:
                            screen.blit(UIE.surf, UIE.rect)
    pygame.display.flip()

#def flip():
