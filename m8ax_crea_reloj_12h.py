# M8AX - Programa Para Crear Un Video De Un Reloj Analógico, Con Todas Sus Horas, Minutos Y Segundos.
# La Variable segundoscalcular Es La Que Indica El Número De Relojes A Realizar Para Posteriormente Hacer El Video.
# Si segundoscalcular=86400 Se Hacen 86400 Relojes Para Hacer El Video... 24h
# Si segundoscalcular=43200 Se Hacen 43200 Relojes Para Hacer El Video... 12h - Por Defecto.
# Usa Una Imágen De Fondo fondoreloj.PnG, Incluida...

import cv2
import glob
import errno
import numpy as np
import time
import diffusers
import os
import datetime
import math
from shutil import rmtree

def array_to_tuple(arr):
    return tuple(arr.reshape(1, -1)[0])

def agregar_cero(valor):
    return f"{valor:02d}"

def segahms(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return horas, minutos, segundos

def segahmss(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return f"{horas}h:{minutos}m:{int(segundos)}s"

def barra_progreso_roja(progreso, total, tiembarra):
    porcen = 100 * (progreso / float(total))
    segrestante = 0
    if porcen > 0:
        segrestante = (100 * (tiembarra - time.time()) / porcen) - (
            tiembarra - time.time()
        )
    barra = "█" * int(porcen) + "-" * (100 - int(porcen))
    print(
        (
            f"\r\033[38;2;{255};{0};{0}m|{barra}| - ETA - {segahmss(segrestante*-1)} -"
            f" {porcen:.2f}%      "
        ),
        end="\r\033[0m",
    )

os.system("cls")

try:
    rmtree("M8AX-HoraS")
except:
    nn = 0

try:
    os.mkdir("M8AX-HoraS")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

colores = {
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "red": (0, 0, 255),
    "yellow": (0, 255, 255),
    "magenta": (255, 0, 255),
    "cyan": (255, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (125, 125, 125),
    "rand": np.random.randint(0, high=256, size=(3,)).tolist(),
    "dark_gray": (50, 50, 50),
    "light_gray": (220, 220, 220),
}

image = np.zeros((640, 640, 3), dtype="uint8")
image[:] = colores["black"]
img2 = cv2.imread('fondoreloj.PnG')
dst = cv2.addWeighted(image,0.5,img2,0.7,0)
image=dst

hours_orig = np.array(
    [
        (620, 320),
        (580, 470),
        (470, 580),
        (320, 620),
        (170, 580),
        (60, 470),
        (20, 320),
        (60, 170),
        (169, 61),
        (319, 20),
        (469, 60),
        (579, 169),
    ]
)

hours_dest = np.array(
    [
        (600, 320),
        (563, 460),
        (460, 562),
        (320, 600),
        (180, 563),
        (78, 460),
        (40, 320),
        (77, 180),
        (179, 78),
        (319, 40),
        (459, 77),
        (562, 179),
    ]
)

for i in range(0, 12):
    cv2.line(
        image,
        array_to_tuple(hours_orig[i]),
        array_to_tuple(hours_dest[i]),
        colores["white"],
        3,
    )

cv2.circle(image, (320, 320), 310, colores["white"], 10)
cv2.putText(image, "M8AX & MvIiIaX", (198, 100), 1, 2, colores["white"], 1, cv2.LINE_AA)
cv2.putText(
    image, "https://oncyber.io/@m8ax", (96, 430), 1, 2, colores["white"], 1, cv2.LINE_AA
)

image_original = image.copy()
nn = 0
tiembarra = time.time()
totaltiem = tiembarra
print("\nM8AX - ... Haciendo Imágenes De Relojes ...\n")
segundoscalcular = 43200

for k in range(0, segundoscalcular):

    hour, minute, second = segahms(k)
    cv2.putText(
        image,
        str(agregar_cero(hour))
        + ":"
        + str(agregar_cero(minute))
        + ":"
        + str(agregar_cero(second)),
        (250, 530),
        1,
        2,
        colores["cyan"],
        1,
        cv2.LINE_AA,
    )

    second_angle = math.fmod(second * 6 + 270, 360)
    minute_angle = math.fmod(minute * 6 + 270, 360)
    hour_angle = math.fmod((hour * 30) + (minute / 2) + 270, 360)
    second_x = round(320 + 310 * math.cos(second_angle * 3.14 / 180))
    second_y = round(320 + 310 * math.sin(second_angle * 3.14 / 180))
    cv2.line(image, (320, 320), (second_x, second_y), colores["red"], 2)
    minute_x = round(320 + 260 * math.cos(minute_angle * 3.14 / 180))
    minute_y = round(320 + 260 * math.sin(minute_angle * 3.14 / 180))
    cv2.line(image, (320, 320), (minute_x, minute_y), colores["white"], 8)
    hour_x = round(320 + 220 * math.cos(hour_angle * 3.14 / 180))
    hour_y = round(320 + 220 * math.sin(hour_angle * 3.14 / 180))
    cv2.line(image, (320, 320), (hour_x, hour_y), colores["white"], 10)
    cv2.circle(image, (320, 320), 10, colores["dark_gray"], -1)
    cv2.imwrite("./M8AX-HoraS/M8AX-Reloj-" + str(k) + ".PnG", image)
    cv2.imshow("clock", image)
    cv2.waitKey(1)
    image = image_original.copy()
    barra_progreso_roja((k * 100) / segundoscalcular, 100, tiembarra)
barra_progreso_roja((segundoscalcular * 100) / segundoscalcular, 100, tiembarra)
cv2.destroyAllWindows()
print("\n\nM8AX - ... Imágenes Terminadas, Haciendo Video ...\n")
framesize = ((640), (640))
outv = cv2.VideoWriter(
    "M8AX-Reloj-12h" + "-Video.WebM",
    cv2.VideoWriter_fourcc(*"vp09"),
    1,
    framesize,
)

tiembarra = time.time()
print("")

for filename in sorted(glob.glob("./M8AX-HoraS/*.png"), key=os.path.getmtime):
    imgv = cv2.imread(filename)
    outv.write(imgv)
    nn = nn + 1
    barra_progreso_roja(
        (nn * 100) / (len(glob.glob("./M8AX-HoraS/*.png"))), 100, tiembarra
    )

barra_progreso_roja((nn * 100) / (len(glob.glob("./M8AX-HoraS/*.png"))), 100, tiembarra)
print("\n")
print(*sorted(glob.glob("./M8AX-HoraS/*.png"), key=os.path.getmtime), sep="\n")
outv.release()
calpors = round((segundoscalcular) / (time.time() - totaltiem), 3)
print(
    f"\n... Video Realizado Correctamente ...\n\n----- M8AX INFORMACIÓN -----\n\nRelojes Creados - {segundoscalcular}.\n\nTiempo De Proceso - {round(time.time()-totaltiem,3)} Segundos - {segahmss(time.time()-totaltiem)}.\n\nRelojes Por Segundo Procesados - {calpors} Cal/s.\n\nA Este Rítmo, En Un Minuto Se Realizan - {round(calpors*60,3)} Relojes.\n\nA Este Rítmo, En Una Hora Se Realizan - {round(calpors*3600,3)} Relojes."
)
print("\nSuscribete A Mi Canal De Youtube - https://youtube.com/m8ax")