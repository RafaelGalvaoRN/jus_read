import pyperclip
from PIL import ImageGrab
from utilidades_tesseract import *
import streamlit as st


# pega imagem da área de transferência

def leitor_imagem():
    button_style = """
    <style>
        .stButton > button {
            color: white;
            background-color: #007BFF;  /* Cor de fundo azul */
            border-radius: 5px;  /* Borda arredondada */
            border: none;  /* Sem borda */
            padding: 10px 20px;  /* Espaçamento interno */
            font-size: 16px;  /* Tamanho da fonte */
        }
        .stButton > button:hover {
            background-color: #0056b3;  /* Cor de fundo mais escura ao passar o mouse */
        }
    </style>
    """

    st.markdown(button_style, unsafe_allow_html=True)

    st.markdown("## Instruções de Uso 📚", unsafe_allow_html=True)
    st.markdown(
        "1. **Instalação**: Primeiramente, baixe e instale o aplicativo LightShot, disponível [aqui](https://app.prntscr.com/pt-br/download.html)."
    )
    st.markdown(
        "2. **Captura de Tela**: Com o LightShot ativo, pressione a tecla `PRINT SCRN` no seu teclado para iniciar a ferramenta de captura de tela. Selecione a área da tela que contém o texto que você deseja transcrever."
    )
    st.markdown(
        "3. **Seleção de Área**: Com o mouse, ajuste e defina exatamente a área que contém o texto. Certifique-se de capturar todo o texto que você deseja transcrever."
    )
    st.markdown(
        "4. **Copiar Texto**: Após selecionar a área de interesse, pressione `Ctrl + C` para copiar a imagem para a sua área de transferência."
    )
    st.markdown(
        "5. **Transcrição**: Finalmente, volte para esta página e clique no botão 'Transcrever' abaixo. O texto também será disponibilizado na sua área de transferência, pronto para ser colado em qualquer aplicativo utilizando `Ctrl + V`."
    )
    st.markdown("<br>", unsafe_allow_html=True)


    if st.button("Transcrever"):
        img = ImageGrab.grabclipboard()
        # Salva a imagem da área de transferência em um arquivo

        if img is not None:
            img.save('arquivo.png', 'PNG')
            # Lê a imagem da área de transferência

            texto = pytesseract.image_to_string(Image.open('arquivo.png'), lang='por')

            # retira as quebras de linha e/ou corrige texto

            # texto = texto.replace('\n', ' ')

            # Imprime o texto da imagem no editor do pycharm

            st.text_area("Texto Transcrito:", texto, height=200)

            # copia o texto para a área de transferência para ser usado prontamente
            pyperclip.copy(texto)
        else:
            st.error("Nenhuma imagem na área de transferência")
