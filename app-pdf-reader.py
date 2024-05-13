import streamlit as st
import PyPDF2
import io
import os
import requests

# Configuración de la API de Groq
groq_api_key = os.environ['GROQ_API_KEY']
groq_api_url = "https://api.groq.com/v1/summarize"

# Crear un título para la aplicación
st.title("Buscar palabras en un archivo PDF y generar resumen")

# Crear un uploader de archivos
uploaded_file = st.file_uploader("Seleccione un archivo PDF", type=["pdf"])

# Crear un campo de texto para ingresar las palabras a buscar
search_words = st.text_input("Buscar palabras")

# Crear un botón para buscar palabras
search_button = st.button("Buscar")

# Crear un botón para generar resumen
generate_summary_button = st.button("Generar resumen")

if search_button:
    if uploaded_file is None:
        st.error("Por favor, suba un archivo PDF antes de buscar.")
    else:
        # Leer el archivo PDF
        pdf_file = uploaded_file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))

        # Leer el contenido del archivo PDF
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        # Buscar las palabras en el contenido del archivo PDF
        results = [word for word in search_words.split() if word in pdf_text]

        # Mostrar los resultados
        st.write("Resultados de la búsqueda:")
        st.write(results)

if generate_summary_button:
    if uploaded_file is None:
        st.error("Por favor, suba un archivo PDF antes de generar un resumen.")
    else:
        # Leer el archivo PDF
        pdf_file = uploaded_file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))

        # Leer el contenido del archivo PDF
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        try:
            # Enviar solicitud a la API de Groq
            response = requests.post(
                groq_api_url,
                headers={"Authorization": f"Bearer {groq_api_key}"},
                json={"text": pdf_text, "num_sentences": 5}  # Configuración del resumen
            )

       # Procesar la respuesta de la API
            if response.status_code == 200:
                summary = response.json()["summary"]
                st.write("Resumen:")
                st.write(summary)
            else:
                st.error("Error al generar resumen. Inténtelo de nuevo.")
        except requests.RequestException as e:
            st.error(f"Error al generar resumen: {e}")
