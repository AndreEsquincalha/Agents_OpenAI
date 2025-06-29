import os 
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_experimental.utilities import PythonREPL
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

#Instanciar o modelo de LLM
model = ChatOpenAI(model='gpt-3.5-turbo', api_key=api_key)

#criação de tool (ferramenta de buscar dados do wikipedia)
python_repl = PythonREPL()
python_repl_tool = Tool(
    name='Python REPL',
    description='Um Shell Python. use isso para executar código Python. Execute apenas códigos Python válidos'
                'Se você precisar obter um retorno do código, usa a função "print(...)".',
    func=python_repl.run

)


#criação de Agente de IA
agent_executor = create_python_agent(
    llm=model,
    tool=python_repl_tool,
    verbose=True,
)

prompt_template = PromptTemplate(
    input_variables=['query'],
    template='''
    Resolva: {query}.
    '''  
)

query = 'quanto é 20 porcento de 3000'
prompt = prompt_template.format(query=query)

response = agent_executor.invoke(prompt)
print(response.get('output'))