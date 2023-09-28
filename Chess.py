import pygame
import engine

path = "D:\Files\Code\Python\Engine"

mainMenu = engine.UIContainer([])
toggleMenu = engine.UIContainer([])

background = engine.UIBackground(pygame.Rect((0,0), (760, 760)), 0, "image winScale ","Menu Back.png")
textbox1 = engine.UITextBox(pygame.Rect((50, 50), (300, 300)), 2, "textFile image moveable ", "Back2.png", "Text2.txt")
textbox2 = engine.UITextBox(pygame.Rect((50, 500), (300, 300)), 2, "textFile image moveable ", "Back2.png", "Text2.txt")

activeMenu = None

def button1func():
    if textbox1.active:
        textbox1.active = False
    else:
        textbox1.active = True

def button2func():
    global activeMenu
    if activeMenu == toggleMenu:
        activeMenu = engine.activateMenu(mainMenu, activeMenu)
    else:
        activeMenu = engine.activateMenu(toggleMenu, activeMenu)

button1 = engine.UIButton(pygame.Rect((20, 20), (100, 50)), 1, "image text ", button1func, "Back2.png", "Button1")
button2 = engine.UIButton(pygame.Rect((20, 70), (100, 50)), 1, "image text ", button2func, "Back2.png", "Button2")

mainMenu.addUIE(background)
mainMenu.addUIE(textbox1)
mainMenu.addUIE(textbox2)
mainMenu.addUIE(button1)
mainMenu.addUIE(button2)

toggleMenu.addUIE(button2)
toggleMenu.addUIE(background)


activeMenu = engine.activateMenu(toggleMenu, activeMenu)

quit = False
waiting = False

while not quit:
    while waiting == True:
        quit, waiting = engine.inputStep(activeMenu)
    
    #print("step")
    engine.renderStep(activeMenu)
    waiting = True