import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import difflib

# Rutas de archivos
ARCHIVO = os.path.join(os.path.dirname(__file__), "preguntas.csv")
ICONO = os.path.join(os.path.dirname(__file__), "logo.ico")

# Cargar CSV
df = pd.read_csv(ARCHIVO)
# Convierte las preguntas en una lista y las guarda en una variable
preguntas_lista = df['pregunta'].tolist()

# Mostrar mensajes en el chat
def mostrar_respuesta(mensaje):
    chat.config(state='normal')
    chat.insert(tk.END, mensaje + "\n")
    chat.config(state='disabled')
    chat.see(tk.END)

#Función de agregar preguntas al archivo csv
def agregar_pregunta(pregunta, respuesta):
    df.loc[len(df.index)] = [pregunta, respuesta]
    df.to_csv(ARCHIVO, index=False)
    preguntas_lista.append(pregunta)

def responder(_event=None):
    comando = entrada.get().strip()

    # Borra el contenido dentro del input
    entrada.delete(0, tk.END)

    # Si el comanod es igual a "salir", se termina el programa
    if comando.lower() == "salir":
        ventana.destroy()
        return

    # Si el comando tiene menos de 8 letras o no tiene como mínimo 2 palabras, se muestra un mensaje de alerta. Se añade la excepción de los comandos "Hola" y "Chau"
    if len(comando) < 8 and len(comando.split()) < 2 and comando.title() not in ["Hola", "Chau"]:
        mostrar_respuesta("Chatbot: Por favor, escribí una consulta más clara (mínimo 8 caracteres o 2 palabras).")
        return

    # Se agrega el mensaje envíado al chat
    mostrar_respuesta(f"Tú: {comando}")

    # Se guardan en la variable las preguntas que contengan el valor de la variable comando sin importar las mayúsculas
    coincidencias = df[df['pregunta'].str.contains(comando, case=False, na=False)]

    # Si hay coinicidencias se muestra su respectiva respuesta
    if not coincidencias.empty:
        respuesta = coincidencias.iloc[0]['respuesta']
        mostrar_respuesta(f"Chatbot: {respuesta}")
    else:
        similar = difflib.get_close_matches(comando, preguntas_lista, n=1, cutoff=0.5)

        # Si hay similar se muestra la pregunta similar con a su respuesta
        if similar:
            sugerida = similar[0]
            respuesta = df[df['pregunta'] == sugerida].iloc[0]['respuesta']
            mostrar_respuesta(f"Chatbot: Tal vez quisiste decir: '{sugerida}'")
            mostrar_respuesta(f"Chatbot: {respuesta}")
        else:
            mostrar_respuesta("Chatbot: No encontré una respuesta parecida.")
            desea_agregar = messagebox.askyesno("Agregar pregunta", "¿Querés agregar esta pregunta?")
            if desea_agregar:
                respuesta_usuario = simpledialog.askstring("Tu respuesta", "Escribí qué respuesta esperabas:")
                if respuesta_usuario:
                    agregar_pregunta(comando, respuesta_usuario)
                    mostrar_respuesta("Chatbot: ¡Gracias! Ya aprendí esa respuesta.")

# Crear ventana
ventana = tk.Tk()

# Título de ventana
ventana.title("CHAD GPT para Python")

# Tamaño de ventana
ventana.geometry("500x600")

# Se cancela la posibilidad de manipular el tamaño de la ventana
ventana.resizable(False, False)

# Se agrega nuestro logo como ícono de la ventana
ventana.iconbitmap(ICONO)

# Área de chat
chat = tk.Text(ventana, height=30, width=58, state='disabled', wrap='word')
chat.pack(pady=10)

# Mensaje de bienvenida
mostrar_respuesta("Chatbot: Bienvenido a Chadbot, un chatbot que responde preguntas sobre Python. ¿En qué te puedo asistir hoy?")

# Campo de entrada
entrada = tk.Entry(ventana, width=50)
entrada.pack(pady=5)
entrada.focus()

# Botón de enviar
boton = tk.Button(ventana, text="Enviar", command=responder)
boton.pack()

# Enviar con Enter
ventana.bind('<Return>', responder)

# Iniciar app
ventana.mainloop()
