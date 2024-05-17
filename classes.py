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

especial_words = ['print','while','do','end','if','else','then','or','and','read','not','local','function','return',","]

# Classes
class WriteNasm():
    def __init__(self ): 
        pass


    header = """; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data
formatin: db "%d", 0
formatout: db "%d", 10, 0 ; newline, null terminator
scanint: times 4 db 0 ; 32-bit integer = 4 bytes

segment .bss ; variaveis
res RESB 1
extern fflush
extern stdout

section .text
global main ; linux
extern scanf ; linux
extern printf ; linux

; subrotinas if/while
binop_je:
    JE binop_true
    JMP binop_false
binop_jg:
    JG binop_true
    JMP binop_false
binop_jl:
    JL binop_true
    JMP binop_false
binop_false:
    MOV EAX, False
    JMP binop_exit
binop_true:
    MOV EAX, True
binop_exit:
    RET

main:
    PUSH EBP ; guarda o base pointer
    MOV EBP, ESP ; estabelece um novo base pointer\n
"""
    
    body = ""
    
    footer = """
PUSH DWORD [stdout]
CALL fflush
ADD ESP, 4
MOV ESP, EBP
POP EBP
MOV EAX, 1
XOR EBX, EBX
INT 0x80
    """
    

    @staticmethod
    def write_header(filename):
        with open(filename, 'w') as file:
            file.write(WriteNasm.header)
    
    @staticmethod
    def write_body(filename):
        with open(filename, 'a') as file:
            file.write(WriteNasm.body)
    
    @staticmethod
    def write_footer(filename):
        with open(filename, 'a') as file:
            file.write(WriteNasm.footer)

    @staticmethod
    def write_nasm():
        WriteNasm.write_header()
        WriteNasm.write_body()
        WriteNasm.write_footer()




from abc import ABCMeta

class Node(metaclass=ABCMeta):
        next_id = 0
        def __init__(self, value, children): 
            self.value = value
            self.children = children
            self.writeNasm = WriteNasm
            self.id = Node.next_id
            Node.next_id+=1


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
            self.writeNasm.body += "ADD EAX, EBX\n"
            return (left + right,'int')
        elif self.value == SUB:
            self.writeNasm.body += "SUB EAX, EBX\n"
            return (left - right,'int')
        elif self.value == MULT:
            self.writeNasm.body += "IMUL EBX\n"
            return (left * right,'int')
        elif self.value == DIV:
            self.writeNasm.body += "IDIV EBX\n"
            return (left // right,'int')
        elif self.value == '==':

            left_string = left.evaluate(symbol_table)[0]
            right_string = right.evaluate(symbol_table)[0]
            if type(left_string) == bool:
                if left_string:
                    left_string = 1
                else:
                    left = 0        
            if type(right) == bool:
                if right:
                    right = 1
                else:
                    right = 0
            print(left,right)
            if type(left) != type(right):
                    raise "não é possivel comparar tipos diferentes"
            self.writeNasm.body += "CMP EAX, EBX\n"
            self.writeNasm.body += "CALL binop_je\n"
            return (left == right,'bool')
        elif self.value == '>':
            self.writeNasm.body += "CMP EAX, EBX\n"
            self.writeNasm.body += "CALL binop_jg\n"
            return (left > right,'bool')
        elif self.value == '<':
            self.writeNasm.body += "CMP EAX, EBX\n"
            self.writeNasm.body += "CALL binop_jl\n"
            return (left < right,'bool')
        elif self.value == 'or':
            self.writeNasm.body += "OR EAX, EBX\n"
            return (left or right,'int')
        elif self.value == 'and':
            self.writeNasm.body += "AND EAX, EBX\n"
            return (left and right,'int')
        elif self.value == '..':
            # left_string = left.evaluate(symbol_table)[0]
            # right_string = right.evaluate(symbol_table)[0]
            if type(left) == bool:
                if left:
                    left = 1
                else:
                    left = 0        
            if type(right) == bool:
                if right:
                    right = 1
                else:
                    right_string = 0
            return (str(left_string) + str(right_string),'concat')
        
class UnOp (Node):  
    def __init__(self, value, children):
        super().__init__(value, children)
        
    def evaluate(self,symbol_table):
        child = self.children[0]
        valor = child.evaluate(symbol_table)[0]
        if self.value == SOMA:
            self.writeNasm.body += f"MOV EAX, {valor}\n"
            return (+valor, 'int')
        elif self.value == SUB:
            self.writeNasm.body += f"NEG EAX\n"
            return (-valor, 'int')
        elif self.value == 'not':
            self.writeNasm.body += f"MOV EAX, {not valor}\n"
            return (not valor, 'int')

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self,symbol_table):
        print('entrou aqui 1')
        print(f"MOV EAX, {self.value}\n")
        self.writeNasm.body += f"MOV EAX, {self.value}\n"
        
        return (self.value, 'int')

class StrVal(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self,symbol_table):
        return (self.value, 'str')

class NoOp(Node):
    def __init__(self, value = None):
        self.value = value
    
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
        self.writeNasm.body += f"PUSH EAX\n"
        self.writeNasm.body += f"PUSH formatout\n"
        self.writeNasm.body += f"CALL printf\n"
        self.writeNasm.body += f"ADD ESP, 8\n"

        
        print(string)

class AssingNode(Node):
    def __init__(self, children):
        super().__init__( value= None ,children = children)

    def evaluate(self, symbol_table):
        left  = self.children[0]
        right = self.children[1]
        symbol_table.set(left.value,right.evaluate(symbol_table))

class Identifier(Node):
    def __init__(self, value):
       super().__init__(value, [])

    def evaluate(self, symbol_table):
        position = symbol_table.get(self.value)[2]
        self.writeNasm.body += f"MOV EAX, [EBP-{position}]\n"
        return (symbol_table.get(self.value)[0], 'identifier')

class Block(Node):
    def __init__(self, children):
        super().__init__(value= None , children = children)

    def add_statement(self, statement: Node):
        self.children.append(statement)

    def evaluate(self,symbol_table):    
        print('blockoipasdkjnsajkndsajk')
        print(self.children)
        for child in self.children:
            if (child.value == "return"):
                print('evaluate do return:')
                auxiliar = child.evaluate(symbol_table)
                print(auxiliar)
                return auxiliar
            child.evaluate(symbol_table)


class SymbolTable():
    def __init__(self):
        self.table = {}
        self.desloc = 4


    def set(self, key, value):

        if key in self.table.keys():
            self.table[key] = (value[0],value[1])
        else:
            raise "Variável não declarada"
    
    def create(self,key):
        if key not in self.table.keys():
            self.table[key] = None
        else:
            raise "Variável já declarada"

    def get(self, key):
        return self.table[key]

class FuncTable():
    table = {}
    @staticmethod
    def set( key, value ):
        if key.value in FuncTable.table.keys():
            FuncTable.table[key.value] = value
        else:
            raise "Funcao não declarada"
    @staticmethod
    def create( key ):
        if key.value not in FuncTable.table.keys():
            FuncTable.table[key.value] = None
        else:
            raise "Funcao já declarada"
    @staticmethod
    def get( key ):
        return FuncTable.table[key]

class WhileNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,symbol_table):
        self.writeNasm.body += f"LOOP_{self.id}:\n"
        self.children[0].evaluate(symbol_table)
        #while self.children[0].evaluate(symbol_table)[0]:
        self.writeNasm.body += f"CMP EAX, False\n"
        self.writeNasm.body += f"JE EXIT_{self.id}\n"
        self.children[1].evaluate(symbol_table)
        self.writeNasm.body += f"JMP LOOP_{self.id}\n"
        self.writeNasm.body += f"EXIT_{self.id}:\n"



class IfNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,symbol_table):
        if self.children[0].evaluate(symbol_table)[0]:
            self.writeNasm.body += f"IF_BLOCK{self.id}:\n"
            self.writeNasm.body += f"CMP EAX, False\n"
            self.writeNasm.body += f"JMP ELSE_BLOCK{self.id}\n"
            self.children[1].evaluate(symbol_table)
            self.writeNasm.body += f"JMP EXIT_IF_BLOCK{self.id}\n"
            self.writeNasm.body += f"ELSE_BLOCK{self.id}:\n"
        elif len(self.children) == 3:
            self.children[2].evaluate(symbol_table)

class VarDecNode(Node):
    def __init__(self,children):
        super().__init__(value = None, children = children)

    def evaluate(self,symbol_table):
        if len(self.children) == 1:
            symbol_table.create(self.children[0].value)
        else:
            symbol_table.create(self.children[0].value)
            symbol_table.set(self.children[0].value,self.children[1].evaluate(symbol_table))

class ReadNode(Node):
    def __init__(self):
        super().__init__(None, None)


    def evaluate(self,symbol_table):
        input_ = int(input())
        self.writeNasm.body += f"PUSH scanint\n"
        self.writeNasm.body += f"PUSH formatin\n"
        self.writeNasm.body += f"CALL scanf\n"
        self.writeNasm.body += f"ADD ESP, 8\n"
        self.writeNasm.body += f"MOV EAX, DWORD [scanint]\n"
        return (input_, 'int')

class FunctionDec(Node):
    def __init__(self, children):
        super().__init__(value = None, children = children)

    def evaluate(self,symbol_table):
        FuncTable.create(self.children[0])
        FuncTable.set(self.children[0],self)

class FunctionCall(Node):
    def __init__(self, value ,children):
        super().__init__(value = value, children = children)

    def evaluate(self,symbol_table):
        table_local = SymbolTable()
        func = FuncTable.get(self.value)
        print(func.children[2].children)
        args = func.children[1:-1]
        if len(args) != len(self.children):
            raise "Número de argumentos incorreto"    
        for i in range(len(args)):
            argumento = args[i].children[0].value
            valor_arg = self.children[i].children[0].evaluate(symbol_table)
            table_local.create(argumento)
            table_local.set(args[i].children[0].value,valor_arg)
        block = func.children[-1]
        print('*'*80)
        print(block.children)
        block_return = block.evaluate(table_local)
        print("passando aqui uma vez", block_return)
        return block_return


class ReturnNode(Node):
    def __init__(self, children):
        super().__init__(value = 'return', children = children)

    def evaluate(self,symbol_table):
        print('entrou no return')
        return self.children[0].evaluate(symbol_table)



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
                while (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_" or self.source[self.position] == ","):
                    if self.source[self.position] == "," and len(aux) > 0:
                        break
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
            elif Parser.tokenizer.next.type == PARE:
                Parser.tokenizer.select_next()
                args = []
                while Parser.tokenizer.next.type != PARD:

                    args.append(VarDecNode([Parser.parse_bool_expression()]))
                    if Parser.tokenizer.next.type == ',':
                        Parser.tokenizer.select_next()
                Parser.tokenizer.select_next()
                return FunctionCall(identifier.value,args)

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
                    assign_node = VarDecNode([identifier, expression])
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
        
        elif Parser.tokenizer.next.type == 'function':
            Parser.tokenizer.select_next()
            
            if Parser.tokenizer.next.type == IDENTIFIER:
                identifier = Identifier(Parser.tokenizer.next.value)
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == PARE:
                    Parser.tokenizer.select_next()
                else:
                    raise "faltando parenteses"
                args = []
                while Parser.tokenizer.next.type != PARD:
                    args.append(VarDecNode([Identifier(Parser.tokenizer.next.value)]))
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == ',':
                        Parser.tokenizer.select_next()
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type != 'QUEBRA':
                    raise "Erro de sintaxe - falta a quebra de linha"
                block = Block(children=[])
                while Parser.tokenizer.next.type != 'end':
                    node = Parser.parse_statement()
                    block.children.append(node)
                Parser.tokenizer.select_next()
                return FunctionDec([identifier]+args+[block])
            else:
                raise "Faltou o nome da função"
        elif Parser.tokenizer.next.type == 'return':
            Parser.tokenizer.select_next()
            expression = Parser.parse_bool_expression()
            return ReturnNode([expression])
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
            if Parser.tokenizer.next.type == PARE:
                Parser.tokenizer.select_next()
                args = []
                while Parser.tokenizer.next.type != PARD:
                    args.append(VarDecNode([Parser.parse_bool_expression()]))
                    if Parser.tokenizer.next.type == ',':
                        Parser.tokenizer.select_next()
                Parser.tokenizer.select_next()
                return FunctionCall(identifier.value,args)
            else:    
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
    

