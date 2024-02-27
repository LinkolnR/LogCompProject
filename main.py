# main.py
import sys

SUB  = 'MINUS'
SOMA = 'PLUS'
MULT = 'MULT'
DIV  = 'DIV'
END = ''

symbols = [SOMA, SUB, MULT, DIV]

# Classes
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
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return self.next
        while self.source[self.position] == ' ':
                    self.position +=1
        aux = []
        while self.source[self.position].isdigit():  
            aux.append(self.source[self.position])
            self.position +=1 
            if self.position >= len(self.source):
                break
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
                
        else:
            num = int(''.join(aux))
            self.next = Token('int',num)
        return self.next 
        


class Parser():
    def __init__(self):
        Parser.tokenizer = None

    tokenizer = None


    @staticmethod
    def parse_term():
        if (Parser.tokenizer.next.type == 'int'):
            res = Parser.tokenizer.next.value                            
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type == 'int':
            raise Exception("string inválida")
        while Parser.tokenizer.next.type in [MULT, DIV]:
            if Parser.tokenizer.next.type == 'int':
                return Parser.tokenizer.next.value
            elif Parser.tokenizer.next.type == MULT:
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == 'int':
                    res *= Parser.tokenizer.next.value
                else:
                    raise "tipo está errado"
            elif Parser.tokenizer.next.type == DIV:
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == 'int':
                    res = res // Parser.tokenizer.next.value
                else:
                    raise "tipo está errado"
            Parser.tokenizer.select_next()

        return res

    
    @staticmethod   
    def parse_expression():
        res = Parser.parse_term()
        while Parser.tokenizer.next.value != END:
            if Parser.tokenizer.next.type == SOMA:
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == 'int':
                    res += Parser.parse_term()

                else:
                    raise "tipo está errado"
            elif Parser.tokenizer.next.type == SUB:
                Parser.tokenizer.select_next()

                if Parser.tokenizer.next.type == 'int':
                    res -= Parser.parse_term()

                else:
                    raise "tipo está errado"       
            else:
                Parser.tokenizer.select_next()            

        return res
        
    
    @staticmethod
    def run(code):
        tokenizador= Tokenizer(code)
        Parser.tokenizer = tokenizador
        resultado = Parser.parse_expression()
        return resultado
    
def main():

    # Verifica se há argumentos suficientes
    if len(sys.argv) != 2:
        print("Por favor, forneça uma string como argumento.")
        return

    #Obtém o argumento da linha de comando
    minha_string = sys.argv[1]
    # minha_string = "1 1"
    

    if minha_string[0] in symbols or minha_string[-1] in symbols:
        raise "Essa string é uma string invalida por não começar e/ou terminar com números"

    res = Parser.run(minha_string)
    print(res)

            
if __name__ == "__main__":
    main()

