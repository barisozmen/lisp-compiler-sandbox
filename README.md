# lisp-compiler-sandbox

Resources

https://norvig.com/lispy.html
https://norvig.com/lispy2.html

Why learning compilers is important:
https://steve-yegge.blogspot.com/2007/06/rich-programmer-food.html
- phases of compilers
 1. parsing: text -> abstract syntax tree (AST)
    - text -> |lexical analysis| -> tokens -> |syntactoc analysis| -> AST
 2. type checking/determination
 3. code geneeration (compiling)
    - generation of the lower level instructions/code


https://norvig.com/lispy.html
- Scheme: 5 keywords + 8 syntactic forms
- Python: 33 keywords + 110 syntactic forms
- Java: 50 keywrods + 133 syntactic forms



https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c11/c11s1/
![image](https://github.com/user-attachments/assets/eb02d912-f67b-4bc7-920d-b27324b239cf)

![image](https://github.com/user-attachments/assets/f3772667-7ae7-4938-93cd-56f7a9abdbdc)



David Beazley's Compilers Course - https://www.dabeaz.com/compiler.html
- He recommendeds Robert Nystrom's [Crafting Interpreters] book
    - ![image](https://github.com/user-attachments/assets/8d28fcdb-a023-4bb1-86e9-838cdf3a7e6f)

- His talk on parsing tools - [video](https://www.youtube.com/watch?v=zJ9z6Ge-vXs)
- ![image](https://github.com/user-attachments/assets/14c96428-f601-45e7-baec-ae0d01cdd515)


**Explain me the Tree-Walking Interpreter?**
gpt-4o answer:
Process of a Tree-Walking Interpreter

 1 L**exing/Scanning:** The source code is processed to convert it into tokens. This step involves breaking down the input text
   into meaningful components, such as keywords, operators, literals, and identifiers.

 2 **Parsing:** The tokens are parsed to create an Abstract Syntax Tree (AST). The AST is a tree representation of the
   hierarchical syntactic structure of the source code. Nodes in the tree represent constructs in the language such as
   expressions, statements, or declarations.

 3 **Interpreting (Tree Walking):** The interpreter traverses the AST, visiting each node to evaluate and execute it. This
   traversal is typically recursive, with different actions taken depending on the type of each node. For example:

 • Literal Nodes: Directly return a value
 
 • Expression Nodes: Evaluate arithmetic operations, variables, etc.

 • Control Flow Nodes: Handle branching (if statements) and loops (while, for).

 • Function Call Nodes: Execute functions, possibly involving further traversal of the tree for arguments and function
   bodies.



## History of Lisp and Scheme
source: https://norvig.com/lispy2.html
![image](https://github.com/user-attachments/assets/523454ea-d752-43e2-be5d-9a84e154c60a)
- 1932, Alonzo Church, Lambda Calculus
- 1958, John McCarthy, Lisp paper
- 1959, Steve Russell, Lisp implementation
- 1975, Guy Steele, Scheme
- 1975, Gerald Jay Sussman, Scheme

## Relevant
geohot writing Scheme in Haskell
- live sessions: [part 1](https://www.youtube.com/watch?v=5QsC_VeYL4g) + [part 2](https://www.youtube.com/watch?v=DJSyCHlry7Y) + [part 3](https://www.youtube.com/watch?v=JMXzoB0-vQo)
- end result: https://github.com/geohot/haskell-scheme
- following the book https://en.wikibooks.org/wiki/Write_Yourself_a_Scheme_in_48_Hours/First_Steps
