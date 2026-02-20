from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.services.file_handler import listar_arquivos_baixados, DOWNLOAD_DIR
import os

router = APIRouter()


@router.get("/listar")
def listar_arquivos():
    """Retorna uma lista de todos os arquivos disponíveis para o outro time processar."""
    arquivos = listar_arquivos_baixados()
    return {
        "quantidade": len(arquivos),
        "arquivos": arquivos,
        "mensagem": "Use a rota /arquivos/download/{nome_arquivo} para baixar"
    }


@router.get("/download/{nome_arquivo}")
def baixar_arquivo(nome_arquivo: str):
    """Permite que o outro time faça o download do arquivo físico."""
    caminho_arquivo = os.path.join(DOWNLOAD_DIR, nome_arquivo)

    if not os.path.exists(caminho_arquivo):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(path=caminho_arquivo, filename=nome_arquivo)