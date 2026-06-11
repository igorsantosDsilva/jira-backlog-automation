import os
import logging

from google.genai import types
from dotenv import load_dotenv
from google import genai
from pathlib import Path

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(env_path)
GEMINI_KEY = os.getenv('GEMINI_KEY')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_description_ia(request_jira:str, gemini_key:str):
    client = genai.Client(api_key=gemini_key)
    PROMPT_AGILE = """
    Você é um Product Owner técnico. Sua função é analisar este relato e transformá-lo em uma tarefa estruturada para o Jira seguindo estritamente o modelo de conteúdo abaixo.

    MODELO DE CONTEÚDO PARA A DESCRIÇÃO:
    [Título Claro e Objetivo]

    1. Contexto e Detalhes Técnicos
    [Escreva aqui um breve resumo de 2 a 3 linhas para situar quem estiver lendo sobre as regras de negócio, APIs envolvidas, banco de dados ou ferramentas utilizadas no ecossistema do Refinery Station.]

    Formato de User Story: (Eu como... Quero... Para...). Garanta que a história descrita seja independente para não gerar dependências complexas.

    2. Critérios de Aceitação
    Cenário 1: [Nome do Cenário Principal de Sucesso]
    Dado que [contexto inicial ou estado do sistema],
    Quando [a ação ou evento principal acontecer],
    Então [o resultado esperado ou comportamento do sistema].

    Cenário 2: [Nome do Cenário de Exceção ou Falha]
    Dado que [contexto inicial onde algo dá errado],
    Quando [o sistema tentar executar a ação],
    Então [o comportamento esperado de tratamento de erro, log ou alerta].

    Cenário 3: [Nome de Outro Cenário de Validação]
    Dado que [condição de interface, formato ou schema],
    Quando [o processo for carregado ou finalizado],
    Então [o padrão de qualidade visual, estrutural ou de performance esperado].

    3. Definition of Done (DoD)
    [ ] Código/Artefato revisado (ortografia, coesão de texto ou boas práticas de clean code validadas).
    [ ] Testado localmente ou em ambiente de desenvolvimento antes de concluir.
    [ ] Estrutura de dependências, schemas ou links totalmente validada (sem quebras ou erros).
    [ ] Alterações publicadas com sucesso na branch principal (main/master) ou ambiente de produção.

    REQUISITO DE FORMATO DE SAÍDA:
    Retorne ESTRITAMENTE um objeto JSON válido com a seguinte estrutura (sem markdown ou blocos ```json):
    {
        "title": "Título conciso e claro da tarefa",
        "description": "Insira aqui TODO o conteúdo gerado com base no MODELO DE CONTEÚDO acima (incluindo o Título, o formato de User Story, a seção 1. Contexto, os 3 Cenários completos da seção 2. Critérios de Aceitação e os checkboxes da seção 3. DoD). Use quebras de linha normais (\\n) para separar os parágrafos dentro desta string.",
        "type": "Tarefa",
        "priority": "Qual melhor se adequar"
    }
    O tipo deve ser sempre "Tarefa". As prioridades válidas do Jira geralmente são 'Highest', 'High', 'Medium', 'Low'. Escolha a prioridade que melhor se adapta ao relato do usuário.
    """
    try:
        response = client.models.generate_content(model='gemini-3.1-flash-lite', contents=[PROMPT_AGILE, request_jira], config=types.GenerateContentConfig(
                response_mime_type="application/json"))
        logging.info("Descrição criada com sucesso")
        return response.text
        
    except Exception as e:
        logging.error(f"Erro ao processar relato com Gemini: {e}")
        return None