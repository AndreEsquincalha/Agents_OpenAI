import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
# Tem memoria que armazena no SQLite
# pesquisar para deixar a memoria persistente fora do tempo de execução
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from mcp_servers import MCP_SERVERS_CONFIG
from prompts import AGENT_SYSTEM_PROMPT

async def main():
    model = ChatOpenAI(model='gpt-4o-mini')
    memory = MemorySaver()

    mcp_client = MultiServerMCPClient(MCP_SERVERS_CONFIG)
    tools = await mcp_client.get_tools()

    agent_executor = create_react_agent(
        model=model,
        tools=tools,
        prompt=AGENT_SYSTEM_PROMPT,
        checkpointer=memory,
    )
    
    config = {'configurable':{'thread_id':'1'}}

    while True:
        input_message = {
            'role': 'user',
            'content':input('Digite: ')
        }
        async for step in agent_executor.astream(
            {'messages': [input_message]}, config, stream_mode='values'
        ):
            step['messages'][-1].pretty_print()

asyncio.run(main())