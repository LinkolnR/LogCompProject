# main.py
import sys

SUB  = 'SUB'
SOMA = 'SOMA'
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
        self.tokenizer = None
    
    # @staticmethod
    def parse_expression(self):
        res = 0 
        expression_parts = []

        token_atual = self.tokenizer.select_next()
        while token_atual.value  != END:

            if token_atual.type == 'int' or token_atual.value in [SOMA,SUB,END,MULT,DIV]:
                # expression_parts.append(token_atual.value)            
                if (res == 0 and token_atual.type == 'int') :
                    expression_parts.append(token_atual.value) 
                    # res = token_atual.value
                elif token_atual.value in [SOMA,SUB,MULT,DIV]:
                    expression_parts.append(token_atual.value) 
                    token_atual = self.tokenizer.select_next()
                    if token_atual.value in [SOMA,SUB]:
                        raise "string com entrada invalida"
                    expression_parts.append(token_atual.value) 
                    
                    # res+= token_atual.value
                # elif token_atual.value == SUB:
                #     expression_parts.append(token_atual.value) 
                #     token_atual = self.tokenizer.select_next()
                #     if token_atual.value in [SOMA,SUB]:
                #         raise "string com entrada invalida"
                #     expression_parts.append(token_atual.value) 
                #     # res-= token_atual.value
                else:
                    raise "string com entrada invalida" 
                # expression_parts.append(token_atual.value)           
            else:
                raise "O valor do token não é um valor válido"
            token_atual = self.tokenizer.select_next()
        
        i = 0 
        j = 0
        aux = 0

        while len(expression_parts) != 1:
            # print(i)
            # print(expression_parts)
            if MULT in expression_parts or DIV in expression_parts:
                if (expression_parts[i] == MULT):
                    aux = expression_parts[i-1]*expression_parts[i+1]
                    expression_parts.pop(i+1)
                    expression_parts.pop(i)
                    expression_parts[i-1] = aux
                    i-=1

                elif (expression_parts[i] == DIV):
                    aux = expression_parts[i-1]/expression_parts[i+1]
                    expression_parts.pop(i+1)
                    expression_parts.pop(i)
                    expression_parts[i-1] = aux
                    i-=1
            else:
                if (expression_parts[j] == SOMA):
                    aux = expression_parts[j-1]+expression_parts[j+1]
                    expression_parts.pop(j+1)
                    expression_parts.pop(j)
                    expression_parts[j-1] = aux
                    j-=1
                elif (expression_parts[j] == SUB):
                    aux = expression_parts[j-1]-expression_parts[j+1]
                    expression_parts.pop(j+1)
                    expression_parts.pop(j)
                    expression_parts[j-1] = aux
                    j-=1
                j+=1
            i+=1

                

        res = int(expression_parts[0])

                         
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

    #Obtém o argumento da linha de comando
    minha_string = sys.argv[1]

    if minha_string[0] in symbols or minha_string[-1] in symbols:
        raise "Essa string é uma string invalida por não começar e/ou terminar com números"

    parsing = Parser()
    res = parsing.run(minha_string)
    print(res)

            
if __name__ == "__main__":
    main()



"1/1   +  2 *  1 -3+4/2"