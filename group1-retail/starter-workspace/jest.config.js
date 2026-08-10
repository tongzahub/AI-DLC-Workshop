/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  // Company standard: tests live in __tests__/ next to the code they cover.
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: ['**/*.ts', '!**/__tests__/**', '!dist/**', '!node_modules/**'],
  // Points and money are integers here; a failing assertion should say so loudly.
  verbose: true,
};
