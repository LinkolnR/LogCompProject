# main.py
import sys

SOMA = 1
SUB  = 0
symbols = [SOMA, SUB]

# Classes
class Token():

    type : str 
    value : int

    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer():
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next

    def select_next(self):
        if self.position >= len(self.source):
            return Token("EOF", "")
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
                
        else:
            num = int(''.join(aux))
            self.next = Token('int',num)
        return self.next 
        


class Parser():
    def __init__(self):
        self.tokenizer = None
    
    # @staticmethod
    def parse_expression(self):
        res = 0 
        token_atual = self.tokenizer.select_next()
        while token_atual.value  != '':

            if token_atual.type == 'int' or token_atual.value in [SOMA,SUB,'']:
                if (res == 0 and token_atual.type == 'int') :
                    res = token_atual.value
                elif token_atual.value == SOMA:
                    token_atual = self.tokenizer.select_next()
                    if token_atual.value in [SOMA,SUB]:
                        raise "string com entrada invalida"

                    res+= token_atual.value
                elif token_atual.value == SUB:
                    token_atual = self.tokenizer.select_next()
                    if token_atual.value in [SOMA,SUB]:
                        raise "string com entrada invalida"
                    res-= token_atual.value
                else:
                    raise "string com entrada invalida"            
            else:
                raise "O valor do token não é um valor válido"
            token_atual = self.tokenizer.select_next()
        return res
        
    
    # @staticmethod
    def run(self,code):
        tokenizador= Tokenizer(code,0,None)
        self.tokenizer = tokenizador
        resultado = self.parse_expression()
        return resultado
    
def main():

    # Verifica se há argumentos suficientes
    if len(sys.argv) != 2:
        print("Por favor, forneça uma string como argumento.")
        return

    # Obtém o argumento da linha de comando
    minha_string = sys.argv[1]

    if minha_string[0] in symbols or minha_string[-1] in symbols:
        raise "Essa string é uma string invalida por não começar e/ou terminar com números"

    parsing = Parser()
    res = parsing.run(minha_string)
    print(res)

            
if __name__ == "__main__":
    main()
