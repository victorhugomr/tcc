class Questao():
    def __init__(self, conteudo: str, pergunta: str, alternativa: str, gabarito: str):
        self.conteudo = conteudo
        self.pergunta = pergunta
        self.alternativa = alternativa
        self.gabarito = gabarito
        self.resultado = None
    
    def responde_questao(self, resposta: str):
        if resposta == self.gabarito:
            resultado = 1
        else:
            resultado = 0