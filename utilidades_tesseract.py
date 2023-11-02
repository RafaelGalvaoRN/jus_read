import pytesseract
import fitz
import time
from PIL import Image
import os

from concurrent.futures import ThreadPoolExecutor


if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'F:\Program Files\Tesseract-OCR\tesseract.exe'




# Função para extrair texto de uma imagem
def extrai_texto_imagem(imagem):
    text = pytesseract.image_to_string(imagem, lang='por')
    return text



# versao com multhread
def extrai_uma_folha(pdf_document, page_num):
    page = pdf_document[page_num]
    image_list = page.get_pixmap()

    # Converta a imagem em um formato suportado pelo Tesseract OCR
    image_pil = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)

    # Extrair texto de cada página do PDF
    text = pytesseract.image_to_string(image_pil, lang='por')
    return text

# versao com multhread
def extrai_texto(pdf_content):
    start = time.time()
    extract = []

    # Use o PyMuPDF para abrir o arquivo PDF
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(extrai_uma_folha, pdf_document, page_num) for page_num in range(pdf_document.page_count)]
        for future in futures:
            extract.append(future.result())

    text = ' '.join(extract).replace('\n', " ")
    duration = time.time() - start
    # print(f'Aqui - Duração do método extrair texto: {duration}')
    # print(text)

    return text

#versao SEM multhread
# # Função para extrair texto de um arquivo PDF
# def extrai_texto(pdf_content):
#     start = time.time()
#     extract = []
#
#     # Use o PyMuPDF para abrir o arquivo PDF
#     pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
#
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document[page_num]
#         image_list = page.get_pixmap()
#
#         # Converta a imagem em um formato suportado pelo Tesseract OCR
#         image_pil = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
#
#         # Extrair texto de cada página do PDF
#         text = pytesseract.image_to_string(image_pil, lang='por')
#         extract.append(text)
#
#     text = ' '.join(extract).replace('\n', " ")
#     duration = time.time() - start
#     print(f'Acolá - Duração do método extrair texto: {duration}')
#     print(text)
#
#     return text