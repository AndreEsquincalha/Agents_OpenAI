import os 
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor, Tool
from langchain.prompts import PromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

from langchain_experimental.utilities import PythonREPL

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

#Instanciar o modelo de LLM
model = ChatOpenAI(model='gpt-3.5-turbo', api_key=api_key)

#String de conexão com o banco de dados
db = SQLDatabase.from_uri('sqlite:///ipca.db')

#Instanciando o Toolkit, para atribuir as ferramentas de analise de SQL para o db desejado
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model,
)

#mensagem de sistema padrão do hub do langchain para dar ao Agente
system_message = hub.pull('hwchase17/react')

#Criação do agente
agent = create_react_agent(
    llm=model,
    tools=toolkit.get_tools(),
    prompt=system_message,
)

#Criação do executor do agente
agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
)

#prompt principal para enviar ao Agente
prompt = '''
Use as ferramentas necessárias para responder as perguntas relacionadas ao historico de IPCA ao longo dos anos.
Responda tudo em português brasileiro.
Perguntas: {q}
'''
#Carregando o prompt no template
prompt_template = PromptTemplate.from_template(prompt)

question = '''
Baseado nos dados históricos de IPCA,
faça uma previsão dos valores e IPCA de cada mês futuro até o final de 2024
'''

#chamando a execução do Agente
output = agent_executor.invoke(
    {'input': prompt_template.format(q=question)}
)

print(output.get('output'))