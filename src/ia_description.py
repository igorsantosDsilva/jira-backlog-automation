from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)
GEMINI_KEY = os.getenv('GEMINI_KEY')

def create_description_ia(request_jira:str, gemini_key:str):
    client = genai.Client(api_key=gemini_key)
    PROMPT_AGILE = """
    Você é um Product Owner técnico. Sua função é analisar este relato e transformá-lo em uma tarefa estruturada para o Jira.

    Retorne ESTRITAMENTE um objeto JSON válido com a seguinte estrutura (sem markdown ou blocos ```json):
    {
        "title": "Título conciso e claro da tarefa",
        "description": "O contexto detalhado em formato de User Story (Eu como... Quero... Para...). Garanta que a história descrita seja independente para não gerar dependências complexas.",
        "type": "Task",
        "priority": "Medium"
    }
    O tipo deve ser sempre "Tarefa". As prioridades válidas do Jira geralmente são 'Highest', 'High', 'Medium', 'Low'.
    """
    try:
        response = client.models.generate_content(model='gemini-3.1-flash-lite', contents=[PROMPT_AGILE, request_jira], config=types.GenerateContentConfig(
                response_mime_type="application/json"))
        return response.text
        
    except Exception as e:
        print(f"[ERRO IA] Falha ao processar relato com Gemini: {e}")
        return None