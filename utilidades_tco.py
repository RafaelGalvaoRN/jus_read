import streamlit as st
from utilidades_tesseract import *
from utilidades_tco_classe import Processo



def trata_df(df):
    df.replace({True: 'Sim', False: 'Não'}, inplace=True)


def leitor_tco():
    st.markdown("""<br><br> """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Escolha seu pdf para eu ler", type=["pdf"], key="leitor_tco")

    if uploaded_file is not None:
        # Lê o conteúdo do arquivo PDF
        pdf_content = uploaded_file.read()

        # Chama a função para extrair texto do PDF
        text = extrai_texto(pdf_content)

        tco = Processo(text)

        tco.atualiza_todos_atributos()

        df = tco.retorna_atributos()
        trata_df(df)
        st.table(df)





