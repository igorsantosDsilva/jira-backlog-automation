import os
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Servidor do Bot está online!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    
    # 1. Verifica se existe uma mensagem no payload
    if "message" in payload:
        message = payload["message"]
        chat_id = message["chat"]["id"]
        
        # Cenário A: Você mandou TEXTO
        if "text" in message:
            texto_recebido = message["text"]
            print(f"\n[TEXTO] Mensagem de texto recebida de {message['from']['first_name']}: {texto_recebido}")
            
        # Cenário B: Você mandou ÁUDIO (Mensagem de voz)
        elif "voice" in message:
            dados_audio = message["voice"]
            file_id = dados_audio["file_id"] # Esse ID é a chave para baixar o arquivo depois
            duracao = dados_audio["duration"]
            
            print(f"\n[ÁUDIO] Áudio recebido!")
            print(f"-> File ID (ID do arquivo no Telegram): {file_id}")
            print(f"-> Duração: {duracao} segundos")
            
        else:
            print("\n[OUTRO] Recebeu um formato não mapeado (foto, sticker, etc).")
            
    return {"status": "ok"}