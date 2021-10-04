from .questao import Questao

class Node():
    def __init__(self, conteudo: str, questoes, node_pai = None):
        self.node_pai = node_pai
        self.conteudo = conteudo
        self.questoes = questoes
        self.pontuacao = None
        self.filhos = []

    def adiciona_pre_requisito(self, node_filho):
        self.filhos.append(node_filho)