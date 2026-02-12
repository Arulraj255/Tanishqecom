const factorial = require('./factorial');

// Test cases
const tests = [
  { input: 0, expected: 1, description: 'factorial of 0' },
  { input: 1, expected: 1, description: 'factorial of 1' },
  { input: 2, expected: 2, description: 'factorial of 2' },
  { input: 3, expected: 6, description: 'factorial of 3' },
  { input: 4, expected: 24, description: 'factorial of 4' },
  { input: 5, expected: 120, description: 'factorial of 5' },
  { input: 10, expected: 3628800, description: 'factorial of 10' },
];

const errorTests = [
  { input: -1, description: 'negative number' },
  { input: 1.5, description: 'decimal number' },
  { input: 'string', description: 'string input' },
  { input: null, description: 'null input' },
];

console.log('Running factorial tests...\n');

let passed = 0;
let failed = 0;

// Test valid inputs
tests.forEach(test => {
  try {
    const result = factorial(test.input);
    if (result === test.expected) {
      console.log(`✓ PASS: ${test.description} = ${result}`);
      passed++;
    } else {
      console.log(`✗ FAIL: ${test.description} - Expected ${test.expected}, got ${result}`);
      failed++;
    }
  } catch (error) {
    console.log(`✗ FAIL: ${test.description} - Unexpected error: ${error.message}`);
    failed++;
  }
});

// Test error cases
errorTests.forEach(test => {
  try {
    const result = factorial(test.input);
    console.log(`✗ FAIL: ${test.description} - Should have thrown an error, got ${result}`);
    failed++;
  } catch (error) {
    console.log(`✓ PASS: ${test.description} - Correctly threw error: ${error.message}`);
    passed++;
  }
});

console.log(`\n${passed} tests passed, ${failed} tests failed`);

if (failed > 0) {
  process.exit(1);
}
