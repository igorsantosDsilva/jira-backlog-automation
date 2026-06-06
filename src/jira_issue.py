import os
import logging
import requests

from pathlib import Path
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)

JIRA_URL = os.getenv('JIRA_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')
SPREDSHEET_ID = os.getenv('SPREDSHEET_ID')

# Debug: Verificar se as variáveis foram carregadas
logging.info(f"JIRA_URL: {JIRA_URL}")
logging.info(f"JIRA_EMAIL: {JIRA_EMAIL}")
logging.info(f"JIRA_TOKEN: {JIRA_TOKEN}")
logging.info(f"JIRA_PROJECT_KEY: {JIRA_PROJECT_KEY}")

def create_issue(comand, jira_url:str, jira_email:str, jira_token:str, jira_project_key:str):

    
    atividade = comand
    title = atividade['title']
    description = atividade['description']
    type = atividade['type']
    priority = atividade['priority']
    
    payload = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": title,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": type
            },
            "priority": {
                "name": priority
            }
        }
    }

    logging.info(f"Tentando criar issue: {title}")
    logging.debug(f"Payload: {payload}")
    logging.debug(f"Usando projeto: {jira_project_key}")

    response = requests.post(
        f"{jira_url}/rest/api/3/issue",
        json=payload,
        auth=HTTPBasicAuth(
            jira_email,
            jira_token
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 201:
        
        print('deu bom')

    else:

        print(
            "deu ruim"
        )

        print(response.text)