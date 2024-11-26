"""
Lisp dialects in Python

https://norvig.com/lispy.html https://norvig.com/lispy2.html

Why learning compilers is important: https://steve-yegge.blogspot.com/2007/06/rich-programmer-food.html

phases of compilers
parsing: text -> abstract syntax tree (AST)
text -> |lexical analysis| -> tokens -> |syntactoc analysis| -> AST
type checking/determination
code geneeration (compiling)
generation of the lower level instructions/code
https://norvig.com/lispy.html

Scheme: 5 keywords + 8 syntactic forms
Python: 33 keywords + 110 syntactic forms
Java: 50 keywrods + 133 syntactic forms
"""

# Nuggets from https://norvig.com/lispy.html
#
# Scheme programs consist solely of expressions. There is no statement/expression distinction.
# Numbers (e.g. 1) and symbols (e.g. A) are called atomic expressions; they cannot be broken into pieces. These are similar to their Java counterparts, except that in Scheme, operators such as + and > are symbols too, and are treated the same way as A and fn.
# Everything else is a list expression: a "(", followed by zero or more expressions, followed by a ")". The first element of the list determines what it means:
# A list starting with a keyword, e.g. (if ...), is a special form; the meaning depends on the keyword.
# A list starting with a non-keyword, e.g. (fn ...), is a function call.
# The beauty of Scheme is that the full language only needs 5 keywords and 8 syntactic forms. In comparison, Python has 33 keywords and 110 syntactic forms, and Java has 50 keywords and 133 syntactic forms. All those parentheses may seem intimidating, but Scheme syntax has the virtues of simplicity and consistency. (Some have joked that "Lisp" stands for "Lots of Irritating Silly Parentheses"; I think it stand for "Lisp Is Syntactically Pure".)





import math
import operator as op
from dataclasses import dataclass
from typing import Callable

# Scheme has 5 keywords + 8 syntactic forms. Let's implement them!
# Read https://norvig.com/lispy.html for references

# keywords = ['define', 'lambda', 'if', 'cond', 'quote']

# types = ['atom', 'list']

# syntactic_forms = ['atom', 'list', 'if', 'define', 'procedure_call', 'quotation', 'assignment', 'procedure_definition']

################ Types

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float


################ Standard Environment
def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

    

# Format
#   (
#       Name of the syntactic form,
#       Does the given expression match the syntactic form?,
#       What to do if it matches?,
#   ),


def eval(expr, env=global_env):
    # symbol
    if isinstance(expr, Symbol):
        
        inner_most_env_having_the_symbol = env.find_innermost_env(expr);
        symbol_value = inner_most_env_having_the_symbol[expr]
        return symbol_value
        

    # number
    elif isinstance(expr, Number):
        
        return expr
        

    # quote
    elif isinstance(expr, List) and len(expr) == 2 and expr[0] == "quote":
        
        quoted_expr = expr[1]
        return quoted_expr
        

    # define
    elif isinstance(expr, List) and len(expr) == 3 and expr[0] == "define":
        
        variable_name, assigned_expr = expr[1], expr[2]
        env[variable_name] = eval(assigned_expr, env)
        

    # set!
    elif isinstance(expr, List) and len(expr) == 3 and expr[0] == "set!":
        
        variable_name, assigned_expr = expr[1], expr[2]
        env.find_innermost_env(variable_name)[variable_name] = eval(assigned_expr, env)
        

    # lambda
    elif isinstance(expr, List) and len(expr) == 3 and expr[0] == "lambda":
        
        params = expr[1]
        body = expr[2]
        return Procedure(params=params, body=body, env=env)
        

    # if
    elif isinstance(expr, List) and len(expr) == 4 and expr[0] == "if":
        
        test = expr[1]
        conseq = expr[2]
        alt = expr[3]
        return conseq if eval(test, env) else eval(alt, env)
        

    # procedure_call
    elif isinstance(expr, List):
        
        proc = eval(expr[0], env)
        args = [eval(exp, env) for exp in expr[1:]]
        return proc(*args)
        
    else:
        raise Exception(f"No matching syntactic form for {expr}")




################ Evaluation (syntactic forms)
def eval(x, env=global_env):
    
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):      # variable reference
        return env.find_innermost_env(x)[x]
    
    elif not isinstance(x, List):  # constant literal
        return x                
    
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    
    else:                          # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)
    








################ Data Model
class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find_innermost_env(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find_innermost_env(var)


class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    def __call__(self, *args): 
        return eval(self.body, Env(self.params, args, self.env))
    
    
    
    
    
    
################ Parsing: parse, tokenize, and read_from_tokens
def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)







################ Interaction: A REPL
def repl(prompt='>>'):
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))

def lispstr(exp):
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)