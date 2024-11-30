import asyncio
import websockets
import json
import logging
from cypress_mcp_connector import CypressMCPConnector

class CypressMCPServer:
    def __init__(self, 
                 project_path: str, 
                 host: str = 'localhost', 
                 port: int = 8765):
        self.connector = CypressMCPConnector(project_path)
        self.host = host
        self.port = port
        self.logger = logging.getLogger('CypressMCPServer')
        logging.basicConfig(level=logging.INFO)
    
    async def handle_message(self, websocket, path):
        """
        Handle incoming WebSocket messages
        
        Supported message types:
        - list_tests: List available test files
        - run_tests: Execute specified or all tests
        - create_test: Generate a new test file
        """
        async for message in websocket:
            try:
                msg_data = json.loads(message)
                response = {}
                
                if msg_data.get('type') == 'list_tests':
                    response = {
                        'type': 'test_list',
                        'tests': self.connector.list_available_tests()
                    }
                
                elif msg_data.get('type') == 'run_tests':
                    test_specs = msg_data.get('specs')
                    browser = msg_data.get('browser', 'chrome')
                    
                    response = {
                        'type': 'test_results',
                        **self.connector.run_cypress_tests(
                            test_specs, 
                            browser
                        )
                    }
                
                elif msg_data.get('type') == 'create_test':
                    filename = msg_data.get('filename')
                    content = msg_data.get('content')
                    
                    response = {
                        'type': 'test_creation',
                        **self.connector.create_test_file(filename, content)
                    }
                
                await websocket.send(json.dumps(response))
            
            except Exception as e:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': str(e)
                }))
    
    async def start_server(self):
        """
        Start the WebSocket server
        """
        server = await websockets.serve(
            self.handle_message, 
            self.host, 
            self.port
        )
        self.logger.info(f"Cypress MCP Server running on {self.host}:{self.port}")
        await server.wait_closed()

async def main():
    server = CypressMCPServer(
        "/Users/dodosaurus/Documents/LOCAL/cypress-mcp"
    )
    await server.start_server()

if __name__ == '__main__':
    asyncio.run(main())