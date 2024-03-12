from abc import ABC, abstractmethod 

SUB  = 'MINUS'
SOMA = 'PLUS'
MULT = 'MULT'
DIV  = 'DIV'
PARE = '('
PARD = ')'
END = ''
EOF = 'EOF'

symbols = [SOMA, SUB, MULT, DIV, PARE, PARD, 'int']

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

    def evaluate(self):
        left  = self.children[0]
        right = self.children[1]
        if self.value == SOMA:
            return left.evaluate() + right.evaluate()
        elif self.value == SUB:
            return left.evaluate() - right.evaluate()
        elif self.value == MULT:
            return left.evaluate() * right.evaluate()
        elif self.value == DIV:
            return left.evaluate() // right.evaluate()

class UnOp (Node):  
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self):
        child = self.children[0]
        if self.value == SOMA:
            return +child.evaluate()
        elif self.value == SUB:
            return -child.evaluate()

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        pass



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
        while self.source[self.position] == ' ':
                    if self.position == len(self.source)-1:
                        self.next = Token("EOF", "")
                        return self.next
                    self.position +=1
        aux = []
        # Verificando se é um núm
        while self.source[self.position].isdigit():  
            # enquanto for número adiciona no auxiliar para após transformar em um número
            aux.append(self.source[self.position])
            self.position +=1 
            if self.position >= len(self.source):
                break
        # Se não for número é um símbolo
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
        else:
            num = int(''.join(aux))
            self.next = Token('int',num)
        return self.next 
        
class Parser():
    def __init__(self):
        Parser.tokenizer = None

    tokenizer = None

    @staticmethod
    def parse_expression():
        node1 = Parser.parse_term()
        while Parser.tokenizer.next.type in [SOMA, SUB]:
            if Parser.tokenizer.next.type == SOMA:
                Parser.tokenizer.select_next()
                node2 = Parser.parse_term()
                node1 = BinOp(SOMA, [node1,node2])
            elif Parser.tokenizer.next.type == SUB:
                Parser.tokenizer.select_next()
                node2 = Parser.parse_term()
                node1 = BinOp(SUB, [node1,node2])
        
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

            node = Parser.parse_expression()
            if Parser.tokenizer.next.type != PARD:  
                raise "Erro de sintaxe"
            Parser.tokenizer.select_next()
            return node
        elif Parser.tokenizer.next.type in [SOMA, SUB]:
            if Parser.tokenizer.next.type == SOMA:
                Parser.tokenizer.select_next()
                node = UnOp(SOMA, [Parser.parse_factor()])
            elif Parser.tokenizer.next.type == SUB:
                Parser.tokenizer.select_next()
                node = UnOp(SUB, [Parser.parse_factor()])
            return node
        else:
            raise "Erro de sintaxe"

    
    @staticmethod
    def run(code):
        pre_pros = Pre_pro()
        code_filter = pre_pros.filter(code)
        tokenizador= Tokenizer(code_filter)
        Parser.tokenizer = tokenizador
        
        resultado = Parser.parse_expression()
        teste = resultado.evaluate()
        print( Parser.tokenizer.next.type)
        return teste
    

class Pre_pro():
    def __init__(self):
        pass

    def filter(self, source):
        return source.split('--')[0]
    

