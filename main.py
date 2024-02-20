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
        aux = []
        while self.source[self.position].isdigit():  
            aux.append(self.source[self.position])
            self.position +=1 
        if aux == []:
            if self.source[self.position] == '+':
                self.next = Token('PLUS', SOMA)
                self.position +=1
            elif self.source[self.position] == '-':
                self.next = Token('MINUS', SUB)
                self.position +=1
        else:
            num = int(''.join(aux))
            self.next = Token(int,num)

        return self.next 
        


class Parser():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    @staticmethod
    def parse_expression(self):
        token_atual = self.tokenizer.select_nex()
        
    
    @staticmethod
    def run(self,code):

        tokenizador= Tokenizer(code,0,None)










def main():

    # Verifica se há argumentos suficientes
    if len(sys.argv) != 2:
        print("Por favor, forneça uma string como argumento.")
        return

    # Obtém o argumento da linha de comando
    minha_string = sys.argv[1]

    if minha_string[0] in symbols or minha_string[-1] in symbols:
        raise "Essa string é uma string invalida por não começar e/ou terminar com números"
    
    atual = None # Define qual operação está sendo executada, começando em None para pegar o primeiro número
    res = 0      # Começando o resultado em zero como sendo o elemento neutro
    LENDO_NUM_INICIAL = 0
    OPERACAO = 1
    LENDO_POS_OP = 2
    ESTADO = LENDO_NUM_INICIAL

    acumulado = []
    num_2 = []
    res = 0
    num = 0

    # 120 + 310 - 20
    for caracter in minha_string:

        if ESTADO == LENDO_NUM_INICIAL:
            if caracter not in symbols:
                acumulado.append(caracter) # 1 2 0 
            else:
                res = int(''.join(acumulado)) # res = 120
                ESTADO = OPERACAO
        
        if ESTADO == LENDO_POS_OP:
            if caracter not in symbols:
                num_2.append(caracter)
            else:
                num = int(''.join(num_2)) # num = 310
                ESTADO = OPERACAO
        
        if ESTADO == OPERACAO:
            if atual is not None:
                if atual == SOMA:
                    res += num
                else:
                    res -= num
                num_2 = []
            if caracter == SOMA:       
                atual = SOMA
            else:
                atual = SUB
            ESTADO = LENDO_POS_OP

    num = int(''.join(num_2))
    if atual == SOMA:
        res += num
    else:
        res -= num
  
    # print(f"para a entrada {minha_string} o resultado obtido foi: {res}")
    print(res)
                
            
if __name__ == "__main__":
    main()
