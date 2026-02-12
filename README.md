# Tanishqecom
Tanishq ecom lead management

## Factorial Function

This repository includes a function to calculate the factorial of a number.

### Usage

```javascript
const factorial = require('./factorial');

console.log(factorial(5)); // Output: 120
console.log(factorial(10)); // Output: 3628800
```

### Features

- Calculates factorial of non-negative integers
- Input validation (throws errors for negative numbers, decimals, and non-numeric inputs)
- Efficient iterative implementation
- Well-tested with comprehensive test suite

### API

**factorial(n)**

Calculates the factorial of a number.

- **Parameters:**
  - `n` (number): A non-negative integer
- **Returns:** The factorial of n
- **Throws:** Error if input is negative, not an integer, or not a number

### Examples

```javascript
factorial(0)  // 1
factorial(1)  // 1
factorial(5)  // 120
factorial(10) // 3628800
factorial(-1) // throws Error: Input must be a non-negative integer
factorial(3.5) // throws Error: Input must be an integer
```

### Running Tests

```bash
npm test
```

### Running Examples

```bash
npm run example
```
