import os
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def resposta_bot(chat_id:int, retorno:str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": retorno
        }
    )
    logging.info(f"Resposta enviada para a conversa: {chat_id}")