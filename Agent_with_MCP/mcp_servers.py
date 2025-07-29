import os 

from dotenv import load_dotenv

load_dotenv()

SMITHERY_API_KEY = os.getenv('SMITHERY_API_KEY')

MCP_SERVERS_CONFIG = {
    'sequentialthinking_tools':{
        'url':f'https://server.smithery.ai/@2511319/mcp-sequentialthinking-tools/mcp?api_key={SMITHERY_API_KEY}&profile=neat-ladybug-P7ERTn',
        'transport':'streamable_http'
    },    
    'DuckDuckGo-Search_tool':{
        'url':f'https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp?api_key={SMITHERY_API_KEY}&profile=neat-ladybug-P7ERTn',
        'transport':'streamable_http'
    },
    'Visualization-Charts_tool':{
        'url':f'https://server.smithery.ai/@antvis/mcp-server-chart/mcp?api_key={SMITHERY_API_KEY}&profile=neat-ladybug-P7ERTn',
        'transport':'streamable_http'
    },
}