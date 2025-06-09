import time
import random
import tkinter
import threading

class Sensores :
    def __init__(self) :
        self.posicao = 0
        self.temperatura = 25
        self.umidade = 50
        self.movimento = False

    def atualizar_movimento(self) :
        self.movimento = random.random() < 0.3
        if self.movimento :
            self.posicao = random.randint(1, 100) # por ex: sala = 1–33, quarto = 34–66...
        else :
            self.posicao = 0

    def atualizar_temperatura(self) :
        if self.movimento:
            self.temperatura = 22 + (self.posicao % 5) + random.uniform(-0.5, 0.5)
        else:
            self.temperatura = 20 + random.uniform(-0.5, 0.5)

    def atualizar_umidade(self) :
        if self.movimento:
            self.umidade = 45 + (self.posicao % 10) + random.uniform(-1, 1)
        else:
            self.umidade = 50 + random.uniform(-1, 1)

class Atuadores :
    def __init__(self, x, y, z) :
        self.x = x
        self.y = y
        self.z = z
