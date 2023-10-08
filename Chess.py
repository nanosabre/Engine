import pygame
import engine

path = "D:\Files\Code\Python\Engine"

mainMenu = engine.Panel(pygame.Rect((0, 0), (760, 760)), 0, "xwinscale ywinscale ")
toggleMenu = engine.Panel(pygame.Rect((0, 0), (760, 760)), 1, None)
textBox = engine.Panel(pygame.Rect((50, 50), (760, 760)), 0, None)

background = engine.UIBackground(pygame.Rect((0,0), (760, 760)), 0, "image xscale yscale","Menu Back.png")
textBlock1 = engine.UITextBox(pygame.Rect((50, 50), (300, 300)), 2, "textFile image ", "Back2.png", "Text2.txt")
mover = engine.UIPanelMover(pygame.Rect((0, 0), (760, 20)), 0, "scale ")

def button1func():
    if textBlock1.active:
        textBlock1.active = False
    else:
        textBlock1.active = True

def button2func():
    print("click")
    if mainMenu.active:
        mainMenu.deactivate()
    else:
        mainMenu.activate()

button1 = engine.UIButton(pygame.Rect((20, 20), (100, 50)), 1, "image text ", button1func, "Back2.png", "Button1")
button2 = engine.UIButton(pygame.Rect((20, 70), (100, 50)), 1, "image text ", button2func, "Back2.png", "Button2")
closer = engine.UIPanelCloser(pygame.Rect((740, 0), (20, 20)), 1, (255, 50, 50))

mainMenu.addUIE(background)
mainMenu.addUIE(textBlock1)
mainMenu.addUIE(button1)
mainMenu.addUIE(mover)
mainMenu.addUIE(closer)

toggleMenu.addUIE(button2)
toggleMenu.activate()

quit = False
waiting = False

panels = [toggleMenu, mainMenu]

while not quit:
    while waiting == True:
        quit, waiting = engine.inputStep(panels)

    #print("step")
    engine.renderStep(panels)
    waiting = True

    #engine.flip()