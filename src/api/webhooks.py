from fastapi import APIRouter, Request, BackgroundTasks
from src.services.file_handler import salvar_arquivo
from src.services.evolution_client import evolution

router = APIRouter()


@router.post("/evolution")
async def receber_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    if payload.get("event") == "messages.upsert":
        data = payload.get("data", {})
        message_type = data.get("messageType")

        if message_type in ["documentMessage", "imageMessage"]:
            msg_content = data.get("message", {}).get(message_type, {})
            telefone = data.get("key", {}).get("remoteJid", "").split("@")[0]
            nome_original = msg_content.get("title") or msg_content.get("fileName") or "sem_nome"
            mimetype = msg_content.get("mimetype", "").split("/")[-1]

            # Tenta pegar o base64 direto do webhook
            base64_data = data.get("base64")

            # Se a Evolution não enviou no webhook (o que é mais seguro para arquivos grandes)
            # Nós usamos o nosso Client para ir lá e baixar!
            if not base64_data:
                print("Arquivo não veio no webhook. Buscando via Evolution Client...")
                base64_data = await evolution.baixar_midia(data.get("key"))

            if base64_data:
                # Salva o arquivo no disco
                salvar_arquivo(base64_data, nome_original, mimetype, telefone)

                # Usa o Client para enviar uma confirmação de volta pelo WhatsApp (assíncrono)
                msg_feedback = f"✅ Arquivo *{nome_original}* recebido e armazenado com sucesso!"
                background_tasks.add_task(evolution.enviar_mensagem, telefone, msg_feedback)

    return {"status": "ok"}