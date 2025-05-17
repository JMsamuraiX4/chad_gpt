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
    preguntas = {} # Se crea un diccionario vacío para almacenar las preguntas y respuestas.
    try:
        with open(ARCHIVO, mode='r', encoding='utf-8') as archivo: #Se abre el archivo .csv en modo lectura (mode='r')
            lector = csv.DictReader(archivo) # Se crea un lector que convierte cada fila en un diccionario.
            for fila in lector:
                preguntas[fila['pregunta'].strip().lower()] = fila['respuesta'] # Se agrega al diccionario una entrada con la pregunta y la respuesta.
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo preguntas.csv no encontrado.") # Si el archivo no existe, se muestra un mensaje de error.
    return preguntas

def agregar_pregunta(pregunta, respuesta):
    with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as archivo: # Se abre el archivo CSV en modo 'append' (mode='a')
        escritor = csv.writer(archivo) #Creacion de un escritor de csv
        escritor.writerow([pregunta, respuesta]) # Se escribe una nueva fila con la pregunta y la respuesta

def normalizar(texto):
    texto = texto.lower().strip() # Convierte todo a minúsculas (lower()) y elimina espacios (strip())
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = texto.replace("¿", "").replace("?", "").replace(",", "").replace(".", "") # Elimina signos de puntuacion comunes para mejorar coincidencia
    return texto

def responder():
    entrada = entrada_usuario.get().strip().lower() # Obtiene el texto ingresado por el usuario
    if not entrada:
        return

    mostrar_respuesta(f"🙋 Tú: {entrada}", "usuario")

    # Si el usuario escribió "salir", se cierra la ventana (termina el programa)
    if entrada == "salir": 
        ventana.quit()
        return
    
    #Si el usuario escribio "ayuda", se muestra un mensaje dando mas informacion sobre su uso al usuario.
    if entrada == "ayuda":
        mostrar_respuesta(
        "🤖 ChadGPT: Guía de uso:\n"
        "- Escribí una pregunta sobre Python, por ejemplo: ¿Cómo uso un bucle for?\n"
        "- Si no sé la respuesta, podés enseñármela y la recordaré.\n"
        "- También podés escribir solo una *palabra clave* (ej: 'herencia') y te sugeriré preguntas relacionadas.\n"
        "- Escribí 'salir' para cerrar el programa.", #Primer argumento, indica el mensaje
        "chatbot" #Argumento que indica el remitente del mensaje
        ) 
        entrada_usuario.delete(0, tk.END)
        return

    entrada_normalizada = normalizar(entrada)

    coincidencias = [preg for preg in base_conocimiento if entrada_normalizada in normalizar(preg)] # Buscar coincidencias con la palabra clave

    if coincidencias and len(coincidencias) >= 2: #Si encuentra coincidencias y son mas de 2
        mensaje = "🤖 ChadGPT: Encontre preguntas relacionadas con esa palabra clave: \n" #Avisa al usuario que encontro mas de una coincidencia
        for i, preg in enumerate(coincidencias[:5], 1): # muestra hasta 5 coincidencias
            mensaje += f"{i}. {preg}\n" #Muestra el mensaje con el siguiente formato: 1. pregunta
        mensaje += "\n Podes copiar y pegar una de estas preguntas para obtener la respuesta." 
        mostrar_respuesta(mensaje, "chatbot")
        entrada_usuario.delete(0, tk.END)
        return

    clave_real = None

    # Intentar buscar pregunta exacta
    for original in base_conocimiento:
        if normalizar(original) == entrada_normalizada:
            clave_real = original
            break

    # Si no se encontró exacta, usar difflib como respaldo
    if not clave_real:
        mejor_coincidencia = difflib.get_close_matches( entrada_normalizada, [normalizar(p) for p in base_conocimiento.keys()], n=1, cutoff=0.75) # Acepta coincidencias hasta 75%
        if mejor_coincidencia:
            for original in base_conocimiento:
                if normalizar(original) == mejor_coincidencia[0]:
                    clave_real = original
                    break


    if clave_real: # Si se encontró una coincidencia
        if entrada != clave_real: # Si la pregunta del usuario no era exactamente igual a la clave encontrada
            mostrar_respuesta(f'🤖 ChadGPT: ¿Quisiste decir: "{clave_real}"?\nRespuesta: {base_conocimiento[clave_real]}', "chatbot") # Sugiere la coincidencia encontrada y la muestra
        else:
            mostrar_respuesta(f"🤖 ChadGPT: {base_conocimiento[clave_real]}", "chatbot") # Si la pregunta coincide exactamente, simplemente muestra la respuesta
    else:
        mostrar_respuesta("🤖 ChadGPT: No sé la respuesta. ¿Querés agregarla?", "chatbot") #Se informa al usuario si no se encontraron coincidencias
        if messagebox.askyesno("Agregar respuesta", "¿Querés agregar una respuesta para esta CHADpregunta?"): # Se le pregunta al usuario si desea agregar una respuesta
            nueva_respuesta = simpledialog.askstring("Respuesta", "Escribí la respuesta:") # Se solicita al usuario que escriba la respuesta
            if nueva_respuesta:
                agregar_pregunta(entrada, nueva_respuesta) # Se guarda la nueva pregunta y respuesta en el archivo
                base_conocimiento[entrada] = nueva_respuesta
                mostrar_respuesta("🤖 ChadGPT: ¡Gracias! Ya aprendí esa respuesta.", "chatbot")

    entrada_usuario.delete(0, tk.END) # Limpia el input para la proxima pregunta

def mostrar_respuesta(texto, remitente):
    chat.configure(state=tk.NORMAL) # Habilita el area de texto para poder modificarla
    if remitente == "usuario": #Si el que envia el mensaje es el usuario...
        chat.insert(tk.END, texto + "\n", "usuario") # Inserta el texto al final del area de chat con el estilo "usuario" (color cian)
    else:
        chat.insert(tk.END, texto + "\n", "chatbot") # Sino el mensaje es del chatbot y lo muestra con el estilo "chatbot" (color amarillo)
    chat.configure(state=tk.DISABLED)
    chat.see(tk.END) # Mueve la vista del chat hasta el final para que siempre se vea el ultimo mensaje

# Cargar datos
base_conocimiento = cargar_preguntas()

# Crear ventana
ventana = tk.Tk()
ventana.title("CHADGPT")
ventana.iconbitmap(ICONO)
ventana.configure(bg="black")

# Área de chat
chat = tk.Text(ventana, height=20, width=60, state=tk.NORMAL, wrap=tk.WORD, bg="black", fg="white", insertbackground="white")
chat.tag_config("usuario", foreground="#00FFFF")  # cian brillante para usuario
chat.tag_config("chatbot", foreground="#FFFF00")  # amarillo brillante para chatbot
chat.pack(padx=10, pady=10)

# Entrada de texto
entrada_usuario = tk.Entry(ventana, width=60, bg="black", fg="white", insertbackground="white")
entrada_usuario.pack(padx=10, pady=(0, 10))
entrada_usuario.bind("<Return>", lambda event: responder())

# Botón de enviar
boton = tk.Button(ventana, text="Enviar", command=responder, bg="black", fg="white", activebackground="#FFFFFF", activeforeground="black")
boton.pack(pady=(0, 10))

# Mensaje inicial
mostrar_respuesta("🤖 ChadGPT: ¡Hola! Bienvenido a CHAD GPT. Un bot de asistencia para aprender Python de forma gratuita.\n\nEscribime tu pregunta (e.j: '¿Cómo se imprime un mensaje en la consola en Python?' o '¿Cómo se usa un bucle for en Python?') e intentaré responderla.\n\nEn el caso de no saberla puede agregarla a la base de datos." "\n\nEscribí 'ayuda' en cualquier momento para ver una guía de uso.", "chatbot")

# Ejecutar
ventana.mainloop()