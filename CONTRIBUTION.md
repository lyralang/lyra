# Contribution Guidelines for the Lyra Programming Language

First of all, we want to extend a heartfelt thank you for your interest in 
contributing to Lyra - an advanced, innovative programming language that 
integrates the strengths of TypeScript and Python. To ensure the quality, 
readability, and consistency of our codebase, we have set a few guidelines 
that all contributors are expected to follow.

## Code Style

### Naming Conventions

- **Function names** should start with the `lyra_` prefix for any function in 
the standard library and the compiler. This is to differentiate Lyra-specific 
functions from other built-in or user-defined functions. For example, a 
function to add two numbers would be `lyra_add`.

- The **variable names** and **function names** should use the `snake_case` 
convention, which involves all lower case letters and underscores to separate 
words, rather than the `camelCase` convention. For example, `my_variable` or 
`lyra_my_function`.

- **Constants** should be in `UPPER_SNAKE_CASE`.

### Syntax 

Lyra borrows from TypeScript and Python, and thus contributors should be 
familiar with both languages. However, Lyra also introduces unique syntactical 
elements that require special attention:

- Lyra uses Python-style indentation, with each block of code indented under 
its parent block.

- Lyra uses TypeScript's static typing system. Variable types should be 
defined when a variable is declared.

- Remember that Lyra, unlike Python, uses TypeScript's semicolon at the end of 
each statement.

## Contributing Code

### Workflow

1. **Fork** the repository and clone it locally.
2. **Branch** off the master branch for each separate issue or feature you are 
working on.
3. **Commit** your changes with clear, concise commit messages that explain 
your changes.
4. **Test** your changes with the existing test suite and add new tests if 
necessary.
5. **Push** your changes to your fork and submit a **Pull Request**.

### Pull Requests

- Each pull request should relate to a single feature or bug fix.
- Pull requests should be based on the master branch and made to the master 
branch.
- Ensure all tests pass before submitting your pull request.
- Include a detailed explanation of your changes and why you made them.
- Ensure your code adheres to our style guide.

### Reporting Bugs

If you find a bug, please create an issue in our GitHub repository. Be sure to 
include:

- A clear, descriptive title.
- A detailed description of the issue.
- Steps to reproduce the issue.
- The expected and actual outcome.

## Documentation

Contributors are expected to document their code following the 
[JSDoc](https://jsdoc.app/) conventions, as Lyra shares similar documentation 
style with TypeScript. This helps to maintain the readability and usability of 
the code.

Thank you for reading through our contribution guidelines, and we look forward 
to your valuable contributions. Happy coding with Lyra!

