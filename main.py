# main.py
import sys
from classes import *


def main():
    
    teste = False

    if not teste:
        # Verifica se há argumentos suficientes
        if len(sys.argv) != 2:
            print("Por favor, forneça uma string como argumento.")
            return

        # #Obtém o argumento da linha de comando
        arquivo = sys.argv[1]
        # # Ler um arquivo com uma linha de   
        with open(arquivo, 'r') as file:
            minha_string = file.read()
    else:
        minha_string = "x = 15 + 12 \n y = 16\n z = x + y\n print(z)"
        
    res = Parser.run(minha_string)
    if (Parser.tokenizer.next.type == "EOF"):
            # print(res)
            return res
    else:
        raise "Erro de sintaxe - Não acabou com EOF"

            
if __name__ == "__main__":
    main()
