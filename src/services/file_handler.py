import base64
import os
import uuid
from datetime import datetime

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def salvar_arquivo(base64_string: str, nome_original: str, extensao: str, telefone_remetente: str) -> dict:
    """Salva o arquivo e retorna os metadados para o outro time usar."""

    # Cria um nome único com a data e o telefone de quem enviou para facilitar a organização
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_seguro = f"{data_hora}_{telefone_remetente}_{uuid.uuid4().hex[:6]}.{extensao}"

    caminho_completo = os.path.join(DOWNLOAD_DIR, nome_seguro)

    # Salva o arquivo no disco
    with open(caminho_completo, "wb") as f:
        f.write(base64.b64decode(base64_string))

    return {
        "nome_arquivo": nome_seguro,
        "nome_original": nome_original,
        "telefone_remetente": telefone_remetente,
        "caminho": caminho_completo
    }


def listar_arquivos_baixados():
    """Lista todos os arquivos disponíveis na pasta."""
    try:
        return os.listdir(DOWNLOAD_DIR)
    except Exception:
        return []