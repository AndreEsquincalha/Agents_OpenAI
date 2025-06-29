import os 
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

#Instanciar o modelo de LLM
model = ChatOpenAI(model='gpt-3.5-turbo', api_key=api_key)

#Prompt principal criado para o Agente
prompt = '''
Como assistente financeiro pessoal, que respoderá as perguntas dando dicas financeiras e de investimentos.
Responda tudo em português brasileiro.
Perguntas: {q}
'''
prompt_template = PromptTemplate.from_template(prompt)

#Ferramenta para o Agente utilizar de códigos pythons
python_repl = PythonREPL()
python_repl_toll= Tool(
    name='Python REPL',
    description='Um Shell Python. use isso para executar código Python. Execute apenas códigos Python válidos.'
                'Se você precisar obter um retorno do código, usa a função "print(...)".'
                'Use para realizar cálculos financeiro necessários para responder as perguntas e dar dicas',
    func=python_repl.run
)

#Ferramenta para o Agente pesquisar na internet
search = DuckDuckGoSearchRun()
duckduckgo_toll = Tool(
    name='Busca DuckDuckGO',
    description='Útil para encontrar informações e dicas de economia e opções de investimentos'
                'Você sempre deve pesquisar na internet as melhores dicas usando essa ferramenta, não'
                'responda diretamente. Sua resposta deve informar que há elementos pesquisados na internet',

    func=search.run
)

#Instruções prontas, baixadas do hub do langchain, para o Agente se comportar de uma maneira padrão
react_instructions = hub.pull('hwchase17/react')

tools = [python_repl_toll, duckduckgo_toll]

#Passo 1: Criar o agente com os itens criados anteriormente
agent = create_react_agent(
    llm=model,
    tools=tools,
    prompt=react_instructions, 
)

#Passo 2: Criar o executor do agente
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

question = '''
Minha renda é de R$3700 por mês, tenho muitos cartões de crédito com total de 4000 por mês.
Tenho mais despesa de aluguel e combustivel de R$600
Quais dicas você me dá?
'''

output = agent_executor.invoke(
    {'input': prompt_template.format(q=question)}
)

print(output.get('output'))