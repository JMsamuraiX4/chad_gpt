import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import difflib

ARCHIVO = os.path.join(os.path.dirname(__file__), "preguntas.csv")
ICONO = os.path.join(os.path.dirname(__file__), "logo.ico")

# Cargar CSV
df = pd.read_csv(ARCHIVO)
preguntas_lista = df['pregunta'].tolist()

def mostrar_respuesta(mensaje):
    chat.config(state='normal')
    chat.insert(tk.END, mensaje + "\n", "espaciado")
    chat.config(state='disabled')
    chat.see(tk.END)

def agregar_pregunta(pregunta, respuesta):
    with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as archivo:
        archivo.write(f'"{pregunta}","{respuesta}"\n')

def responder():
    comando = entrada.get().strip()
    entrada.delete(0, tk.END)

    if comando.lower() == "salir":
        ventana.destroy()
        return

    if len(comando.strip()) < 8 and len(comando.strip().split()) < 2 and comando.title() not in ["Hola", "Chau"]:
        mostrar_respuesta("Chatbot: Por favor, escribí una consulta más clara (mínimo 8 caracteres o 2 palabras).")
        return

    mostrar_respuesta(f"Tú: {comando}")

    coincidencias = df[df['pregunta'].str.contains(comando, case=False, na=False)]

    if not coincidencias.empty:
        respuesta = coincidencias.iloc[0]['respuesta']
        mostrar_respuesta(f"Chatbot: {respuesta}")
    else:
        similar = difflib.get_close_matches(comando, preguntas_lista, n=1, cutoff=0.5)
        if similar:
            sugerida = similar[0]
            respuesta = df[df['pregunta'] == sugerida].iloc[0]['respuestas']
            mostrar_respuesta(f"Chatbot: Tal vez quisiste decir: '{sugerida}'")
            mostrar_respuesta(f"Chatbot: {respuesta}")
        else:
            mostrar_respuesta("Chatbot: No encontré una respuesta parecida.")
            desea_agregar = messagebox.askyesno("Agregar pregunta", "¿Querés agregar esta pregunta?")
            if desea_agregar:
                respuesta_usuario = simpledialog.askstring("Tu respuesta", "Escribí qué respuesta esperabas:")
                if respuesta_usuario:
                    agregar_pregunta(comando, respuesta_usuario)
                    df.loc[len(df.index)] = [comando, respuesta_usuario]
                    preguntas_lista.append(comando)
                    mostrar_respuesta("Chatbot: ¡Gracias! Ya aprendí esa respuesta.")

# Crear ventana
ventana = tk.Tk()
ventana.title("CHAD GPT para Python")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.iconbitmap(ICONO)

# Área de chat
chat = tk.Text(ventana, height=30, width=58, state='disabled', wrap='word')
chat.pack(pady=10)
chat.tag_configure("espaciado", spacing3=5)

# Mensaje inicial
mostrar_respuesta("Chatbot: Bienvenido a Chadbot, un chatbot que responde preguntas sobre Python. ¿En qué te puedo asistir hoy?")

# Campo de entrada
entrada = tk.Entry(ventana, width=50)
entrada.pack(pady=5)
entrada.focus()

# Botón de enviar
boton = tk.Button(ventana, text="Enviar", command=responder)
boton.pack()

# Enviar con Enter
ventana.bind('<Return>', lambda event: responder())

ventana.mainloop()
