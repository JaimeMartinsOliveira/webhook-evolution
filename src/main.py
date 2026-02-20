from fastapi import FastAPI
from src.api.webhooks import router as webhook_router
from src.api.files import router as files_router

app = FastAPI(title="Hub de Captura de Documentos WhatsApp")

app.include_router(webhook_router, prefix="/webhook", tags=["Captura da Evolution"])
app.include_router(files_router, prefix="/arquivos", tags=["Acesso do Outro Time"])