import streamlit as st
import PyPDF2
import io

# Crear un título para la aplicación
st.title("Buscar palabras en un archivo PDF")

# Crear un uploader de archivos
uploaded_file = st.file_uploader("Seleccione un archivo PDF", type=["pdf"])

# Crear un campo de texto para ingresar las palabras a buscar
search_words = st.text_input("Buscar palabras")

# Crear un botón para buscar palabras
search_button = st.button("Buscar")

# Procesar la solicitud cuando se carga el archivo PDF
if uploaded_file is not None and search_button:
    # Leer el archivo PDF
    pdf_file = uploaded_file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
    # Leer el contenido del archivo PDF
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extractText()

    # Buscar las palabras en el contenido del archivo PDF
    results = [word for word in search_words.split() if word in pdf_text]

    # Mostrar los resultados
    st.write("Resultados de la búsqueda:")
    st.write(results)
