import pygame
import engine

path = "D:\Files\Code\Python\Engine"
UIList = []

running = True
waiting = True



background = engine.UIBackground(pygame.Rect((0,0), (760, 760)), 0, "image winScale ","Menu Back.png")
textbox1 = engine.UITextBox(pygame.Rect((50, 50), (300, 300)), 2, "textFile image moveable ", "Back2.png", "Text2.txt")
textbox2 = engine.UITextBox(pygame.Rect((50, 500), (300, 300)), 2, "textFile image moveable ", "Back2.png", "Text2.txt")


def button1func():
    if textbox1.active:
        textbox1.active = False
    else:
        textbox1.active = True

button1 = engine.UIButton(pygame.Rect((20, 20), (100, 50)), 1, "image text ", button1func, "Back2.png", "Button")

UIList.append(background)
UIList.append(textbox1)
UIList.append(textbox2)
UIList.append(button1)

mainMenu = engine.UIContainer(UIList)

while running:
    waiting = True
    while waiting:
        running, waiting = engine.inputStep(mainMenu)
    
    #print("step")
    engine.renderStep(mainMenu)