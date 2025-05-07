#modulos
import os  # interactuar con sistema operativo, buscar archivos...
import csv  # archivos .csv (leer, modificar)
import tkinter as tk  # interfaz gráfica
from tkinter import messagebox, simpledialog  # mensajes y diálogos

ARCHIVO = os.path.join(os.path.dirname(__file__), "preguntas.csv")  # ruta al archivo csv

def cargar_preguntas():
    preguntas = {}
    try:
        with open(ARCHIVO, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                preguntas[fila['pregunta'].strip().lower()] = fila['respuesta']
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo preguntas.csv no encontrado.")
    return preguntas

def agregar_pregunta(pregunta, respuesta):
    with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([pregunta, respuesta])

def responder():
    entrada = entrada_usuario.get().strip().lower()
    if not entrada:
        return

    entrada_sin_signos = entrada.replace("¿", "").replace("?", "")

    # 👉 Mostrar lo que escribió el usuario
    mostrar_respuesta(f"Tú: {entrada}")

    if entrada_sin_signos == "salir":
        ventana.quit()
        return

    respuesta = base_conocimiento.get(entrada_sin_signos)

    if respuesta:
        mostrar_respuesta(f"🤖: {respuesta}")
    else:
        mostrar_respuesta("🤖: No sé la respuesta. ¿Querés agregarla?")
        if messagebox.askyesno("Agregar respuesta", "¿Querés agregar una respuesta para esta CHADpregunta?"):
            nueva_respuesta = simpledialog.askstring("Respuesta", "Escribí la respuesta:")
            if nueva_respuesta:
                agregar_pregunta(entrada_sin_signos, nueva_respuesta)
                base_conocimiento[entrada_sin_signos] = nueva_respuesta
                mostrar_respuesta("🤖: ¡Gracias! Ya aprendí esa respuesta.")

    entrada_usuario.delete(0, tk.END)

def mostrar_respuesta(texto):
    chat.insert(tk.END, texto + "\n")
    chat.see(tk.END)

# Cargar datos
base_conocimiento = cargar_preguntas()

# Crear ventana
ventana = tk.Tk()
ventana.title("CHADGPT")

# Área de chat
chat = tk.Text(ventana, height=20, width=60, state=tk.NORMAL, wrap=tk.WORD)
chat.pack(padx=10, pady=10)

# Entrada de texto
entrada_usuario = tk.Entry(ventana, width=60)
entrada_usuario.pack(padx=10, pady=(0, 10))
entrada_usuario.bind("<Return>", lambda event: responder())

# Botón de enviar
boton = tk.Button(ventana, text="Enviar", command=responder)
boton.pack(pady=(0, 10))

# Mensaje inicial
mostrar_respuesta("🤖: ¡Hola! Soy tu asistente. Escribí tu CHADpregunta o 'salir' para terminar.")

# Ejecutar
ventana.mainloop()