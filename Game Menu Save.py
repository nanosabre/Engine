import pygame
import csv
import classes

maxLayers = 21

#Parameters
resolution = [768, 768]
path = "D:\Files\Code\Python\Engine"

pygame.init()
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)




#"LIST" OF ONE ELEMENT REPRESENTING THE ELEMENT FOCUSED BY USER
# ITS A LIST SO PYTHON STORES JUST THE POINTER FOR LESS MEM USAGE I THINK?
focused = []





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
            UIList.append(classes.UIBackground(
                row['name'],
                int(row['layer']),
                (int(row['x']), int(row['y'])),
                (int(row['height']), int(row['height'])),
                 row['attributes'],
                 data
            ))
        elif "textbox" in row['name']:
            UIList.append(classes.UITextbox(
                row['name'],
                int(row['layer']),
                (int(row['x']), int(row['y'])),
                (int(row['height']), int(row['height'])),
                 row['attributes'],
                 data
            ))
        elif "button" in row['name']:
            UIList.append(classes.UIButton(
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
                    if not UIE.focused:
                        focused.remove(UIE)
                        continue
                    waiting = UIE.userInput(event)
                    if UIE.rect.collidepoint(mousePos):
                        skip = True
                if not skip and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for layer in reversed(range(maxLayers)):
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
    for layer in range(maxLayers):
        for UIE in UIList:
            #EXCLUDE FOCUSED OBJECT TO PREVENT DOUBLE-DRAWING
            if UIE.layer == layer and not UIE.hidden:
                screen.blit(UIE.surf, UIE.rect)

    #RENDER FRAME ON SCREEN
    pygame.display.flip()


pygame.quit()