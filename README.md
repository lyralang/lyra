![Original Logo Symbol](assets/art/logo.png)

**Lyra** is a cutting-edge programming language that blends the best features from TypeScript and Python, offering developers a unique, flexible coding experience. It integrates the robustness of static typing with the flexibility of an interpreted language, delivering performance with ease of use.

**Static Typing**: Taking a leaf from TypeScript's book, Lyra incorporates optional static typing, catching errors at compile time and improving tooling support. Code refactoring, auto-completion, hinting, and documentation generation are much more efficient, thanks to this feature.

**Interpreted Nature**: Like Python, Lyra is an interpreted language, facilitating quick and efficient run of scripts without the necessity for prior compilation.

**Strong Standard Library**: A robust and comprehensive standard library is one of Lyra's highlights, inspired by Python's offering. It provides developers with a vast selection of modules, available out-of-the-box, and capable of performing a wide array of tasks.

**Indentation Syntax**: Adopting Python's hallmark indentation syntax, Lyra uses indentation to denote blocks of code, improving readability and making code look cleaner.

**Object-Oriented and Functional Programming**: Borrowing from both TypeScript and Python, Lyra supports both object-oriented and functional programming paradigms. It comes with support for classes and inheritance, as well as functional programming features such as first-class functions, map/filter/reduce operations, and more.

**Asynchronous Programming**: Lyra offers robust support for asynchronous programming, inspired by TypeScript (and JavaScript), making use of the async/await syntax for non-blocking code execution.

**Generators and Iterators**: Inspired by Python, Lyra's approach to iterators and generators is smooth and efficient, facilitating the handling of data streams and asynchronous programming.

**Decorators**: Lyra incorporates the use of decorators to modify classes, methods, or properties, a feature shared by both TypeScript and Python, enhancing its meta-programming capabilities.

**Transpiling**: Similar to TypeScript, Lyra is designed to be transpilable to other languages for improved compatibility and performance. This feature becomes particularly beneficial for web development, where Lyra code can be transpiled to JavaScript for broader compatibility.

**Interoperability**: A major advantage of Lyra is its interoperability with other languages. It allows developers to call upon JavaScript or Python libraries, reminiscent of how TypeScript uses JavaScript libraries and Python uses C libraries.

In essence, Lyra combines the best of TypeScript and Python, offering a compelling mix of versatility, efficiency, and power. Its distinct features cater to a broad spectrum of programming needs, making it a popular choice among developers.

---

**Sample Code**: In this program, we define two asynchronous functions, fetch_data and get_user_data. The fetch_data function sends an HTTP GET request to a given URL and returns the response. The get_user_data function uses fetch_data to retrieve data for a specific user from a hypothetical API. The main function is also asynchronous and calls get_user_data with a specific user ID, then prints the data it receives.
Finally, main() is called to execute the program. The use of async/await syntax in Lyra allows these HTTP requests to be handled in a non-blocking manner, improving the program's efficiency.



```typescript
# Lyra Sample Program
import async, fetch from '@lyra:core';

// Define an asynchronous function
async sub fetch_data(url: string): 
    response = await http.get(url)
    return response

// Define another asynchronous function that uses the first
async sub get_user_data(user_id: string): 
    url = "https://api.lyralang.org/users/:user_id" ::user_id
    user_data = await fetch_data(url)
    return user_data

// Call the function
async sub main():
    user_id = "12345"
    data = await get_user_data(user_id)
    print(data)

// Run the main function
main()
```


```typescript
const BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

// Encodes a string to base64 using byte conversion and base64 encoding
sub lyra_base64_encode(input: string) { 
    return "".join([lyra_bytes_to_base64(bytes(input)[i:i+3]) for i in range(0, len(bytes(input)), 3)]);
}

// Converts a group of bytes to base64 with padding for incomplete groups
sub lyra_bytes_to_base64(byte_group: array) { 
    return "".join([BASE64_CHARS[byte] for byte in byte_group]).ljust(4, '=');
```
