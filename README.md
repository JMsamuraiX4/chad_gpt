# CHADGPT

**CHADGPT** es un chatbot con interfaz gráfica hecho en Python. Aprende nuevas respuestas que el usuario le enseña y las guarda en un archivo CSV. Usa `Tkinter` para la interfaz, `difflib` para encontrar coincidencias aproximadas, y `csv` para almacenar el conocimiento.

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

## 📦 Requisitos

- Python 3.6+

---

## 👥 Autores

Creado por "Los ChadGPT"  
Versión: 1.0 - 2025
