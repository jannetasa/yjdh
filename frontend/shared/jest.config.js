const sharedConfig = require('../jest.config.js');
module.exports = {
  ...sharedConfig,
  globals: {
    'ts-jest': {
      tsconfig: '<rootDir>/../tsconfig.json',
    },
  },
  moduleNameMapper: {
    ['^shared/test/(.*)$']: '<rootDir>/test/$1',
    [`^shared\/(.*)$`]: '<rootDir>/src/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/src/__tests__/utils/setupTests.ts'],
  coveragePathIgnorePatterns: [
    '<rootDir>/src/server/next-server.js',
    '<rootDir>/test/',
  ],
};
