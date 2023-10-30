import spacy
from spacy import displacy
from spacy.matcher import PhraseMatcher, Matcher
import re
import time
from functools import wraps
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dicionario_pattern import DICT_PATTERN_REGEX, DICT_PATTERN_SPACY
import pandas as pd
from threading import Thread


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Início da execução do método {func.__name__}.")  # imprime a mensagem de início
        start_time = time.time()  # inicia o contador de tempo
        result = func(*args, **kwargs)  # chama a função original
        end_time = time.time()  # termina o contador de tempo
        execution_time = end_time - start_time  # calcula o tempo de execução
        print(f"Fim da execução do método {func.__name__}")
        print(f"Tempo de execução de {func.__name__}: {execution_time} segundos")
        return result

    return wrapper


class Processo:
    nlp = spacy.load("pt_core_news_lg")

    def __init__(self, texto, per=None, misc=None, org=None, loc=None):
        self.numero_processo = None
        self.texto = texto
        self.texto_entidades = self.get_ent_spacy()
        self.per = per if per is not None else []
        self.misc = misc if misc is not None else []
        self.org = org if org is not None else []
        self.loc = loc if loc is not None else []
        self.proposta_transacao = None  # Atributo para armazenar o resultado da verificação
        self.infracao_penal = None  # Atributo para armazenar o resultado da verificação
        self.data_do_crime = None
        self.certidao = None
        self.natureza_acao = None
        self.nome_autor = None
        self.retratacao_representacao = None
        self.queixa_crime = None
        self.sentenciado = False
        self.representacao_criminal = None
        self.prazo_decadencial = None
        self.procuracao = None

    def verifica_decadencia_seis_meses(self, data):
        data = data.strip()

        if data is None:
            self.prazo_decadencial = None
            return

        match = re.match(r'\d{2}\/\d{2}\/\d{2,4}', data, re.IGNORECASE)

        if not match:
            self.prazo_decadencial = None
            return

        try:
            data = datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            data = datetime.strptime(data, "%d/%m/%y")

        data_atual = datetime.now()

        diff = relativedelta(data_atual, data)

        # Verifica se passaram mais de 6 meses
        if diff.years > 0 or diff.months > 6 or (diff.months == 6 and diff.days > 0):
            self.prazo_decadencial = True
        else:
            self.prazo_decadencial = False

    def get_ner(self):
        pessoas = []
        miscelaneo = []
        organizacao = []
        localidade = []

        doc = self.nlp(self.texto)
        ents = list(doc.ents)

        for ent in ents:
            if ent.label_ == "PER":
                pessoas.append(ent.text)
            elif ent.label_ == "MISC":
                miscelaneo.append(ent.text)
            elif ent.label_ == "ORG":
                organizacao.append(ent.text)
            elif ent.label_ == "LOC":
                localidade.append(ent.text)
            else:
                continue  # ignore other labels

        self.per = set(pessoas)
        self.misc = set(miscelaneo)
        self.org = set(organizacao)
        self.loc = set(localidade)

    # @timer_decorator
    def verifica_proposta_transacao_regex_spacy(self):

        patterns = DICT_PATTERN_REGEX["proposta_transacao"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                result = match.group(0).strip()  # strip() é usado para remover espaços em branco no início e no final
                print(f"\033[92mSucesso\033[0m: Transação | Regex")

                self.proposta_transacao = True  # Armazena o resultado da verificação
                return

        # passa a analisar pel spacy

        print(f"Falhou: Transação | Regex")

        doc = self.nlp.make_doc(self.texto)
        matcher = PhraseMatcher(self.nlp.vocab, attr='LOWER')

        # com matcher
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["proposta_transacao"]["pattern1"]
        pattern2 = DICT_PATTERN_SPACY["proposta_transacao"]["pattern2"]

        matcher.add("proposta_transacao", [pattern1, pattern2])
        matches = matcher(doc)

        # com prahse matcher

        pattern_prase_matcher = DICT_PATTERN_SPACY["proposta_transacao"]["phrase_matcher"]

        phrase_patterns = [self.nlp.make_doc(text) for text in pattern_prase_matcher]
        phrase_matcher = PhraseMatcher(self.nlp.vocab)
        phrase_matcher.add("proposta_transacao", phrase_patterns)
        phrase_matches = [(match_id, start, end) for match_id, start, end, label in
                          phrase_matcher(doc)]  # Extraímos somente as partes relevantes

        combined_matches = matches + phrase_matches

        if combined_matches:
            for match_id, start, end in combined_matches:
                span = doc[start:end]
                print('Sucesso: Proposta de transacão | SPACY')
                print(start, end, span.text)
            self.proposta_transacao = True  # Armazena o resultado da verificação
            return
        print('Falhou: Transação | Spacy')
        self.proposta_transacao = False

    def separar_crimes(self, crime_str):
        # Procura por 'Art' seguido de números e possivelmente outros caracteres
        pattern = r'(?=Art\. \d+)'

        # Usa o padrão detectado para dividir a string em crimes individuais
        crimes = re.split(pattern, crime_str)

        # Limpa cada crime
        crimes = [crime.strip() for crime in crimes if crime]

        return crimes

    def split_string_based_on_keywords(self, text):
        # Lista de palavras-chave para divisão
        keywords = ['Art', ';', 'Lei']

        # Criamos um padrão regex que procura qualquer uma das palavras-chave
        pattern = '|'.join(map(re.escape, keywords))

        # O split retorna uma lista de strings
        # O padrão "\s*" é para remover espaços adicionais no início ou no final das strings
        splits = [s.strip() for s in re.split(r'\s*(?=' + pattern + r')|\s*(?<=;)\s*', text) if s]

        return splits

    # @timer_decorator
    def verifica_infracao_penal_regex(self):
        patterns = DICT_PATTERN_REGEX["infracao_penal"]
        srings_crimes = []

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            # print('aqui aqui', match)
            if match:
                result = match.group(0).strip()
                if result:
                    srings_crimes.append(result)

        string_crimes_nova = []
        for s in srings_crimes:
            string_crimes_nova.extend(self.split_string_based_on_keywords(s))

        patterns = DICT_PATTERN_REGEX["crimes"]
        crimes_encontrados=[]

        for pattern in patterns:
            for item in string_crimes_nova:
                # print("Analisando trecho:", item)
                match = re.findall(pattern, item, re.IGNORECASE)
                # print("Encontrei os trechos:", match, "com o pattern", pattern)
                if match:
                    result = [x.strip() for x in match]

                    # print("Adicionando o seguinte result no listao:", result)

                    crimes_encontrados.extend(result)

        # print('aqui aqui CRIMES ENCONTRADOS', crimes_encontrados)





                #
                # print(f"Sucesso: Infração penal '{result}' | REGEX")
                #
                # # transforma os crimes em uma lista de crimes
                # crimes = result.split(';')
                #
                # # Usa a função separar_crimes para cada crime
                # crimes = [self.separar_crimes(crime) for crime in crimes]

                # "Achata" a lista
                # crimes = [item for sublist in crimes for item in sublist]

                # # retira o elemento da lista vazia gerado pelo split, quando o ; é o último caractere
                # crimes = [r for r in crimes if r]
                #
                # # retira espaços antes e depois
                # crimes = [r.strip() for r in crimes]
                #
                # crimes_encontrados.extend(crimes)
                # break  # Se uma correspondência foi encontrada, saímos do loop

        # Aplica a função de sanitização e converte o resultado para uma lista
        crimes_sanitizados = list(set(map(self.satitization_crime, crimes_encontrados)))


        # Armazena o resultado da verificação
        self.infracao_penal = crimes_sanitizados

        if not crimes_encontrados:
            # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem
            print("Falhou: Infração Penal | Regex")

    # @timer_decorator
    def get_ent_spacy(self):
        texto_com_entidades = None  # Valor padrão
        try:
            doc = self.nlp(self.texto)
            texto_com_entidades = displacy.render(doc, style="ent", page=True, jupyter=False)
            return texto_com_entidades
        except Exception as e:
            print(f"Erro ao processar o texto: {e}")

    # @timer_decorator
    def verifica_retratacao_regex_spacy(self):

        patterns = DICT_PATTERN_REGEX["retratacao"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"\033[92mSucesso\033[0m: Retratação de representação | Regex")
                self.retratacao_representacao = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Falhou: Retratacao da Representação | Regex")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["retratacao"]["pattern1"]

        matcher.add("retratacao_representacao", [pattern1])

        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                span = doc[start:end]
                print(f'\033[92mSucesso\033[0m: Retratação da Representacao | SPACY')
                print(start, end, span.text)
            self.retratacao_representacao = True  # Armazena o resultado da verificação
            return
        print('Falhou: Retratação da Representação | Spacy')
        self.retratacao_representacao = False
        return


    def get_numero_processo(self):
        patterns = DICT_PATTERN_REGEX["numero_processo"]
        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"\033[92mSucesso\033[0m: Número do Processo | Regex")
                numero_processo = match.group()
                self.numero_processo = numero_processo

                return  # Se uma correspondência foi encontrada, saímos da função
            # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Falhou: Número Processo | Regex")
        self.numero_processo = False



    # @timer_decorator
    def verifica_sentenca(self):

        patterns = DICT_PATTERN_REGEX["sentença"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"033[92mSucesso033[0m: Sentença | REGEX")
                self.sentenciado = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Falhou: Sentença | Regex")

        doc = self.nlp.make_doc(self.texto)

        # com matcher
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["sentença"]["pattern1"]

        matcher.add("sentença", [pattern1])
        matches = matcher(doc)

        pattern_prase_matcher = DICT_PATTERN_SPACY["sentença"]["phrase_matcher"]

        phrase_patterns = [self.nlp.make_doc(text) for text in pattern_prase_matcher]
        phrase_matcher = PhraseMatcher(self.nlp.vocab)
        phrase_matcher.add("sentença", phrase_patterns)
        phrase_matches = [(match_id, start, end) for match_id, start, end, label in
                          phrase_matcher(doc)]  # Extraímos somente as partes relevantes

        combined_matches = matches + phrase_matches

        if combined_matches:
            for match_id, start, end in combined_matches:
                span = doc[start:end]
                print('033[92mSucesso033[0m: Sentença | SPACY')
                print(start, end, span.text)
            self.sentenciado = True  # Armazena o resultado da verificação
            return
        print('Falhou: Sentença | Spacy')
        return

    # @timer_decorator
    def verifica_representacao_regex_spacy(self):

        patterns = DICT_PATTERN_REGEX["representacao"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"\033[92mSucesso\033[0m: Representação criminal | REGEX")
                self.representacao_criminal = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Falhou: Representação criminal | Regex")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["representacao"]["pattern1"]

        matcher.add("representação criminal", [pattern1])

        matches = matcher(doc)
        if matches:
            print(f'\033[92mSucesso\033[0m: Representação criminal | SPACY')
            self.representacao_criminal = True  # Armazena o resultado da verificação
            return
        print('Falhou: Representação criminal | Spacy')
        self.representacao_criminal = False
        return

    # @timer_decorator
    def verifica_queixa_crime_regex_spacy(self):

        patterns = DICT_PATTERN_REGEX["queixa_crime"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"\033[92mSucesso\033[0m: Queixa Crime | REGEX")
                self.queixa_crime = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Falhou: Queixa-crime | Regex")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["queixa_crime"]["pattern1"]

        matcher.add("queixa-crime", [pattern1])

        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                span = doc[start:end]
                print('033[92mSucesso033[0m: Queixa-crime | SPACY')
                print(start, end, span.text)
            self.queixa_crime = True  # Armazena o resultado da verificação
            return
        print('Falhou: Queixa-crime | Spacy')
        self.queixa_crime = False
        return

    # @timer_decorator
    def verifica_data_crime_regex_spacy(self):

        patterns = DICT_PATTERN_REGEX["data_crime"]

        for pattern in patterns:
            # Use re.search para encontrar a correspondência
            match = re.search(pattern, self.texto, re.IGNORECASE)
            # Se uma correspondência foi encontrada, imprima-a
            if match:

                date = match.group(1)  # group(1) pega o primeiro grupo capturado, que é a data
                print(f"\033[92mSucesso\033[0m: Data do crime {date} | Regex")

                self.data_do_crime = date

                # atualiza prazo de decadencia
                self.verifica_decadencia_seis_meses(self.data_do_crime)
                return

        print("Falhou: Data | Regex")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["data_crime"]["pattern1"]
        pattern2 = DICT_PATTERN_SPACY["data_crime"]["pattern2"]

        matcher.add("data_crime_localizada_spacy", [pattern1, pattern2])
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                span = doc[start:end]


                # lista de palavras para remover

                result = self.sanitiza_data(span.text)


            print(f"\033[92mSucesso\033[0m: Data do crime {result} | Spacy")
            self.data_do_crime = result  # Armazena o resultado da verificação

            # atualiza prazo de decadencia
            self.verifica_decadencia_seis_meses(self.data_do_crime)

            return

        self.data_do_crime = None  # Armazena o resultado da verificação se nenhuma condição for satisfeita

    def satitization_crime(self, result: str) -> str:
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
        result = result.replace('|', '')
        result = result.replace('da', '')
        result = result.replace('Caput', '')
        result = result.replace('Lei de Drogas', 'Lei 11.343/2006')
        result = result.replace('Código Penal', 'CP')

        result = result.strip()

        # retira mais de dois espaços para um espaço
        result = re.sub(r'\s{2,}', r' ', result)

        # separa art.xxx para Art. XXX
        result = re.sub(r'Art\.? ?(\d+)', r'Art. \1', result)

        # separa artigo de "do (331do)
        result = re.sub(r'(\d+)do', r'\1 do', result, flags=re.IGNORECASE)

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


        return result

    # @timer_decorator
    def verifica_certidao_regex_spacy(self):

        patterns_certidao_positiva = DICT_PATTERN_REGEX["certidao_positiva"]
        patterns_certidao_negativa = DICT_PATTERN_REGEX["certidao_negativa"]

        for pattern in patterns_certidao_positiva:
            match_positiva = re.search(pattern, self.texto, re.IGNORECASE)
            if match_positiva:
                print(f"033[92mSucesso033[0m: Certidão Positiva | Regex")
                self.certidao = "Positiva"
                return

        for pattern in patterns_certidao_negativa:
            match_negativa = re.search(pattern, self.texto, re.IGNORECASE)
            if match_negativa:
                print(f"033[92mSucesso033[0m: Certidão Negativa | Regex")
                self.certidao = "Negativa"
                return

        print('Falhou: Certidão | Regex')
        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)
        pattern_postiva = DICT_PATTERN_SPACY["certidao_positiva"]["pattern1"]

        pattern_negativa = DICT_PATTERN_SPACY["certidao_negativa"]["pattern1"]

        matcher.add("certidao_positiva", [pattern_postiva])
        matcher.add("certidao_negativa", [pattern_negativa])
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                string_id = self.nlp.vocab.strings[match_id]
                if string_id == 'certidao_positiva':
                    print('033[92mSucesso033[0m: Certidão positiva | Spacy')
                    print(start, end)

                    self.certidao = "Positiva"
                    return
                elif string_id == "certidao_negativa":
                    print('033[92mSucesso033[0m: Certidão Negativa | Spacy')
                    print(start, end)

                    self.certidao = "Negativa"
                    return
        else:
            print("Falhou: Certidão | Spacy")
            self.certidao = False

    # @timer_decorator
    def verifica_procuracao_poderes_regex_spacy(self):

        patterns_procuracao = DICT_PATTERN_REGEX["procuracao_poderes"]

        for pattern in patterns_procuracao:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"033[92mSucesso033[0m: Procuração com poderes | REGEX")
                self.procuracao = True
                return

        print('Falhou: Procuração | Regex')
        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["procuracao_poderes"]["pattern1"]

        matcher.add("procuracao", [pattern1])
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                string_id = self.nlp.vocab.strings[match_id]
                if string_id == 'Procuração com poderes encontrada via SPACY':
                    print(f"033[92mSucesso033[0m: Procuração com poderes | Spacy")
                    print(start, end)
                    self.procuracao = True  # Armazena o resultado da verificação
                    return

        else:
            self.procuracao = False

    # @timer_decorator
    def atualiza_natureza_acao(self):
        # Cria dic com crimes e natureza da acao
        crime_dict = {
            'Art. 129, CP': 'Pública condicionada à representação',
            'Art. 129, § 1º, CP': 'Pública condicionada à representação',
            'Art. 129, § 9º, CP': 'Pública condicionada à representação',
            'Art. 139, CP': 'Privada',
            'Art. 140, CP': 'Privada',
            'Art. 147, CP': 'Pública condicionada à representação',
            'Art. 148, § único, CP': 'Pública incondicionada',
            'Art. 150, § 1º, CP': 'Pública condicionada à representação',
            'Art. 155, § 4º, CP': 'Pública incondicionada',
            'Art. 155, § 4º, inciso IV, CP': 'Pública incondicionada',
            'Art. 163, CP': 'Privada',
            'Art. 163, parágrafo único, inciso I, CP': 'Pública incondicionada',
            'Art. 168, CP': 'Pública incondicionada',
            'Art. 171, § 2º, incisos I a VI, CP': 'Pública incondicionada',
            'Art. 180, CP': 'Pública incondicionada',
            'Art. 186, CP': 'Privada',
            'Art. 187, CP': 'Privada',
            'Art. 189, CP': 'Privada',
            'Art. 214 c/ Art. 223, CP': 'Pública incondicionada',
            'Art. 216-A, CP': 'Pública condicionada à representação',
            'Art. 236, CP': 'Pública incondicionada',
            'Art. 237, CP': 'Pública incondicionada',
            'Art. 238, CP': 'Pública incondicionada',
            'Art. 239, CP': 'Pública incondicionada',
            'Art. 240, CP': 'Pública incondicionada',
            'Art. 241, CP': 'Pública incondicionada',
            'Art. 241-A, CP': 'Pública incondicionada',
            'Art. 241-B, CP': 'Pública incondicionada',
            'Art. 241-C, CP': 'Pública incondicionada',
            'Art. 241-D, CP': 'Pública incondicionada',
            'Art. 241-E, CP': 'Pública incondicionada',
            'Art. 243, CP': 'Pública incondicionada',
            'Art. 244-B, CP': 'Pública incondicionada',
            'Art. 247, CP': 'Pública incondicionada',
            'Art. 248, CP': 'Pública incondicionada',
            'Art. 249, CP': 'Pública incondicionada',
            'Art. 250, CP': 'Pública incondicionada',
            'Art. 251, CP': 'Pública incondicionada',
            'Art. 252, CP': 'Pública incondicionada',
            'Art. 253, CP': 'Pública incondicionada',
            'Art. 254, CP': 'Pública incondicionada',
            'Art. 255, CP': 'Pública incondicionada',
            'Art. 331, CP': 'Pública incondicionada',
            'Art. 345, CP': 'Pública incondicionada',
            'Art. 345, §único, CP': 'Privada',
            'Art. 28, Lei 11.343/2006': 'Pública incondicionada',
            'Art. 21, LCP': 'Pública incondicionada',
            'Art. 42, LCP': 'Pública incondicionada'
        }

        self.natureza_acao = []

        if self.infracao_penal is None:
            return

        print(f'Imprimindo infraçoes dentro do metodo atualiza natureza da infração: {self.infracao_penal}')

        # Atualiza self.natureza_acao com base em self.infracao_penal
        for infracao in self.infracao_penal:
            self.natureza_acao.append(
                crime_dict.get(infracao, 'Crime não localizado no Dic'))

    def sanitiza_autor(self, palavra):
        palavra = re.sub(r"AUTOR", "", palavra)

        # lista de palavras para remover
        words_to_remove = ["Autor do Fato", "Autor:", "Autor;", ":"]

                # remove todas as palavras da lista
        for word in words_to_remove:
            palavra = re.sub(word, '', palavra)

        palavra = palavra.title().strip()

        return palavra

    def sanitiza_data(self, palavra):

        # Expressão regular para encontrar datas no formato dd/dd/dd{2-4}
        regex = re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b')

        # Procura pela primeira ocorrência de uma data no texto
        match = regex.search(palavra)

        # Retorna a data encontrada ou None se nenhuma data for encontrada
        return match.group(0) if match else None

    # @timer_decorator
    def verifica_autor_fato(self):

        patterns = DICT_PATTERN_REGEX["nome_autor_fato"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"\033[92mSucesso\033[0m: Nome do Autor do Fato | Regex")
                nome_autor = match.group(1)

                self.nome_autor = nome_autor.title()

                return  # Se uma correspondência foi encontrada, saímos da função
            # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Falhou: Nome Autor | Regex")



        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        patterns_dict = DICT_PATTERN_SPACY["nome_autor_fato"]
        num_patterns = len(patterns_dict)
        patterns = [patterns_dict[f"pattern{i}"] for i in range(1, num_patterns + 1)]
        matcher.add("nome_autor", patterns)

        matches = matcher(doc)

        if matches:
            print("\033[92mSucesso\033[0m: Nome do Autor | Spacy")


            maior_nome = 0
            for match_id, start, end in matches:
                span = doc[start:end]
                # print("Imprimindo span: ", span.text)

                if len(span.text) > maior_nome:
                    maior_nome = len(span.text)


            texto_limpo = self.sanitiza_autor(span.text)
            self.nome_autor = texto_limpo  # Armazena o resultado da verificação
            return

        print("Falhou: Nome do Autor | Spacy")
        return

    def atualiza_todos_atributos(self):

        metodos = [
            self.get_numero_processo,
            self.verifica_proposta_transacao_regex_spacy,
            self.verifica_infracao_penal_regex,
            self.verifica_data_crime_regex_spacy,
            self.verifica_certidao_regex_spacy,
            self.verifica_autor_fato,
            self.verifica_retratacao_regex_spacy,
            self.verifica_sentenca,
            self.verifica_representacao_regex_spacy,
            self.verifica_procuracao_poderes_regex_spacy,
            self.verifica_queixa_crime_regex_spacy
        ]

        threads = [Thread(target=metodo) for metodo in metodos]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.atualiza_natureza_acao()

    def retorna_atributos(self):
        atributos = {
            "Número do Processo": [self.numero_processo],
            "Proposta de Transação": [self.proposta_transacao],
            "Infração Penal": [self.infracao_penal],
            "Data do Crime": [self.data_do_crime],
            "Certidão de Antecedentes": [self.certidao],
            "Natureza da Ação": [self.natureza_acao],
            "Nome do Infrator(a)": [self.nome_autor],
            "Retratação da Representação": [self.retratacao_representacao],
            "Queixa-Crime": [self.queixa_crime],
            "Sentenciado": [self.sentenciado],
            "Representação Criminal": [self.representacao_criminal],
            "Prazo Decadencial": [self.prazo_decadencial],
            "Procuração com Poderes": [self.procuracao],
        }

        df = pd.DataFrame(atributos)
        return df.T
