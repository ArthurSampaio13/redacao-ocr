from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
import cv2
from PIL import Image
from io import BytesIO
import numpy as np
from redacao_detector.detector import detectar_areas_texto, corrigir_rotacao

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def convert_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(image_bytes))
    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return img_bgr


@app.post("/processar-imagem/")
async def processar_imagem(file: UploadFile = File(...)) -> Response:
    image_bytes = await file.read()

    imagem = convert_image(image_bytes)
    imagem_corrigida = corrigir_rotacao(imagem)
    imagem_resultado = detectar_areas_texto(imagem_corrigida)

    success, img_encoded = cv2.imencode(".png", imagem_resultado)
    if not success:
        return Response(status_code=500, content=b"Falha ao codificar imagem")

    img_bytes = img_encoded.tobytes()
    return Response(
        content=img_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f'inline; filename="{file.filename}"'},
    )
