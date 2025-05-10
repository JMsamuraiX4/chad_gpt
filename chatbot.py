# modulos
import os  # interactuar con sistema operativo, buscar archivos...
import csv  # archivos .csv (leer, modificar)
import difflib
import unicodedata
import tkinter as tk  # interfaz gráfica
from tkinter import messagebox, simpledialog  # mensajes y diálogos

ARCHIVO = os.path.join(os.path.dirname(__file__), "preguntas.csv")  # ruta al archivo csv
ICONO = os.path.join(os.path.dirname(__file__), "logo.ico")  # ruta al archivo ico

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
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = texto.replace("¿", "").replace("?", "").replace(",", "").replace(".", "")
    return texto

def responder():
    entrada = entrada_usuario.get().strip().lower()
    if not entrada:
        return

    mostrar_respuesta(f"🙋 Tú: {entrada}", "usuario")

    if entrada == "salir":
        ventana.quit()
        return

    entrada_normalizada = normalizar(entrada)
    preguntas_normalizadas = {normalizar(p): p for p in base_conocimiento}
    clave_real = preguntas_normalizadas.get(entrada_normalizada)

    if not clave_real:
        coincidencias = difflib.get_close_matches(entrada_normalizada, preguntas_normalizadas.keys(), n=1, cutoff=0.8)
        if coincidencias:
            clave_real = preguntas_normalizadas[coincidencias[0]]

    respuesta = base_conocimiento.get(entrada)

    if clave_real:
        respuesta = base_conocimiento[clave_real]
        mostrar_respuesta(f"🤖 ChadGPT: {respuesta}", "chatbot")
    else:
        mostrar_respuesta("🤖 ChadGPT: No sé la respuesta. ¿Querés agregarla?", "chatbot")
        if messagebox.askyesno("Agregar respuesta", "¿Querés agregar una respuesta para esta CHADpregunta?"):
            nueva_respuesta = simpledialog.askstring("Respuesta", "Escribí la respuesta:")
            if nueva_respuesta:
                agregar_pregunta(entrada, nueva_respuesta)
                base_conocimiento[entrada] = nueva_respuesta
                mostrar_respuesta("🤖 ChadGPT: ¡Gracias! Ya aprendí esa respuesta.", "chatbot")

    entrada_usuario.delete(0, tk.END)

def mostrar_respuesta(texto, remitente):
    chat.configure(state=tk.NORMAL)
    if remitente == "usuario":
        chat.insert(tk.END, texto + "\n", "usuario")
    else:
        chat.insert(tk.END, texto + "\n", "chatbot")
    chat.configure(state=tk.DISABLED)
    chat.see(tk.END)

# Cargar datos
base_conocimiento = cargar_preguntas()

# Crear ventana
ventana = tk.Tk()
ventana.title("CHADGPT")
ventana.iconbitmap(ICONO)
ventana.configure(bg="black")

# Área de chat
chat = tk.Text(ventana, height=20, width=60, state=tk.NORMAL, wrap=tk.WORD,
               bg="black", fg="white", insertbackground="white")
chat.tag_config("usuario", foreground="#00FFFF")  # cian brillante para usuario
chat.tag_config("chatbot", foreground="#FFFF00")  # amarillo brillante para chatbot
chat.pack(padx=10, pady=10)

# Entrada de texto
entrada_usuario = tk.Entry(ventana, width=60, bg="black", fg="white", insertbackground="white")
entrada_usuario.pack(padx=10, pady=(0, 10))
entrada_usuario.bind("<Return>", lambda event: responder())

# Botón de enviar
boton = tk.Button(ventana, text="Enviar", command=responder,
                  bg="black", fg="white", activebackground="#FFFFFF", activeforeground="black")
boton.pack(pady=(0, 10))

# Mensaje inicial
mostrar_respuesta("🤖 ChadGPT: ¡Hola! Soy tu asistente. Escribí tu CHADpregunta o 'salir' para terminar.", "chatbot")

# Ejecutar
ventana.mainloop()