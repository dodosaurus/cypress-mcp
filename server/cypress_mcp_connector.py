import os
import json
import asyncio
import websockets
import subprocess
import logging
from typing import List, Dict, Any

class CypressMCPConnector:
    def __init__(self, project_path: str):
        """
        Initialize the Cypress MCP Connector
        
        :param project_path: Full path to the Cypress project
        """
        self.project_path = project_path
        self.logger = logging.getLogger('CypressMCPConnector')
        logging.basicConfig(level=logging.INFO)
        
        # Validate project structure
        self.validate_project_structure()
    
    def validate_project_structure(self):
        """
        Validate the Cypress project structure
        """
        required_dirs = ['cypress', 'cypress/e2e', 'cypress/fixtures']
        for dir_path in required_dirs:
            full_path = os.path.join(self.project_path, dir_path)
            if not os.path.exists(full_path):
                raise ValueError(f"Missing required directory: {full_path}")
        
        self.logger.info(f"Validated Cypress project at {self.project_path}")
    
    def list_available_tests(self) -> List[str]:
        """
        List all available Cypress test files
        
        :return: List of test file paths relative to cypress/e2e
        """
        integration_path = os.path.join(self.project_path, 'cypress', 'e2e')
        test_files = [
            os.path.join('cypress', 'e2e', f) 
            for f in os.listdir(integration_path) 
            if f.endswith('.cy.js') or f.endswith('.cy.ts')
        ]
        return test_files
    
    def run_cypress_tests(self, 
                           test_specs: List[str] = None, 
                           browser: str = 'chrome') -> Dict[str, Any]:
        """
        Run Cypress tests with specified configuration
        
        :param test_specs: List of specific test files to run
        :param browser: Browser to use for testing
        :return: Test execution results
        """
        # If no test_specs provided, run all tests
        if not test_specs:
            test_specs = self.list_available_tests()
        
        # Prepare Cypress command
        cypress_cmd = [
            'npx', 'cypress', 'run',
            '--browser', browser,
            '--spec', ','.join(test_specs)
        ]
        
        try:
            # Change to project directory
            original_dir = os.getcwd()
            os.chdir(self.project_path)
            
            # Run tests
            result = subprocess.run(
                cypress_cmd, 
                capture_output=True, 
                text=True
            )
            
            # Return to original directory
            os.chdir(original_dir)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_test_file(self, 
                          filename: str, 
                          content: str) -> Dict[str, Any]:
        """
        Create a new Cypress test file
        
        :param filename: Name of the test file (should end with .cy.js or .cy.ts)
        :param content: Content of the test file
        :return: File creation result
        """
        if not filename.endswith('.cy.js') and not filename.endswith('.cy.ts'):
            filename += '.cy.js'  # Default to .cy.js
        
        file_path = os.path.join(
            self.project_path, 
            'cypress', 
            'integration', 
            filename
        )
        
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {
                'success': True,
                'file_path': file_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Example usage
def main():
    connector = CypressMCPConnector("/Users/dodosaurus/Documents/LOCAL/cypress-mcp")
    
    # List available tests
    available_tests = connector.list_available_tests()
    print("Available Tests:", available_tests)
    
    # Run all tests
    test_results = connector.run_cypress_tests()
    print("Test Results:", test_results)

if __name__ == '__main__':
    main()