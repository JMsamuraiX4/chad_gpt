#modulos
import os #interactuar con sistema operativo, buscar archivos...
import csv #archivos .csv (leer, modificar)
import tkinter as tk #interfaz grafica
from tkinter import messagebox, simpledialog #tirar mensajes en sistema, y poder hacer input en mensajes de sistema

ARCHIVO = os.path.join(os.path.dirname(__file__), "preguntas.csv") #busca si esta el .csv en el mismo directorio, lo guarda como variable

def cargar_preguntas(): #carga las preguntas en el programa
    preguntas = {} #variable diccionario
    try:
        with open(ARCHIVO, mode='r', encoding='utf-8') as archivo: #abre el archivo desde modo lectura (read)
            lector = csv.DictReader(archivo) #convierte las lineas del csv en strings (objetos)
            for fila in lector:
                preguntas[fila['pregunta'].strip().lower()] = fila['respuesta'] #los guarda en el diccionario sin mayusculas ni espacios
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo preguntas.csv no encontrado.")
    return preguntas

def agregar_pregunta(pregunta, respuesta):
    with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as archivo: #abre el archivo desde modo agregar (add)
        escritor = csv.writer(archivo)
        escritor.writerow([pregunta, respuesta]) #guarda la pregunta junto con la respuesta que ingresa el usuario

def responder():
    entrada = entrada_usuario.get().strip().lower() #lee lo que ingresa el usuario
    if not entrada:
        return
    
    entrada = entrada.replace("¿", "").replace("?", "") #ignora signos de pregunta

    if entrada == "salir":
        ventana.quit() #sale del programa
        return

    respuesta = base_conocimiento.get(entrada) #asocia la respuesta con la pregunta

    if respuesta:
        mostrar_respuesta(f"🤖: {respuesta}") #si existe una respuesta para esa pregunta, lo responde
    else:
        mostrar_respuesta("🤖: No sé la respuesta. ¿Querés agregarla?") #si no existe, sugiere de agregar una respuesta para esas pregunta
        if messagebox.askyesno("Agregar respuesta", "¿Querés agregar una respuesta para esta pregunta?"):
            nueva_respuesta = simpledialog.askstring("Respuesta", "Escribí la respuesta:") #registra la respuesta ingresada por el usuario en un dialog contextual
            if nueva_respuesta:
                agregar_pregunta(entrada, nueva_respuesta) #agrega la respuesta a la pregunta con otra funcion
                base_conocimiento[entrada] = nueva_respuesta
                mostrar_respuesta("🤖: ¡Gracias! Ya aprendí esa respuesta.")

    entrada_usuario.delete(0, tk.END) #cierra el dialog contextual

def mostrar_respuesta(texto): #muestra el output de programa en la interfz principal
    chat.insert(tk.END, texto + "\n")
    chat.see(tk.END)

# Cargar datos
base_conocimiento = cargar_preguntas() #carga los datos con la funcion ya establecida y lo guarda

# Crear ventana
ventana = tk.Tk()
ventana.title("ChatBot - Fundamentos de Programación") #inicia la interfaz

# Área de chat
chat = tk.Text(ventana, height=20, width=60, state=tk.NORMAL, wrap=tk.WORD) #parametros de la interfaz
chat.pack(padx=10, pady=10)

# Entrada de texto
entrada_usuario = tk.Entry(ventana, width=60) #parametros apariencia cuadro input
entrada_usuario.pack(padx=10, pady=(0, 10))
entrada_usuario.bind("<Return>", lambda event: responder())

# Botón de enviar
boton = tk.Button(ventana, text="Enviar", command=responder) #parametros apariencia boton enviar
boton.pack(pady=(0, 10))

# Mensaje inicial
mostrar_respuesta("🤖: ¡Hola! Soy tu asistente. Escribí tu pregunta o 'salir' para terminar.")

# Ejecutar
ventana.mainloop() #ejecuta la interfaz