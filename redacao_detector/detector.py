import os
import cv2
import numpy as np
from redacao_detector.utils import (
    is_image_file, 
    agrupar_por_linhas, 
    agrupar_palavras, 
    calcular_angulo_medio
)


def corrigir_rotacao(imagem):
    img_copy = imagem.copy()
    
    cinza = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    
    _, binario = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    contornos, _ = cv2.findContours(binario, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    angulos = []
    for contorno in contornos:
        if cv2.contourArea(contorno) < 100:
            continue
        
        rect = cv2.minAreaRect(contorno)
        
        (x, y), (w, h), angulo = rect
        
        if w < h:
            angulo = angulo - 90
        
        if abs(angulo) < 45:
            angulos.append(angulo)
    
    if not angulos:
        return imagem
    
    angulo_medio = calcular_angulo_medio(angulos)
    
    (h, w) = imagem.shape[:2]
    centro = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(centro, angulo_medio, 1.0)
    
    imagem_corrigida = cv2.warpAffine(imagem, M, (w, h), 
                                      flags=cv2.INTER_CUBIC, 
                                      borderMode=cv2.BORDER_REPLICATE)
    
    return imagem_corrigida


def detectar_areas_texto(imagem, debug=False, params=None):
    default_params = {
        "tam_kernel_dilatacao": (5, 2),
        "block_size": 11,
        "c_value": 10,
        "min_area": 500  
    }

    if params is None:
        params = default_params
    else:
        for key, value in default_params.items():
            if key not in params:
                params[key] = value

    imagem_resultado = imagem.copy()

    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    cinza_blur = cv2.GaussianBlur(cinza, (3, 3), 0)

    binario = cv2.adaptiveThreshold(
        cinza_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, params["block_size"], params["c_value"]
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, params["tam_kernel_dilatacao"])
    dilatado = cv2.dilate(binario, kernel, iterations=2)

    if debug:
        cv2.imshow("Binário", binario)
        cv2.imshow("Dilatado", dilatado)

    contornos, _ = cv2.findContours(dilatado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    retangulos = []
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > params["min_area"]:
            x, y, w, h = cv2.boundingRect(contorno)
            retangulos.append((x, y, w, h))

    linhas = agrupar_por_linhas(retangulos, tolerancia_y=20)
    todas_palavras = [agrupar_palavras(linha, distancia_x=30) for linha in linhas]
    todas_palavras = [palavra for linha in todas_palavras for palavra in linha]

    for (x, y, w, h) in todas_palavras:
        cv2.rectangle(imagem_resultado, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if debug:
        return imagem_resultado, {'binario': binario, 'dilatado': dilatado}
    else:
        return imagem_resultado

def processar_imagem(caminho_imagem, salvar_resultado=True, mostrar_debug=False, params=None):
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        raise FileNotFoundError(f"Não foi possível abrir a imagem: {caminho_imagem}")
    
    imagem_corrigida = corrigir_rotacao(imagem)
    
    if mostrar_debug:
        resultado, debug_imgs = detectar_areas_texto(imagem_corrigida, debug=True, params=params)
    else:
        resultado = detectar_areas_texto(imagem_corrigida, params=params)
    
    if salvar_resultado:
        diretorio_base = os.path.dirname(caminho_imagem)
        nome_arquivo = os.path.basename(caminho_imagem)
        nome_saida = os.path.join(diretorio_base, f"processado_{nome_arquivo}")
        cv2.imwrite(nome_saida, resultado)
        
        if mostrar_debug:
            for nome, img in debug_imgs.items():
                debug_path = os.path.join(diretorio_base, f"debug_{nome}_{nome_arquivo}")
                cv2.imwrite(debug_path, img)
            
        return nome_saida
    else:
        if mostrar_debug:
            return resultado, debug_imgs
        else:
            return resultado



def processar_diretorio(diretorio_entrada, diretorio_saida=None, params=None):
    if diretorio_saida is None:
        diretorio_saida = diretorio_entrada
    
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
    
    for arquivo in os.listdir(diretorio_entrada):
        caminho_completo = os.path.join(diretorio_entrada, arquivo)
        
        if os.path.isfile(caminho_completo) and is_image_file(caminho_completo):
            try:
                print(f"\nProcessando: {arquivo}")
                
                imagem = cv2.imread(caminho_completo)
                if imagem is None:
                    print(f"Erro ao abrir a imagem: {arquivo}")
                    continue
                
                imagem_corrigida = corrigir_rotacao(imagem)
                
                resultado = detectar_areas_texto(imagem_corrigida, params=params)
                
                caminho_saida = os.path.join(diretorio_saida, f"processado_{arquivo}")
                cv2.imwrite(caminho_saida, resultado)
                
                print(f"Salvo como: {caminho_saida}")
                
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")