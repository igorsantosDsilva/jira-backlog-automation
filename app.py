import os
from fastapi import FastAPI, Request

app = FastAPI()

# Rota simples só para testar se o servidor está vivo
@app.get("/")
def home():
    return {"status": "Servidor do Bot está online!"}

# A rota que vai receber as mensagens do Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    
    # Isso aqui vai printar a mensagem direto no painel da nuvem
    print("\n=== MENSAGEM RECEBIDA DO TELEGRAM ===")
    print(payload)
    print("=====================================\n")
    
    return {"status": "recebido"}