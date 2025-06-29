import os 
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

#Instanciar o modelo de LLM
model = ChatOpenAI(model='gpt-3.5-turbo', api_key=api_key)

#criação de tool (ferramenta de buscar dados do wikipedia)
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        lang='pt'
    )
)

#criação de Agente de IA
agent_executor = create_python_agent(
    llm=model,
    tool=wikipedia_tool,
    verbose=True,
)

prompt_template = PromptTemplate(
    input_variables=['query'],
    template='''
    Pesquise na Web sobre {query} e forneça um resumo sobre o assunto
    '''  
)

query = 'genshin impact'
prompt = prompt_template.format(query=query)

response = agent_executor.invoke(prompt)
print(response.get('output'))