import time
import random
import tkinter as tk
from tkinter import ttk
import threading

class Sensores :
    def __init__(self) :
        self.posicao = 0
        self.temperatura = 25.0
        self.umidade = 50.0
        self.movimento = False
        
    def atualizar(self):
        self.atualizar_movimento()
        self.atualizar_temperatura()
        self.atualizar_umidade()

    def atualizar_movimento(self) :
        self.movimento = random.random() < 0.3
        self.posicao = random.randint(1, 100) if self.movimento else 0

    def atualizar_temperatura(self) :
        base = 22 + (self.posicao % 5) if self.movimento else 20
        self.temperatura = round(base + random.uniform(-0.5, 0.5), 1)

    def atualizar_umidade(self) :
        base = 45 + (self.posicao % 10) if self.movimento else 50
        self.umidade = round(base + random.uniform(-1, 1), 1)

class Atuadores :
    def __init__(self):
        self.luzes = False
        self.ar_condicionado = False
        self.modo_automatico = True
        
    def atualizar(self, sensores: Sensores):
        if self.modo_automatico:
            self.luzes = sensores.movimento
            self.ar_condicionado = sensores.temperatura > 25
            
class CasaInteligenteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Casa Inteligente")

        self.sensores = Sensores()
        self.atuadores = Atuadores()

        self.temp_label = ttk.Label(root, text="Temperatura: -- °C")
        self.temp_label.pack(pady=5)

        self.umid_label = ttk.Label(root, text="Umidade: -- %")
        self.umid_label.pack(pady=5)

        self.mov_label = ttk.Label(root, text="Movimento: --")
        self.mov_label.pack(pady=5)

        self.var_luz = tk.BooleanVar()
        self.check_luz = ttk.Checkbutton(root, text="Luz da Sala", variable=self.var_luz, command=self.toggle_luz)
        self.check_luz.pack(pady=5)

        self.var_ar = tk.BooleanVar()
        self.check_ar = ttk.Checkbutton(root, text="Ar-Condicionado", variable=self.var_ar, command=self.toggle_ar)
        self.check_ar.pack(pady=5)

        #modo automático
        self.var_auto = tk.BooleanVar(value=True)
        self.check_auto = ttk.Checkbutton(root, text="Modo Automático", variable=self.var_auto, command=self.mudar_modo)
        self.check_auto.pack(pady=10)

        #thread de atualização
        self.atualizando = True
        self.thread = threading.Thread(target=self.atualizar_interface)
        self.thread.daemon = True
        self.thread.start()

    def mudar_modo(self):
        self.atuadores.modo_automatico = self.var_auto.get()

    def toggle_luz(self):
        if not self.atuadores.modo_automatico:
            self.atuadores.luzes = self.var_luz.get()

    def toggle_ar(self):
        if not self.atuadores.modo_automatico:
            self.atuadores.ar_condicionado = self.var_ar.get()

    def atualizar_interface(self):
        while self.atualizando:
            self.sensores.atualizar()
            self.atuadores.atualizar(self.sensores)

            self.temp_label.config(text=f"Temperatura: {self.sensores.temperatura:.1f} °C")
            self.umid_label.config(text=f"Umidade: {self.sensores.umidade:.1f} %")
            self.mov_label.config(text=f"Movimento: {'Sim' if self.sensores.movimento else 'Não'}")

            if self.atuadores.modo_automatico:
                self.var_luz.set(self.atuadores.luzes)
                self.var_ar.set(self.atuadores.ar_condicionado)

            time.sleep(1.5)


if __name__ == "__main__":
    root = tk.Tk()
    app = CasaInteligenteApp(root)
    root.mainloop()
