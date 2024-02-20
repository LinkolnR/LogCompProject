class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer():
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next

    def select_next(self):

        return Token(self.source[self.position])
        self.position+=1
        self.next = self.source[self.position]
        


class Parser():
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    @staticmethod
    def parse_expression(self):
        token_atual = self.tokenizer.select_nex()
        pass
    
    @staticmethod
    def run(self,code):
        tokenizador= Tokenizer(code,)

