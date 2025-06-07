const codeCoverageTask = require('@cypress/code-coverage/task');

module.exports = {
  e2e: {
    specPattern: 'testClient/**/*.cy.js',
    baseUrl: 'http://localhost:3000',
    setupNodeEvents(on, config) {
      codeCoverageTask(on, config);
      return config;
    },
  },
};
