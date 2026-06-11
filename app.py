import os
import json
import logging
import requests

from src.ia_description import create_description_ia
from src.jira_issue import create_issue
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from google import genai
from pathlib import Path

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)
GEMINI_KEY = os.getenv('GEMINI_KEY')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

JIRA_URL = os.getenv('JIRA_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

app = FastAPI()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.get("/")
def home():
    return {"status": "Servidor do Bot está online!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    
    if "message" in payload:
        message = payload["message"]
        texto_ia_retorno = None
        
        if "text" in message:
            text_content = message['text']
            logging.warning(f"\n[TEXTO] Processando: {text_content}")
            texto_ia_retorno = create_description_ia(text_content, GEMINI_KEY)
            
        elif "voice" in message:
            dados_audio = message["voice"]
            file_id = dados_audio["file_id"]
            
            logging.warning(f"\n[ÁUDIO] Iniciando download do File ID: {file_id}")
            
            url_get_file = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
            resposta_file = requests.get(url_get_file).json()
            
            if resposta_file.get("ok"):
                file_path = resposta_file["result"]["file_path"]
                url_download = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
                arquivo_binario = requests.get(url_download).content
                
                caminho_local = "/tmp/audio_recebido.ogg"
                with open(caminho_local, "wb") as f:
                    f.write(arquivo_binario)
                    
                logging.info(f"Áudio salvo em: {caminho_local}")
                
                client_files = genai.Client(api_key=GEMINI_KEY)
                audio_upload = client_files.files.upload(file=Path(caminho_local))
                
                logging.warning("Analisando áudio com Gemini...")
                texto_ia_retorno = create_description_ia(audio_upload, GEMINI_KEY)
                
                client_files.files.delete(name=audio_upload.name)
        
        if texto_ia_retorno:
            try:
                comando_jira = json.loads(texto_ia_retorno)
                logging.info(f"[JIRA] Dados estruturados recebidos da IA: {comando_jira}")
                create_issue(
                    comand=comando_jira,
                    jira_url=JIRA_URL,
                    jira_email=JIRA_EMAIL,
                    jira_token=JIRA_TOKEN,
                    jira_project_key=JIRA_PROJECT_KEY
                )
            except Exception as e:
                logging.error(f"Falha ao processar JSON ou criar issue no Jira: {e}")
                logging.debug(f"Conteúdo bruto da IA: {texto_ia_retorno}")
                
    return {"status": "ok"}