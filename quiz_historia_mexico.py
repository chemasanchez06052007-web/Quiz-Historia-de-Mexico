import tkinter as tk
from tkinter import messagebox
import csv
import random
TOTAL_PREGUNTAS = 5
VIDAS = 3
PUNTOS = 10
COLOR_FONDO = "white"
#backend (lógica, sin Tkinter)
class Pregunta:
    def __init__(self, texto, opciones, correcta):
        self.texto = texto
        self.opciones = opciones
        self.correcta = correcta
    def es_correcta(self, respuesta):
        return respuesta == self.correcta
def leer_preguntas():
    """Lee TODAS las preguntas del CSV. Puede lanzar FileNotFoundError."""
    preguntas = []
    with open("preguntas.csv", "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            if len(fila) == 6 and fila[0] != "pregunta":
                opciones = [fila[1], fila[2], fila[3], fila[4]]
                preguntas.append(Pregunta(fila[0], opciones, fila[5]))
    return preguntas
class Juego:
    def __init__(self, preguntas):
        self.preguntas = random.sample(preguntas, TOTAL_PREGUNTAS)
        self.indice = 0
        self.vidas = VIDAS
        self.puntaje = 0
    def pregunta_actual(self):
        return self.preguntas[self.indice]
    def responder(self, respuesta):
        if self.pregunta_actual().es_correcta(respuesta):
            self.puntaje += PUNTOS
            return True
        self.vidas -= 1
        return False
    def avanzar(self):
        self.indice += 1
    def terminado(self):
        return self.vidas == 0 or self.indice == TOTAL_PREGUNTAS - 1
#GUI (vistas)
class QuizApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Quiz de Historia de México")
        self.ventana.geometry("700x420")
        self.ventana.config(bg=COLOR_FONDO)
        self.marco = tk.Frame(ventana, bg=COLOR_FONDO)
        self.opcion = tk.StringVar()
        self.juego = None
        self.nombre = ""
        self.respondida = False
        self.mostrar_inicio()
    def nueva_vista(self):
        self.marco.destroy()
        self.marco = tk.Frame(self.ventana, bg=COLOR_FONDO)
        self.marco.pack()
    #vista inicio (pack)
    def mostrar_inicio(self):
        self.nueva_vista()
        tk.Label(self.marco, text="Quiz de Historia de México",
                 font=("Times New Roman", 24), bg=COLOR_FONDO).pack(pady=30)
        tk.Label(self.marco, text="Nombre del jugador:", bg=COLOR_FONDO).pack()
        self.entry_nombre = tk.Entry(self.marco)
        self.entry_nombre.pack(pady=10)
        tk.Button(self.marco, text="Comenzar", command=self.comenzar).pack(pady=10)
    def comenzar(self):
        nombre = self.entry_nombre.get().strip()
        if nombre == "":
            messagebox.showerror("Error", "Escribe tu nombre para comenzar")
            return
        try:
            preguntas = leer_preguntas()
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo preguntas.csv")
            return
        if len(preguntas) < TOTAL_PREGUNTAS:
            messagebox.showerror("Error", f"El archivo tiene menos de {TOTAL_PREGUNTAS} preguntas")
            return
        self.nombre = nombre
        self.juego = Juego(preguntas)
        self.mostrar_juego()
    #vista juego (grid)
    def mostrar_juego(self):
        self.nueva_vista()
        self.lbl_vidas = tk.Label(self.marco, bg=COLOR_FONDO)
        self.lbl_puntaje = tk.Label(self.marco, bg=COLOR_FONDO)
        self.lbl_pregunta = tk.Label(self.marco, font=("Times New Roman", 14),
                                     fg="#0a0a0a", bg=COLOR_FONDO)
        self.lbl_resultado = tk.Label(self.marco, bg=COLOR_FONDO)
        self.radios = []
        for i in range(4):
            self.radios.append(tk.Radiobutton(self.marco, variable=self.opcion, bg=COLOR_FONDO))
        boton_responder = tk.Button(self.marco, text="Responder", command=self.responder)
        boton_siguiente = tk.Button(self.marco, text="Siguiente", command=self.siguiente)
        self.lbl_vidas.grid(row=0, column=0, pady=10)
        self.lbl_puntaje.grid(row=0, column=1, pady=10)
        self.lbl_pregunta.grid(row=1, column=0, pady=15)
        for i in range(4):
            self.radios[i].grid(row=2 + i, column=0)
        self.lbl_resultado.grid(row=6, column=0, pady=10)
        boton_responder.grid(row=7, column=0, pady=10)
        boton_siguiente.grid(row=7, column=1, pady=10)
        self.mostrar_pregunta()
    def actualizar_marcadores(self):
        self.lbl_vidas.config(text=f"Vidas: {self.juego.vidas}")
        self.lbl_puntaje.config(text=f"Puntaje: {self.juego.puntaje}")
    def mostrar_pregunta(self):
        pregunta = self.juego.pregunta_actual()
        self.respondida = False
        self.opcion.set("")
        self.lbl_pregunta.config(text=pregunta.texto)
        for i in range(4):
            self.radios[i].config(text=pregunta.opciones[i], value=pregunta.opciones[i])
        self.lbl_resultado.config(text="")
        self.actualizar_marcadores()
    def responder(self):
        if self.respondida:
            return
        elegida = self.opcion.get()
        if elegida == "":
            messagebox.showerror("Error", "Selecciona una opción")
            return
        self.respondida = True
        if self.juego.responder(elegida):
            self.lbl_resultado.config(text=f"¡Correcto! +{PUNTOS} puntos")
        else:
            correcta = self.juego.pregunta_actual().correcta
            self.lbl_resultado.config(text=f"Incorrecto. La respuesta era: {correcta}")
        self.actualizar_marcadores()
    def siguiente(self):
        if not self.respondida:
            messagebox.showerror("Error", "Primero responde la pregunta")
            return
        if self.juego.terminado():
            self.mostrar_resultados()
        else:
            self.juego.avanzar()
            self.mostrar_pregunta()
    #vista resultados
    def mostrar_resultados(self):
        self.nueva_vista()
        total = TOTAL_PREGUNTAS * PUNTOS
        tk.Label(self.marco, text="Juego terminado",
                 font=("Times New Roman", 24), bg=COLOR_FONDO).pack(pady=30)
        tk.Label(self.marco,
                 text=f"{self.nombre}, tu puntaje final es {self.juego.puntaje} de {total}",
                 bg=COLOR_FONDO).pack(pady=10)
        tk.Button(self.marco, text="Reiniciar", command=self.mostrar_inicio).pack(pady=10)
        messagebox.showinfo("Fin del juego", f"Obtuviste {self.juego.puntaje} puntos")
ventana = tk.Tk()
app = QuizApp(ventana)
ventana.mainloop()