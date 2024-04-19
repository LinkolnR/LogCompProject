from abc import ABC, abstractmethod 

SUB  = 'MINUS'
SOMA = 'PLUS'
MULT = 'MULT'
DIV  = 'DIV'
PARE = '('
PARD = ')'
END = ''
EOF = 'EOF'
ASS = '='
PRINT = 'print'
QUEBRA = '\n'
IDENTIFIER = 'identifier'
ATRIBUICAO = 'atribuicao'



symbols = [SOMA, SUB, MULT, DIV, PARE, PARD, 'int','=','==','>','<']
# symbols_tokens = ["+","-","*","/","=","(",")"]

especial_words = ['print','while','do','end','if','else','then','or','and','read','not','local']


# Classes
from abc import ABCMeta

class Node(metaclass=ABCMeta):
        def __init__(self, value, children): 
            self.value = value
            self.children = children

        @abstractmethod
        def evaluate(self):
            pass

class BinOp (Node):
    def __init__(self, value, children):  
        super().__init__(value, children)

    def evaluate(self,symbol_table):
        left  = self.children[0]
        right = self.children[1]
        if self.value == SOMA:
            return (left.evaluate(symbol_table)[0] + right.evaluate(symbol_table)[0],'int')
        elif self.value == SUB:
            return (left.evaluate(symbol_table)[0] - right.evaluate(symbol_table)[0],'int')
        elif self.value == MULT:
            return (left.evaluate(symbol_table)[0] * right.evaluate(symbol_table)[0],'int')
        elif self.value == DIV:
            return (left.evaluate(symbol_table)[0] // right.evaluate(symbol_table)[0],'int')
        elif self.value == '==':
            return (left.evaluate(symbol_table)[0] == right.evaluate(symbol_table)[0],'bool')
        elif self.value == '>':
            return (left.evaluate(symbol_table)[0] > right.evaluate(symbol_table)[0],'bool')
        elif self.value == '<':
            return (left.evaluate(symbol_table)[0] < right.evaluate(symbol_table)[0],'bool')
        elif self.value == 'or':
            return (left.evaluate(symbol_table)[0] or right.evaluate(symbol_table)[0],'int')
        elif self.value == 'and':
            return (left.evaluate(symbol_table)[0] and right.evaluate(symbol_table)[0],'int')
        elif self.value == '..':
            left_string = left.evaluate(symbol_table)[0]
            right_string = right.evaluate(symbol_table)[0]
            if type(left_string) != str:
                if left_string:
                    left_string = 1
                else:
                    left_string = 0        
            if type(right_string) != str:
                if right_string:
                    right_string = 1
                else:
                    right_string = 0
            return (str(left_string) + str(right_string),'concat')
        
        

class UnOp (Node):  
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self,symbol_table):
        child = self.children[0]
        if self.value == SOMA:
            return (+child.evaluate(symbol_table)[0], 'int')
        elif self.value == SUB:
            return (-child.evaluate(symbol_table)[0], 'int')
        elif self.value == 'not':
            return (not child.evaluate(symbol_table)[0], 'int')

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self,symbol_table):
        return (self.value, 'int')

class StrVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self,symbol_table):
        return (self.value, 'str')


class NoOp(Node):
    def __init__(self):
        pass
    
    def evaluate(self,symbol_table):
        pass

class PrintNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,symbol_table):
        string = self.children[0].evaluate(symbol_table)[0]
        if type(string) == bool:
            if string:
                string = 1
            else:
                string = 0
        print(string)

class AssingNode(Node):
    def __init__(self, children):
        super().__init__( value= None ,children = children)

    def evaluate(self, symbol_table):
        # popular a symbol table
        left  = self.children[0]
        right = self.children[1]
        # symbol_table.create(left)
        symbol_table.set(left,right.evaluate(symbol_table))


class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbol_table):
        return (symbol_table.get(self.value)[0], 'identifier')

class Block(Node):
    def __init__(self, children):
        super().__init__(value= None , children = children)

    def add_statement(self, statement: Node):
        self.children.append(statement)

    def evaluate(self,symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)

class SymbolTable():
    def __init__(self):
        self.table = {}

    def set(self, key, value):
        self.table[key.value] = (value[0],value[1])
    
    def create(self,key):
        if key.value not in self.table.keys():
            self.table[key.value] = None

    def get(self, key):
        return self.table[key]




class WhileNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,symbol_table):
        while self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)

class IfNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,symbol_table):
        if self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].evaluate(symbol_table)


class VarDecNode(Node):
    def __init__(self,children):
        super().__init__(value = None, children = children)

    def evaluate(self,symbol_table):
        if len(self.children) == 1:
            symbol_table.create(self.children[0])
        else:
            symbol_table.set(self.children[0],self.children[1].evaluate(symbol_table))

class ReadNode(Node):
    def __init__(self):
        pass

    def evaluate(self,symbol_table):
        input_ = int(input())
        return (input_, 'int')




# Tokenizer

class Token():

    type : str 
    value : int

    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer():
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = self.select_next()

    # @staticmethod
    def select_next(self):

        # Criando o token de final da string
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return self.next
        # Ignorando espaços
        while self.source[self.position] == ' ' or self.source[self.position] == '\t':
                    if self.position == len(self.source)-1:
                        self.next = Token("EOF", "")
                        return self.next
                    self.position +=1
        aux = []
        # Verificando se é um núm
        if self.source[self.position].isdigit():
            while self.source[self.position].isdigit():  
                # enquanto for número adiciona no auxiliar para após transformar em um número
                aux.append(self.source[self.position])
                self.position +=1 
                if self.position >= len(self.source):
                    break
            num = int(''.join(aux))
            self.next = Token('int',num)
            return self.next 

            
    
        if aux == []:
            if self.source[self.position] == '+':
                self.next = Token('PLUS', SOMA)
                self.position +=1
            elif self.source[self.position] == '-':
                self.next = Token('MINUS', SUB)
                self.position +=1
            elif self.source[self.position] == '*':
                self.next = Token('MULT', MULT)
                self.position +=1
            elif self.source[self.position] == '/':
                self.next = Token('DIV', DIV)
                self.position +=1
            elif self.source[self.position] == '(':
                self.next = Token('(', PARE)
                self.position +=1
            elif self.source[self.position] == ')':
                self.next = Token(')', PARD)
                self.position +=1
            elif self.source[self.position] == '\n':
                self.next = Token('QUEBRA', QUEBRA)
                self.position +=1
            elif self.source[self.position] == '=':
                self.position +=1
                if self.source[self.position] == '=':
                    self.next = Token('==', '==')
                    self.position +=1
                else:    
                    self.next = Token(ATRIBUICAO,'=')
            elif self.source[self.position] == '>':
                self.next = Token('>', '>')
                self.position +=1
            elif self.source[self.position] == '<':
                self.next = Token('<', '<')
                self.position +=1
            elif self.source[self.position] == '.':
                self.position +=1
                if self.source[self.position] == '.':
                    self.next = Token('..', '..')
                    self.position +=1
                else:
                    raise "concatenacao incompleta"
            elif self.source[self.position] == '"':
                self.position +=1
                while self.source[self.position] != '"':
                    aux.append(self.source[self.position])
                    self.position +=1
                self.position +=1   
                string = ''.join(aux)
                self.next = Token('string',string )
            else:
                while (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):
                    aux.append(self.source[self.position])
                    self.position = self.position + 1
                    if (self.position == (len(self.source))):
                        self.position = self.position - 1
                        break
                if aux == []:
                    raise "Erro de sintaxe - não é um token válido"
                palavra = ''.join(aux)
                if palavra in especial_words:
                    self.next = Token(palavra, palavra)
                    return self.next
                self.next = Token('identifier', ''.join(aux))
                return self.next

            
        return self.next 
        
class Parser():
    def __init__(self):
        Parser.tokenizer = None
        Parser.block = None

    tokenizer = None

    @staticmethod
    def parse_block(): 
        while (Parser.tokenizer.next.type != "EOF"):
            statement = Parser.parse_statement()
            Parser.block.add_statement(statement)
        Parser.tokenizer.select_next()
        return Parser.block

    @staticmethod
    def parse_statement():
        if Parser.tokenizer.next.type == IDENTIFIER:
            identifier = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == ATRIBUICAO:
                Parser.tokenizer.select_next()
                expression = Parser.parse_bool_expression()
                assign_node = AssingNode([identifier, expression])
                return assign_node
            else:
                raise "Erro de sintaxe - falta o simbolo de atribuição ou identificador deveria ser um nome especial/reservado"
        elif Parser.tokenizer.next.type == 'local':
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == IDENTIFIER:
                identifier = Identifier(Parser.tokenizer.next.value)
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == ATRIBUICAO:
                    Parser.tokenizer.select_next()
                    expression = Parser.parse_bool_expression()
                    assign_node = AssingNode([identifier, expression])
                    return assign_node
                elif Parser.tokenizer.next.type == 'QUEBRA':
                    assign_node = VarDecNode([identifier])
                    return assign_node
                else:
                    raise 'SINTAXE NAO ACEITA'
        elif Parser.tokenizer.next.type == PRINT:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == PARE:
                Parser.tokenizer.select_next()
            expression = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type != PARD:
                raise "Erro de sintaxe - falta o parenteses de fechada"
            Parser.tokenizer.select_next()
            return PrintNode(PRINT, [expression])
        elif Parser.tokenizer.next.type == 'QUEBRA':
            Parser.tokenizer.select_next()
            return NoOp()
        elif Parser.tokenizer.next.type == 'while':
            Parser.tokenizer.select_next()
            condicional = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type != 'do':
                raise "Erro de sintaxe - falta o do"
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != 'QUEBRA':
                raise "Erro de sintaxe - falta a quebra de linha"
            while_block = Block(children=[])
            while Parser.tokenizer.next.type != 'end':
                node = Parser.parse_statement()
                while_block.children.append(node)
            Parser.tokenizer.select_next()
            return WhileNode('while', [condicional, while_block])
        
        elif Parser.tokenizer.next.type == 'if':
            Parser.tokenizer.select_next()
            condicional = Parser.parse_bool_expression()
            # Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != 'then':
                raise "Erro de sintaxe - falta o then"
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != 'QUEBRA':
                raise "Erro de sintaxe - falta a quebra de linha"
            if_block = Block(children=[])
            Parser.tokenizer.select_next()

            while Parser.tokenizer.next.type not in ['end','else']:
                node = Parser.parse_statement()
                if_block.children.append(node)

            if Parser.tokenizer.next.type == 'else':
                Parser.tokenizer.select_next()
                else_block = Block(children=[])
                while Parser.tokenizer.next.type != 'end':
                    node = Parser.parse_statement()
                    else_block.children.append(node)
                Parser.tokenizer.select_next()
                return IfNode('if', [condicional, if_block, else_block])
            elif Parser.tokenizer.next.type != 'end':
                raise "Erro de sintaxe - falta o end de fechamento do if"
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type not in ['QUEBRA','EOF']:
                raise "Erro de sintaxe - não pode ter statement após o end do if"
            return IfNode('if', [condicional, if_block])
        else:
            raise "Erro de sintaxe - parenteses sem fechar ou falta algum termo"
    @staticmethod
    def parse_bool_expression():
        node1 = Parser.parse_bool_term()
        while Parser.tokenizer.next.type in ['or']:
            if Parser.tokenizer.next.type == 'or':
                Parser.tokenizer.select_next()
                node2 = Parser.parse_bool_term()
                node1 = BinOp('or', [node1,node2])  
        return node1

    @staticmethod
    def parse_bool_term():
        node1 = Parser.parse_relational_expression()
        while Parser.tokenizer.next.type in ['and']:
            if Parser.tokenizer.next.type == 'and':
                Parser.tokenizer.select_next()
                node2 = Parser.parse_relational_expression()
                node1 = BinOp('and', [node1,node2])  
        return node1



    @staticmethod
    def parse_relational_expression():
        node1 = Parser.parse_expression()
        while Parser.tokenizer.next.type in ['==','<','>']:
            if Parser.tokenizer.next.type == '==':
                Parser.tokenizer.select_next()
                node2 = Parser.parse_expression()
                node1 = BinOp('==', [node1 ,node2])
            elif Parser.tokenizer.next.type == '<':
                Parser.tokenizer.select_next()
                node2 = Parser.parse_expression()
                node1 = BinOp('<',  [node1, node2])
            elif Parser.tokenizer.next.type == '>':
                Parser.tokenizer.select_next()
                node2 = Parser.parse_expression()
                node1 = BinOp('>',  [node1, node2])
            elif Parser.tokenizer.next.type in symbols:
                node1 = UnOp(Parser.tokenizer.next.type, [Parser.parse_factor()])
            else:
                raise "Erro de sintaxe"
        return node1

    @staticmethod
    def parse_expression():
        node1 = Parser.parse_term()
        while Parser.tokenizer.next.type in [SOMA, SUB,'..']:
            if Parser.tokenizer.next.type == SOMA:
                Parser.tokenizer.select_next()
                node2 = Parser.parse_term()
                node1 = BinOp(SOMA, [node1,node2])
            elif Parser.tokenizer.next.type == SUB:
                Parser.tokenizer.select_next()
                node2 = Parser.parse_term()
                node1 = BinOp(SUB, [node1,node2])
            elif Parser.tokenizer.next.type == '..':
                Parser.tokenizer.select_next()
                node2 = Parser.parse_term()
                node1 = BinOp('..', [node1,node2])
        
        return node1
    
    @staticmethod   
    def parse_term():
        node1 = Parser.parse_factor()
        while Parser.tokenizer.next.type in [DIV,MULT]:
            if Parser.tokenizer.next.type == MULT:
                Parser.tokenizer.select_next()
                node2 = Parser.parse_factor()
                node1 = BinOp(MULT, [node1 ,node2])
            elif Parser.tokenizer.next.type == DIV:
                Parser.tokenizer.select_next()
                node2 = Parser.parse_factor()
                node1 = BinOp(DIV,  [node1, node2])
            elif Parser.tokenizer.next.type in symbols:
                node1 = UnOp(Parser.tokenizer.next.type, [Parser.parse_factor()])
            else:
                raise "Erro de sintaxe"
        return node1
        
    @staticmethod
    def parse_factor():

        if Parser.tokenizer.next.type == 'int':
            inteiro = IntVal(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            return inteiro
        elif Parser.tokenizer.next.type == PARE:
            Parser.tokenizer.select_next()
            node = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type != PARD:  
                raise "Erro de sintaxe"
            Parser.tokenizer.select_next()
            return node
        elif Parser.tokenizer.next.type == IDENTIFIER:
            identifier = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            return identifier
        elif Parser.tokenizer.next.type in [SOMA, SUB,'not']:
            if Parser.tokenizer.next.type == SOMA:
                Parser.tokenizer.select_next()
                node = UnOp(SOMA, [Parser.parse_factor()])
            elif Parser.tokenizer.next.type == SUB:
                Parser.tokenizer.select_next()
                node = UnOp(SUB, [Parser.parse_factor()])
            elif Parser.tokenizer.next.type == 'not':
                Parser.tokenizer.select_next()
                node = UnOp('not', [Parser.parse_factor()])
            return node
        elif Parser.tokenizer.next.type in ['read']:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == PARE:
                Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != PARD:
                raise "Erro de sintaxe"
            Parser.tokenizer.select_next()
            return ReadNode()
        elif Parser.tokenizer.next.type == 'string':
            string = StrVal(Parser.tokenizer.next.value)
            Parser.tokenizer.select_next()
            return string
        else:
            raise "Erro de sintaxe"

    
    @staticmethod
    def run(code):
        pre_pros = Pre_pro()
        code_filter = pre_pros.filter(code)
        tokenizador= Tokenizer(code_filter)
        Parser.tokenizer = tokenizador
        Parser.block = Block([])
        resultado = Parser.parse_block()
        teste = Parser.block.evaluate(symbol_table = SymbolTable())
        return teste
    

class Pre_pro():
    def __init__(self):
        pass

    def filter(self, source):
        lista = source.split('\n')
        for i in range(0,len(lista)-1):
            if '--' in lista[i]:
                lista[i] = lista[i].split('--')[0]
        completo = '\n'.join(lista)
        return completo
    

