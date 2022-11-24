import sys
import lex as lex
#reserved words
reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'import': 'IMPORT',
    'from': 'FROM',
    'def': 'DEF',
    'return': 'RETURN',
    'not': 'NOT',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'class': 'CLASS',
    'assert': 'ASSERT',
    'as': 'AS',
    'del': 'DEL',
    'elif': 'ELIF',
    'finally': 'FINALLY',
    'except': 'EXCEPT',
    'global': 'GLOBAL',
    'None': 'NONE',
    'is': 'IS',
    'lambda': 'LAMBDA',
    'pass': 'PASS',
    'nonlocal': 'NONLOCAL',
    'raise': 'RAISE',
    'try': 'TRY',
    'with': 'WITH',
    'yield': 'YIELD',
    'match': 'MATCH',
    'case': 'CASE',
    'print': 'PRINT',

 }

# List of token names.   This is always required
tokens = [
    'NUMBER',
    'OARS',
    'LPAREN',
    'RPAREN',
    'IDN',
    'COM',
    'ATR',
    'BOO',
    'STR',
    'PRS',
    'PTO',
    'RCO',
    'LCO',
    'CAR',
    'COMPLEXO',
    'LISTA',
    'TUPLA',
    'SET',
] + list(reserved.values())


 # Compute column.
 #     inp is the input text string
 #     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1 #Busca entre inicio do texto e a posicao de leitura atual(token), qual a ultima ocorrencia de \n
    return (token.lexpos - line_start) + 1 #retorna a distancia entre o token e a linha anterior



#Identificadores e palavras reservadas
def t_IDN(t): #token Identificador #letra_ (letra_|digito)*
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDN')  # Check for reserved words
    if(t.type != 'IDN'): # ex, se t.type=PRINT --> recebe PRS
        t.type='PRS'
    if (t.value == 'and' or t.value == 'or'): # Se nao for palavra reservada, verifica se é Operado and ou or
        t.type = 'OARS'
    t.value = t.value, t.lineno, find_column(lexer.lexdata, t)  # Valor de t recebe lexema, linha e coluna
    return t



# A regular expression rule with some action code --COMENTARIOS DEVEM VIR ANTES DE STRING E CAR
def t_COM(t):
    r'(\# [^\n]*) | (\" \" \" (.| \n)* \" \" \")'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t) #Valor de t recebe lexema, linha e coluna
    return t



def t_CAR(t): #caracter vem antes de String
    r'(\" . \") | (\' [^\'] \')'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t



def t_STR(t):
    r'(\" .* \") | (\' \' \' (.| \n)* \' \' \') | (\' .* \')'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t


def t_BOO(t):
    r'True | False'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t



def t_OARS(t):
    r' -= | \+= | \* \= | \/ \= | \+ \+ | -- | \+ | - | \* \* | \* | \/ | <> | <= | << | < | >= | >> | > | != | == | & | \| | \^ | %' #OARS vem antes de =
    if(t.value=='-=' or t.value=='+=' or t.value=='++' or t.value=='--' or t.value=='*=' or t.value=='/='):
        t.type = 'PTO'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t



def t_ATR(t):
    r'='
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t


def t_LPAREN(t):
    r'\('
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t


def t_RPAREN(t):
    r'\)'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t


def t_LCO(t):
    r'\['
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t


def t_RCO(t):
    r'\]'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t)
    return t


def t_COMPLEXO(t):
    r'[0-9]+ (\.[0-9]+)? \s* \+ \s* [0-9]+ (\.[0-9]+)? j'
    t.type = 'NUMBER'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t) #Valor de t recebe lexema, linha e coluna
    return t



# A regular expression rule with some action code
def t_NUMBER(t):
    r'[0-9]+ (\.[0-9]+)? (e [+-]? [0-9]+)?'
    t.value = float(t.value),t.lineno,find_column(lexer.lexdata, t) #Valor de t recebe lexema, linha e coluna
    return t

#Pontuacao vem depois que . em floats, token Number, ja foram usados
def t_PTO(t):
    r', | \. | : | ;'
    t.value = t.value,t.lineno,find_column(lexer.lexdata, t) #Valor de t recebe lexema, linha e coluna
    return t



# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("NIN, '%s'," % t.value[0],t.lineno,'\n')
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

#Lê o codigo
filename = sys.argv[1]
file_handle = open(filename, "r")
file_contents = file_handle.read()

#Run the Lexer giving it input
lexer.input(file_contents)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print('Token:',tok.type,'\nLexema:',tok.value[0], '\nLinha:',tok.value[1],'\nColuna:',tok.value[2], '\n')