from fastapi import FastAPI, File, UploadFile
import io
import cv2
from PIL import Image
from io import BytesIO
import numpy as np
from redacao_detector.utils import detectar_areas_texto, corrigir_rotacao

app = FastAPI()

# Função para converter imagem
def convert_image(image_bytes):
    img = Image.open(BytesIO(image_bytes))  # Usando PIL para abrir a imagem
    img = np.array(img)  # Convertendo a imagem para array numpy
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convertendo de RGB (PIL) para BGR (OpenCV)
    return img

@app.post("/processar-imagem/")
async def processar_imagem(file: UploadFile = File(...)):
    # Lendo os bytes da imagem enviada
    image_bytes = await file.read()
    
    # Convertendo os bytes para imagem
    imagem = convert_image(image_bytes)
    
    # Corrigindo a rotação da imagem
    imagem_corrigida = corrigir_rotacao(imagem)
    
    # Detectando as áreas de texto na imagem
    imagem_resultado = detectar_areas_texto(imagem_corrigida)
    
    # Codificando a imagem resultante para PNG
    _, img_encoded = cv2.imencode('.png', imagem_resultado)
    
    # Convertendo para bytes
    img_bytes = img_encoded.tobytes()

    # Retornando a imagem processada como resposta
    return {"filename": file.filename, "image": img_bytes}
