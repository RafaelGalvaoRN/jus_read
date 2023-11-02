import re


def sanitiza_data(palavra):
    # Expressão regular para encontrar datas no formato dd/dd/dd{2-4}
    regex = re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b')

    # Procura pela primeira ocorrência de uma data no texto
    match = regex.search(palavra)

    # Retorna a data encontrada ou None se nenhuma data for encontrada
    return match.group(0) if match else None


def sanitiza_data_8_digitos(data):
    # Verifica se a data tem 8 dígitos
    match = re.match(r"\d{8}", data)

    if match:
        # Obtém os 8 dígitos correspondentes
        oito_digitos = match.group(0)

        # Formate os 8 dígitos como uma data (assumindo que são YYYYMMDD)
        data_formatada = oito_digitos[0:2] + "/" + oito_digitos[2:4] + "/" + oito_digitos[4:8]

        # Substitui os 8 dígitos na string original pela data formatada
        resultado = re.sub(r"\d{8}", data_formatada, data)
        return resultado
    else:
        return data


def sanitiza_autor(palavra):
    palavra = re.sub(r"AUTOR", "", palavra)

    # lista de palavras para remover
    words_to_remove = ["Autor do Fato", "Autor:", "Autor;", ":"]

    # remove todas as palavras da lista
    for word in words_to_remove:
        palavra = re.sub(word, '', palavra)

    palavra = palavra.title().strip()

    return palavra


def sanitiza_crime2(result: str) -> str:
    words_to_remove = ["INFRAÇÕES", "PENAIS:",
                       "CUMPRIMENTO DE MANDADO;",
                       'BUSCA E APREENSÃO', "DOMICILIAR",
                       "TESTEMUNHA(S)", "\\\\",
                       "INFRAÇÚES", "AUTUAÇÃO",
                       '\"', "CUMPRIMENTO DE MANDADO",
                       "|", "TESTEMUNHA(S)", ", Autorizando",
                       " - | TESTEMUNHA(S)", "infração penal: ",
                       'TESTEMUNHA(S)', "— ", ":",
                       "\* ", 'ENDIS', 'TRÁFICO DE DROGAS ', 'AMEAÇA', 'Lesão corporal dolosa',
                       'INJÚRIA REAL', '(VIOLÊNCIA CONTRA A MULHER)',
                       'VIOLÊNCIA CONTRA A MULHER', "da", "caput", "do", "VTIMA"]

    # remove todas as palavras da lista
    for word in words_to_remove:
        result = re.sub(word, '', result,  flags=re.IGNORECASE)

    result = re.sub(r'[^a-zA-Z\d]+', '', result)
    result = re.sub(r'capu.', '', result ,flags=re.IGNORECASE)

    result = re.sub(r'CPB', 'CP', result)

    result = result.lower()



    return result


def satitization_crime(result: str) -> str:
    # lista de palavras para remover
    words_to_remove = ["INFRAÇÕES", "PENAIS:",
                       "CUMPRIMENTO DE MANDADO;",
                       'BUSCA E APREENSÃO', "DOMICILIAR",
                       "TESTEMUNHA(S)", "\\\\",
                       "INFRAÇÚES", "AUTUAÇÃO",
                       '\"', "CUMPRIMENTO DE MANDADO",
                       "|", "TESTEMUNHA(S)", ", Autorizando",
                       " - | TESTEMUNHA(S)", "infração penal: ",
                       'TESTEMUNHA(S)', "— ", ":",
                       "\* ", 'ENDIS', 'TRÁFICO DE DROGAS ']

    # remove todas as palavras da lista
    for word in words_to_remove:
        result = re.sub(word, '', result)

    # remove com re.sub, com ignorecase
    crimes_extensos = ['AMEAÇA', 'Lesão corporal dolosa',
                       'INJÚRIA REAL', '(VIOLÊNCIA CONTRA A MULHER)',
                       'VIOLÊNCIA CONTRA A MULHER']

    for crime in crimes_extensos:
        result = re.sub(crime, r'', result, flags=re.IGNORECASE)

    # corrige
    result = result.replace("CPB", 'CP')
    result = result.replace("TESTEMUNHA(S)", '')
    result = result.replace("FENAIS", '')
    result = result.replace("CPArt.", 'CP, Art.')
    result = result.replace("ART.", 'Art.')
    result = result.replace("artigo .", 'Art.')
    result = result.replace("()", '')
    result = result.replace('"', '')
    result = result.replace('“', '')
    result = result.replace('”', '')
    result = result.replace('|', '')
    result = result.replace('da', '')
    result = result.replace('Caput', '')
    result = result.replace('Lei de Drogas', 'Lei 11.343/2006')
    result = result.replace('Código Penal', 'CP')
    result = result.replace('Capur ', '')


    result = result.strip()

    # retira mais de dois espaços para um espaço
    result = re.sub(r'\s{2,}', r' ', result)

    # separa art.xxx para Art. XXX
    result = re.sub(r'Art\.? ?(\d+)', r'Art. \1', result)

    # separa artigo de "do (331do)
    result = re.sub(r'(\d+)do', r'\1 do', result, flags=re.IGNORECASE)

    #substitui caput, , por nada
    result = re.sub(r'caput, ,', r'', result, flags=re.IGNORECASE)
    result = re.sub(r'caput', r'', result, flags=re.IGNORECASE)


    # substitui 'do CP'por CP artigo de "do (331do)
    result = re.sub(r'do (CP)', r', \1', result, flags=re.IGNORECASE)

    # substitui '147 ,' por '147, " (retira espaço entre artigo e virgula)
    result = re.sub(r'(\d+) ,', r'\1,', result)

    # substitui ', CP ,' ou ', CP,' por ', CP;" (troca a virgula por ; para criar o futuro split)
    result = re.sub(r', CP ?,?', ', CP;', result)

    # substitui 'CP;Art.', por 'CP; Art.'
    result = re.sub(r'CP;Art\.', 'CP; Art.', result)

    # substitui Caput , CP por Caput, CP
    result = re.sub(r'Caput , CP', ', CP', result)

    # substitui '147 ,' por '147, " (retira espaço entre artigo e virgula)
    result = re.sub(r'(\d+) ,', r'\1,', result)

    # substitui 'C.B' por 'CP'
    result = re.sub(r'C.B', 'CP', result)




    # substitui a virgula por ponto, na expressao lei
    result = re.sub(r'(\d{2}),(?=\d{3})', r'\1.', result)

    # acrescenta uma virgula entre artigo da lei e a palavra "lei"
    result = re.sub(r'(Art.\s\d+)\s(Lei)', r'\1, \2', result)

    # retira espaco entre artigo e virgula, unindo o artigo a virgula
    result = re.sub(r'(\d+)\s,', r'\1,', result)

    # retira 'do' e, acrescenta uma virgula entre artigo e cp
    result = re.sub(r'(\d+) ?do ?CP,?', r'\1, CP', result)

    # corrige Decreto-Lei por LCP
    result = re.sub(r'(.+) do (.)+Lei +3\.68(.)+', r'\1, LCP', result)

    # corrige t. por Art.
    result = re.sub(r'^t\. ', r'Art. ', result)

    # retira incisos de art. 42 da LCP
    result = re.sub(r'Art. 42(.+)LCP', r'Art. 42, LCP', result)

    # corrige art. da 11343
    result = re.sub(r'Art. 33(.{,10})LEI 11.343/2006', r'Art. 33, Lei 11.343/06', result)

    result = re.sub(r'^-\s*(?=[Aa])', '', result)

    result = re.sub(r'^AArt.', 'Art.', result)

    result = re.sub(r'^ss Art.', 'Art.', result)

    result = re.sub(';', '', result)

    result = result.replace('$.503/1997', '9.503/1997')

    return result
