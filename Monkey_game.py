import pygame
import random
import math
from pygame import mixer


# Iniciar pygame
pygame.init()
# crecar pantalla
pantalla = pygame.display.set_mode((800,600))

# Titulo e icono
pygame.display.set_caption("Islande")
icono = pygame.image.load("isla (1).png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

# agregar musica de fondo
mixer.music.load("musica de fondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)


# variables jugador
img_jugador = pygame.image.load("mono.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables enemigos
img_enemigo =[]
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("pajaro.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# variables del disparo
disparo = []
img_disparo = pygame.image.load("platano.png")
disparo_x = 0
disparo_y = 500
disparo_x_cambio = 0
disparo_y_cambio = 1
disparo_visible = False

# variable puntaje
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf",32)
texto_x = 10
texto_y = 10

# texto final juego
fuente_final = pygame.font.Font("freesansbold.ttf",40)


def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO",True,(0,0,0))
    pantalla.blit(mi_fuente_final,(60,200))
# funcion mostar puntaje


def mostar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}",True,(0,0,0 ))
    pantalla.blit(texto,(x,y))


# funcion jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))


# funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))


# funcion disparo
def hacer_disparo(x,y):
    global disparo_visible
    disparo_visible = True
    pantalla.blit(img_disparo,(x + 16,y + 10))


# funcion detectar colisiones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2,2) + math.pow(y_2 - y_1,2))
    if distancia < 27:
        return True
    else:
        return False


# loop del juego
se_ejecuta = True
while se_ejecuta:
    # imagen fondo
    pantalla.blit(fondo,(0,0))
    # iterar eventos
    for evento in pygame.event.get():

        # evento para cerrar el programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                nuevo_disparo = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                disparo.append(nuevo_disparo)

        # evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or  evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 450:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]

        # mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        # colision
        for disparos in disparo:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], disparos["x"], disparos["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("golpe.mp3")
                sonido_colision.play()
                disparo.remove(disparos)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break
        enemigo(enemigo_x[e], enemigo_y[e],e)

    # moviento disparo
    for disparos in disparo:
        disparos["y"] += disparos["velocidad"]
        pantalla.blit(img_disparo,(disparos["x"] + 16, disparos["y"] + 10))
        if disparos["y"] < 0:
            disparo.remove(disparos)

    if disparo_visible:
        hacer_disparo(disparo_x,disparo_y)
        disparo_y -= disparo_y_cambio

    jugador(jugador_x,jugador_y)

    mostar_puntaje(texto_x,texto_y)

    # actualizar
    pygame.display.update()
