import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

# Pega o token que você acabou de salvar lá no Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.get("/")
def home():
    return {"status": "Servidor do Bot está online!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    
    if "message" in payload:
        message = payload["message"]
        
        if "voice" in message:
            dados_audio = message["voice"]
            file_id = dados_audio["file_id"]
            
            print(f"\n[INFO] Iniciando processo para o File ID: {file_id}")
            
            # --- ETAPA 1: Pedir o caminho do arquivo para o Telegram ---
            url_get_file = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
            resposta_file = requests.get(url_get_file).json()
            
            if resposta_file.get("ok"):
                file_path = resposta_file["result"]["file_path"]
                print(f"[INFO] Caminho do arquivo encontrado: {file_path}")
                
                # --- ETAPA 2: Baixar o arquivo binário (.ogg) ---
                url_download = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
                arquivo_binario = requests.get(url_download).content
                
                # Vamos salvar temporariamente na pasta /tmp do servidor Linux
                caminho_local = "/tmp/audio_recebido.ogg"
                with open(caminho_local, "wb") as f:
                    f.write(arquivo_binario)
                    
                print(f"[SUCESSO] Áudio baixado e salvo localmente em: {caminho_local}")
                print(f"[INFO] Tamanho do arquivo: {os.path.getsize(caminho_local)} bytes")
                
                # Próximo passo será jogar esse arquivo na IA de transcrição...
                
            else:
                print(f"[ERRO] Falha ao obter file_path do Telegram: {resposta_file}")
                
    return {"status": "ok"}