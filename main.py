import streamlit as st
from utilidades_tesseract import *
from utilidades_simples import leitor_simples
from utilidades_tco import leitor_tco
from leitor_img import leitor_imagem




st.title("LEITOR DE PDF")

tab1, tab2, tab3 = st.tabs(["Leitor Simples", "Leitor de Imagem",  "Analisador de TCO"])

with tab1:
   leitor_simples()

with tab2:
    leitor_imagem()
#
with tab3:
    leitor_tco()


