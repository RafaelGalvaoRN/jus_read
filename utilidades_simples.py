import streamlit as st
from utilidades_tesseract import *



def leitor_simples():
    st.markdown("""<br><br> """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Escolha seu pdf para eu ler", type=["pdf"])

    if uploaded_file is not None:
        # Lê o conteúdo do arquivo PDF
        pdf_content = uploaded_file.read()

        # Chama a função para extrair texto do PDF
        text = extrai_texto(pdf_content)

        # Exibe o texto extraído
        st.write(text)