import pygame
import engine

path = "D:\Files\Code\Python\Engine"
UIList = []

running = True
waiting = True

background = engine.UIBackground(pygame.Rect((0,0), (760, 760)), 0, "image winScale ","Menu Back.png")
textbox1 = engine.UITextBox(pygame.Rect((50, 50), (300, 300)), 1, "textFile image moveable ", "Back2.png", "Text2.txt")
UIList.append(background)
UIList.append(textbox1)

while running:
    waiting = True
    while waiting:
        running, waiting = engine.inputStep(UIList)
    
    print("step")
    engine.renderStep(UIList)