import streamlit as st
from utilidades_tesseract import *
from utilidades_simples import leitor_simples
from utilidades_tco import leitor_tco





st.title("LEITOR DE PDF")

tab1, tab2 = st.tabs(["Leitor Simples", "Analisador de TCO"])

with tab1:
   leitor_simples()

with tab2:
    leitor_tco()


