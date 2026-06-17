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
        Você é um Product Owner técnico e Mentor de Aprendizado. Sua função é analisar este relato e transformá-lo em uma tarefa estruturada para o Jira, escolhendo o modelo adequado com base no pedido do usuário.

        INSTRUÇÃO DE CLASSIFICAÇÃO:
        - Se o relato for sobre implementar código, criar pipelines, fixar bugs ou regras de negócio, use o MODELO A (Desenvolvimento).
        - Se o relato for sobre aprender uma nova tecnologia, ler documentação, estudar conceitos ou fazer cursos, use o MODELO B (Estudo).

        ---

        MODELO A: DESENVOLVIMENTO (Refinery Station)
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

        ---

        MODELO B: ESTUDO E APRENDIZADO
        [Título Claro e Objetivo]

        1. Objetivo de Aprendizado e Contexto
        [Escreva um breve resumo de 2 a 3 linhas explicando o que será estudado, por que esse conhecimento é importante e onde ele será aplicado no futuro.]

        Frase de Foco: (Para dominar o conceito de... Eu vou estudar/praticar... Para ser capaz de...).

        2. Plano de Ação e Prática
        Recursos & Referências:
        [Liste links de documentações, artigos ou cursos relevantes baseados no relato do usuário.]

        Passo a Passo:
        - Bloco 1 (Teoria): [O que ler ou assistir primeiro]
        - Bloco 2 (Prática Ativa): [O que codificar, testar ou replicar na máquina local para fixar o conteúdo]

        3. Critérios de Aceite (DoD de Estudo)
        [ ] Consigo explicar os conceitos principais estudados sem olhar o material de apoio.
        [ ] Consegui replicar o exemplo prático localmente com sucesso.
        [ ] Criei notas, resumos ou snippets de código para consulta rápida no futuro.

        ---

        REQUISITO DE FORMATO DE SAÍDA:
        Retorne ESTRITAMENTE um objeto JSON válido com a seguinte estrutura (sem markdown ou blocos ```json):
        {
            "title": "Título conciso e claro da tarefa",
            "description": "Insira aqui TODO o conteúdo gerado com base no modelo escolhido (Modelo A ou Modelo B). Inclua todos os títulos de seções, textos gerados e os checkboxes [ ]. Use quebras de linha normais (\\n) para separar os parágrafos dentro desta string.",
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