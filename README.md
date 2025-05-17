# CHADGPT

**CHADGPT** es un chatbot con interfaz gráfica hecho en Python. Aprende nuevas respuestas que el usuario le enseña y las guarda en un archivo CSV. Usa `Tkinter` para la interfaz, `difflib` para encontrar coincidencias aproximadas, y `csv` para almacenar el conocimiento.

---

## 🤔 ¿Que puede hacer ChadGPT?

- Responde preguntas sobre Python usando una base de datos propia.
- Aprende nuevas preguntas y respuestas que el usuario le enseña.
- Sugiere preguntas si el usuario escribe una palabra clave (ej: "listas", "herencia").
- Permite buscar y explorar el conocimiento guardado.

---

## 📝 Instrucciones de uso

- Escribi una pregunta sobre Python, por ejemplo:  
  `¿Cómo se imprime un mensaje en la consola?`
- Si el bot no sabe la respuesta, podes enseñarsela.
- Tambien podes escribir una sola palabra clave como `bucles`, `funciones` o `condicionales` para buscar coincidencias.
- Escribí `ayuda` para ver la guía de uso.
- Escribí `salir` para cerrar la aplicación.

---

## 📂 Estructura del proyecto

```
chad_gpt/
├── chatbot.py        # Script principal del bot
├── preguntas.csv     # Base de conocimiento (preguntas y respuestas)
├── logo.ico          # Ícono de la ventana
└── README.md         # Documentación
```

## 🚀 Cómo ejecutar el bot

### 1. Instala Python (si no lo tenés)

Este proyecto usa Python 3.6 o superior.

### 2. Clona el repositorio

```bash
git clone https://github.com/JMsamuraiX4/chad_gpt.git
cd chad_gpt
```

### 3. Ejecuta el ChadGPT

```bash
python chatbot.py
```

---

## 🧠 Cómo funciona el bot

1. Al iniciar, el bot carga todas las preguntas desde `preguntas.csv`.

2. Cuando el usuario pregunta algo: normaliza la entrada, busca coincidencias y si no encuentra la respuesta, pide al usuario que la enseñe.

3. Cada nueva respuesta se guarda en el archivo CSV y se aprende al instante.

---

## 💬 Ejemplo de uso

```
🙋 Tú: ¿Cómo se declara una variable en Python?
🤖 ChadGPT: Solo asignando un valor: x = 10.

🙋 Tú: ¿cuántos años tenés?
🤖 ChadGPT: No sé la respuesta. ¿Querés agregarla?
(Usuario agrega: "La edad es irrelevante para un chad.")
🤖 ChadGPT: ¡Gracias! Ya aprendí esa respuesta.
```

---

## 🛠️ Manejo de errores

- Si el archivo `preguntas.csv` no existe, se muestra un mensaje de error.
- El bot evita errores si el usuario no escribe nada.
- Se filtran caracteres especiales y tildes para mejorar las coincidencias.

---

## 📦 Requisitos

- Python 3.6+

---

## 👥 Autores

Creado por "Los ChadGPT"  
Versión: 1.0 - 2025
