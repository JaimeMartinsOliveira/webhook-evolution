import httpx
from src.core.config import settings


class EvolutionClient:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_KEY
        self.instance = settings.EVOLUTION_INSTANCE
        self.headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }

    async def enviar_mensagem(self, numero: str, texto: str):
        """Envia uma mensagem de texto (feedback) para o usuário no WhatsApp"""
        url = f"{self.base_url}/message/sendText/{self.instance}"
        payload = {
            "number": numero,
            "text": texto
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)
                return response.json()
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                return None

    async def baixar_midia(self, message_id: dict) -> str:
        """
        Busca o arquivo na Evolution API caso ele não venha completo no Webhook.
        message_id é o objeto 'key' que vem no webhook.
        """
        url = f"{self.base_url}/chat/getBase64FromMediaMessage/{self.instance}"
        payload = {
            "message": message_id
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)
                if response.status_code == 200:
                    dados = response.json()
                    # A Evolution retorna a string base64 da mídia
                    return dados.get("base64")
                else:
                    print(f"Erro ao baixar mídia: {response.text}")
                    return None
            except Exception as e:
                print(f"Erro de conexão com Evolution: {e}")
                return None


# Instância única para ser importada em outras partes do app
evolution = EvolutionClient()