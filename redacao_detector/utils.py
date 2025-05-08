import os
import numpy as np


def is_image_file(filepath):
    extensoes = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]
    _, ext = os.path.splitext(filepath)
    return ext.lower() in extensoes


def agrupar_por_linhas(retangulos, tolerancia_y=20):
    if not retangulos:
        return []

    retangulos_ordenados = sorted(retangulos, key=lambda r: r[1])

    linhas = [[retangulos_ordenados[0]]]

    for retangulo in retangulos_ordenados[1:]:
        _, y, _, h = retangulo
        ultimo_grupo = linhas[-1]
        _, ultimo_y, _, ultimo_h = ultimo_grupo[-1]

        if abs((y + h / 2) - (ultimo_y + ultimo_h / 2)) < tolerancia_y:
            ultimo_grupo.append(retangulo)
        else:
            linhas.append([retangulo])

    return linhas


def agrupar_palavras(linha, distancia_x=30):
    if not linha:
        return []

    palavras = [[linha[0]]]

    for retangulo in linha[1:]:
        x, y, w, h = retangulo
        ultimo_grupo = palavras[-1]
        ultimo_x, _, ultimo_w, _ = ultimo_grupo[-1]

        if x - (ultimo_x + ultimo_w) < distancia_x:
            ultimo_grupo.append(retangulo)
        else:
            palavras.append([retangulo])

    resultado = []
    for palavra in palavras:
        if not palavra:
            continue

        x_min = min(r[0] for r in palavra)
        y_min = min(r[1] for r in palavra)
        x_max = max(r[0] + r[2] for r in palavra)
        y_max = max(r[1] + r[3] for r in palavra)

        resultado.append((x_min, y_min, x_max - x_min, y_max - y_min))

    return resultado
