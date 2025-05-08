#modulos
import os  # interactuar con sistema operativo, buscar archivos...
import csv  # archivos .csv (leer, modificar)
import difflib
import unicodedata
import tkinter as tk  # interfaz gráfica
from tkinter import messagebox, simpledialog  # mensajes y diálogos

ARCHIVO = os.path.join(os.path.dirname(__file__), "preguntas_respuestas_chatbot_python.csv")  # ruta al archivo csv

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

def normalizar(texto):
    texto = texto.lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn') #Elimina las tildes
    texto = texto.replace("¿", "").replace("?", "").replace(",", "").replace(".", "")
    return texto

def responder():
    entrada = entrada_usuario.get().strip().lower()
    if not entrada:
        return

    # 👉 Mostrar lo que escribió el usuario
    mostrar_respuesta(f"Tú: {entrada}")

    if entrada == "salir":
        ventana.quit()
        return
    
    entrada_normalizada = normalizar(entrada)

    # Crear un diccionario con claves normalizadas
    preguntas_normalizadas = {normalizar(p): p for p in base_conocimiento}

    # Buscar coincidencia exacta
    clave_real = preguntas_normalizadas.get(entrada_normalizada)

        # Si no hay coincidencia exacta, buscar la más parecida
    if not clave_real:
        coincidencias = difflib.get_close_matches(entrada_normalizada, preguntas_normalizadas.keys(), n=1, cutoff=0.8)
        if coincidencias:
            clave_real = preguntas_normalizadas[coincidencias[0]]

    respuesta = base_conocimiento.get(entrada)

    if clave_real:
        respuesta = base_conocimiento[clave_real]
        mostrar_respuesta(f"🤖: {respuesta}")
    else:
        mostrar_respuesta("🤖: No sé la respuesta. ¿Querés agregarla?")
        if messagebox.askyesno("Agregar respuesta", "¿Querés agregar una respuesta para esta CHADpregunta?"):
            nueva_respuesta = simpledialog.askstring("Respuesta", "Escribí la respuesta:")
            if nueva_respuesta:
                agregar_pregunta(entrada, nueva_respuesta)
                base_conocimiento[entrada] = nueva_respuesta
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