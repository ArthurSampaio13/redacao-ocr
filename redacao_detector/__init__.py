__version__ = "0.1.0"

from redacao_detector.detector import (
    corrigir_rotacao,
    detectar_areas_texto,
    processar_imagem,
    processar_diretorio,
)

__all__ = [
    "corrigir_rotacao",
    "detectar_areas_texto",
    "processar_imagem",
    "processar_diretorio",
]
