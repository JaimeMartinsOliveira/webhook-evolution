import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
    EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "sua_apikey_aqui")
    EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "sua_instancia")

settings = Settings()