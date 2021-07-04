import pygame
import numpy as np
import time

pygame.init()
#tamaño de la pantalla
size = width, height = 700, 700

screen = pygame.display.set_mode(size)

BG_COLOR = (10,10,10) # Define background color
LIVE_COLOR = (255,255,255) #color celda viva
DEAD_COLOR = (128,128,128) #color celda muerta

screen.fill(BG_COLOR)

#Numero de celdas
nx_Cells = 50
ny_Cells = 50

#Dimensiones de la celda
dimCW = width / nx_Cells
dimCH = height/ ny_Cells

#Estado de las Celdas. 1 = viva, 0 = muerta 
gameState = np.zeros((nx_Cells, ny_Cells))

#automatas predefinidos

#automata "palo"
gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1

#automata "caminante"
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

pauseRun = False

running = True

#main loop
while running:

    new_gameState = np.copy(gameState) # Copy status

    #detectamos los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #se cierr la pantalla
            running = False #cerramos el juego

        if event.type == pygame.KEYDOWN: #se presiona una tecla
            pauseRun = not pauseRun #pausamos el juego

        mouseClick = pygame.mouse.get_pressed() #presionamos un boton del muse
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos() #obtenemos la posicion del cursor en ese momento
            x, y = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH)) #ubicamos la celda señalada
            new_gameState[x,y] = not mouseClick[2] #asignamos el estado a la celda (btn der: muere; btn izq: vive)
    
    screen.fill(BG_COLOR)
    
    for y in range(0, ny_Cells):
        for x in range(0, nx_Cells):

            if not pauseRun:
                #Calculo de vecinos cercnos
                n_neigh = gameState[(x-1) % nx_Cells, (y-1) % ny_Cells] + \
                        gameState[(x) % nx_Cells, (y-1) % ny_Cells] + \
                        gameState[(x+1) % nx_Cells, (y-1) % ny_Cells] + \
                        gameState[(x-1) % nx_Cells, (y) % ny_Cells] + \
                        gameState[(x+1) % nx_Cells, (y) % ny_Cells] + \
                        gameState[(x-1) % nx_Cells, (y+1) % ny_Cells] + \
                        gameState[(x) % nx_Cells, (y+1) % ny_Cells] + \
                        gameState[(x+1) % nx_Cells, (y+1) % ny_Cells]

                # Rule 1: Una celula muerta con 3 vecinas revive
                if gameState[x,y] == 0 and n_neigh==3:
                    new_gameState[x,y] = 1
                # Rule 2: Una celula viva con mas de 3 o menos de 2 vecinos vivos muere
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_gameState[x,y] = 0

            #Poligno para cada celda a dibujar
            poly = [
                    ((x)       * dimCW, (y)       * dimCH), 
                    ((x + 1)   * dimCW, (y)       * dimCH), 
                    ((x + 1)   * dimCW, (y + 1)   * dimCH),
                    ((x)       * dimCW, (y + 1)   * dimCH)
                   ]
            
            #Dibujamos el cada celda
            if new_gameState[x,y] == 0:
                pygame.draw.polygon(screen, DEAD_COLOR, poly, 1)
            else:
                pygame.draw.polygon(screen, LIVE_COLOR, poly, 0)

    gameState = np.copy(new_gameState)
    time.sleep(0.01)
    pygame.display.flip()
