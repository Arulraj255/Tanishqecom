const factorial = require('./factorial');

// Example usage of the factorial function
console.log('Factorial Examples:');
console.log('===================\n');

// Calculate factorials for numbers 0-10
for (let i = 0; i <= 10; i++) {
  console.log(`factorial(${i}) = ${factorial(i)}`);
}

console.log('\nLarger numbers:');
console.log(`factorial(15) = ${factorial(15)}`);
console.log(`factorial(20) = ${factorial(20)}`);

console.log('\nError handling:');
try {
  factorial(-5);
} catch (error) {
  console.log(`factorial(-5) throws: ${error.message}`);
}

try {
  factorial(3.14);
} catch (error) {
  console.log(`factorial(3.14) throws: ${error.message}`);
}
