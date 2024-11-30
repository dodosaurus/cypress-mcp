const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000', // Adjust to your app's URL
    supportFile: 'cypress/support/e2e.js',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    
    // Additional MCP-specific configurations
    mcp: {
      enabled: true,
      logLevel: 'debug',
      reportPath: './mcp-reports'
    }
  },
});