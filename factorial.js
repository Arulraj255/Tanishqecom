/**
 * Calculate the factorial of a number
 * @param {number} n - The number to calculate factorial for
 * @returns {number} The factorial of n
 * @throws {Error} If n is negative or not an integer
 */
function factorial(n) {
  // Validate input
  if (typeof n !== 'number' || !Number.isInteger(n)) {
    throw new Error('Input must be an integer');
  }
  
  if (n < 0) {
    throw new Error('Input must be a non-negative integer');
  }
  
  // Base cases
  if (n === 0 || n === 1) {
    return 1;
  }
  
  // Calculate factorial iteratively
  let result = 1;
  for (let i = 2; i <= n; i++) {
    result *= i;
  }
  
  return result;
}

module.exports = factorial;
