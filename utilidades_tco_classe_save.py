import spacy
from spacy import displacy
from spacy.matcher import PhraseMatcher, Matcher
import re
import time
from functools import wraps
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dicionario_pattern import DICT_PATTERN_REGEX, DICT_PATTERN_SPACY


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
        self.nome_autor_spacy = None
        self.retratacao_representacao = None
        self.queixa_crime = None
        self.sentenciado = False
        self.representacao_criminal = None
        self.prazo_decadencial = None
        self.procuracao = None

    def verifica_decadencia_seis_meses(self, data):
        data = data.strip()
        print('entrei no metodo')
        print(data)

        if data is None:
            self.prazo_decadencial = None
            return

        match = re.match(r'\d{2}\/\d{2}\/\d{2,4}', data, re.IGNORECASE)

        print(f'printando match{match}')

        if not match:
            self.prazo_decadencial = None
            return

        try:
            data = datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            data = datetime.strptime(data, "%d/%m/%y")

        data_atual = datetime.now()

        diff = relativedelta(data_atual, data)

        print(f'printando diff{diff}')

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
            match ent.label_:
                case "PER":
                    pessoas.append(ent.text)  # you probably want to append entity text, not label
                case "MISC":
                    miscelaneo.append(ent.text)
                case "ORG":
                    organizacao.append(ent.text)
                case "LOC":
                    localidade.append(ent.text)
                case _:
                    continue  # ignore other labels

        self.per = set(pessoas)
        self.misc = set(miscelaneo)
        self.org = set(organizacao)
        self.loc = set(localidade)

    @timer_decorator
    def verifica_proposta_transacao_regex_spacy(self):
        # patterns = [r'a fim de oportunizar, .quele, a seguinte PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das op..es abaixo,',
        #     r'oferece PROPOSTA DE TRANSAÇÃO  PENAL a(o) autor(a) do fato, consistente em uma das seguintes propostas:?',
        #     r'oferece proposta de transacao penal a',
        #     r'oferece PROPOSTA DE TRANSAÇÃO PENAL a(o) autor(a) do fato,'
        #     r'PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das opções abaixo:',
        #     r'oferece PROPOSTA DE TRANSAÇÃO PENAL',
        #     r"presta..o pecuni.ria, no valor de (.{,70})dividida em, at.,(.{,30})a ser efetuada"
        # ]
        patterns = DICT_PATTERN_REGEX["proposta_transacao"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                result = match.group(0).strip()  # strip() é usado para remover espaços em branco no início e no final
                print(f"Prosta de transação encontrada: '{result}'")

                self.proposta_transacao = True  # Armazena o resultado da verificação
                return

        # passa a analisar pel spacy

        doc = self.nlp.make_doc(self.texto)
        matcher = PhraseMatcher(self.nlp.vocab, attr='LOWER')

        # com matcher
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["proposta_transacao"]["pattern1"]

        # pattern1 = [{"LOWER": "oferece"},
        #             {"LOWER": "proposta"},
        #             {"LOWER": "de"},
        #             {"LOWER": "transação"},
        #             {"LOWER": "penal"},
        #             {"IS_PUNCT": True, "OP": "*"},
        #             {"LOWER": {"IN": ["consistente", "a"]}},
        #             ]

        pattern2 = DICT_PATTERN_SPACY["proposta_transacao"]["pattern2"]

        # pattern2 = [{"LOWER": "oferece"},
        #             {"LOWER": "proposta"},
        #             {"LOWER": "de"},
        #             {"LOWER": "transação"},
        #             {"LOWER": "penal"},
        #             {"IS_PUNCT": True, "OP": "*"},
        #             {"LOWER": "a(o)"},
        #             {"LOWER": "autor(a)"},
        #             {"LOWER": "do"},
        #             {"LOWER": "fato,"},
        #             {"LOWER": "consistente"},
        #             ]

        matcher.add("proposta_transacao", [pattern1, pattern2])
        matches = matcher(doc)

        # com prahse matcher

        pattern_prase_matcher = DICT_PATTERN_SPACY["proposta_transacao"]["prase_matcher"]

        # pattern_prase_matcher = [r'a fim de oportunizar, .quele, a seguinte PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das op..es abaixo,',
        #     r'oferece PROPOSTA DE TRANSAÇÃO  PENAL a(o) autor(a) do fato, consistente em uma das seguintes propostas:?',
        #     r'oferece proposta de transacao penal a',
        #     r'oferece PROPOSTA DE TRANSAÇÃO PENAL a(o) autor(a) do fato,'
        #     r'PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das opções abaixo:'
        # ]

        phrase_patterns = [self.nlp.make_doc(text) for text in pattern_prase_matcher]
        phrase_matcher = PhraseMatcher(self.nlp.vocab)
        phrase_matcher.add("proposta_transacao", phrase_patterns)
        phrase_matches = [(match_id, start, end) for match_id, start, end, label in
                          phrase_matcher(doc)]  # Extraímos somente as partes relevantes

        combined_matches = matches + phrase_matches

        if combined_matches:
            for match_id, start, end in combined_matches:
                span = doc[start:end]
                print('Achei proposta de transacão via SPACY')
                print(start, end, span.text)
            self.proposta_transacao = True  # Armazena o resultado da verificação
            return
        print('Não localizei propsota de transação   pelo Spacy')
        self.proposta_transacao = False

    @timer_decorator
    def verifica_infracao_penal_regex(self):

        # patterns = [
        #     r"(?<=INFRA..O PENAL.)(.{1,100})(?=AUTUA..O\b)",
        #     r"(?<=infra..o penal.)(.{1,100})(?=Autorizando\b)",
        #     r"(?<=infra..es penais)(.{1,100})(?=testemunha\(s\))",
        #     r"(?<=INFRA..ES)(.{1,100})(?=AUTUA..O\b)",
        #     r"(?<=INFRA..O\(.ES\) PENAL\(IS\):)(.{1,100})(?=AUTUA..O\b)",
        #     r"(?<=il.cito PENAL)(.{1,100})(?=infratora?:?\b)",
        #     r"(?<=il.cito PENAL):?(.{1,100})(?=autor? do fato:?\b)",
        #     r"(?<=enquadramento legal):?(.{1,100})(?=relato\b)",
        #     r"(?<=il.cito PENAL)(.{1,50})\.",
        #     r"(?<=enquadramentos legais )(.{1,50})(?=hist.rico da)",
        #     r"(?<=infra..o penal:)(.{0,50})(?=v.tima)",
        #     "(?<=infra..o penal)(.{0,50})(?=v.tima)"
        # ]

        patterns = DICT_PATTERN_REGEX["infracao_penal"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                result = match.group(0).strip()  # strip() é usado para remover espaços em branco no início e no final
                print(f"Infracao penal encontrada: '{result}'")

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
                print(result)

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

                # remove com re.sub, com ignorecase
                crimes_extensos = ['AMEAÇA', 'Lesão corporal dolosa',
                                   'INJÚRIA REAL', '(VIOLÊNCIA CONTRA A MULHER)',
                                   'VIOLÊNCIA CONTRA A MULHER']

                for crime in crimes_extensos:
                    result = re.sub(crime, r'', result, flags=re.IGNORECASE)

                # transforma os crimes em uma lista de crimes
                result = result.split(';')

                # retira o elemento da lista vazia gerado pelo split, quando o ; é o ultimo caractere
                result = [r for r in result if r]

                # retira espacos antes e depois
                result = [r.strip() for r in result]

                # Armazena o resultado da verificação
                self.infracao_penal = result

                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem
        print("Nenhum texto encontrado a título de infração penal")

    @timer_decorator
    def get_ent_spacy(self):
        texto_com_entidades = None  # Valor padrão
        try:
            doc = self.nlp(self.texto)
            texto_com_entidades = displacy.render(doc, style="ent", page=True, jupyter=False)
            return texto_com_entidades
        except Exception as e:
            print(f"Erro ao processar o texto: {e}")

    @timer_decorator
    def verifica_retratacao_regex_spacy(self):

        patterns = DICT_PATTERN_REGEX["retratacao"]

        # patterns = [r"se retrata em representar em face do autor do fato",
        #             r"se retrata em representar",
        #
        #             ]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"Retratação de representação encontrada")
                self.retratacao_representacao = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Nenhum texto encontrado a título de retratacao por meio de regex")
        print("Iniciando pesquisa pelo Spacy")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["retratacao"]["pattern1"]

        # pattern1 = [{"LOWER": { "IN": ["retratou", "retirou", "desistiu", "retrata"]}},
        #             {"IS_PUNCT": True, "OP": "*"},
        #             {"LOWER": "se", "OP": "*"},
        #             {"IS_PUNCT": True, "OP": "*"},
        #             {"LOWER": {"IN": [ "da", "a", "o", "em"]}},
        #             {"IS_PUNCT": True, "OP": "*"},
        #             {"LOWER": {"IN": ["acusação", "representação", "queixa", "denuncia", "depoimento", "representar"]}}]
        #

        matcher.add("retratacao_representacao", [pattern1])

        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                span = doc[start:end]
                print('Achei retratação da representacao via SPACY')
                print(start, end, span.text)
            self.retratacao_representacao = True  # Armazena o resultado da verificação
            return
        print('Não localizei represetanção pelo Spacy')
        self.retratacao_representacao = None
        print('Fim do método - representação setada para None')
        return

    @timer_decorator
    def verifica_sentenca(self):

        patterns = DICT_PATTERN_REGEX["sentença"]

        # patterns = [r"SENTENÇA Vistos etc.,",
        #             r"poder judici.rio(.{1,300})processo(.{1,300})senten.a",
        #             r"isto posto,?(.+)homologo[o/s]o? pedido de arquivamento",
        #             r"DECLARO EXTINTA A PUNIBILIDADE,"
        #             ]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"Sentença encontrada")
                self.sentenciado = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Nenhum texto encontrado a título de sentença por meio de regex")
        print("Iniciando pesquisa pelo Spacy")

        doc = self.nlp.make_doc(self.texto)

        # com matcher
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["sentença"]["pattern1"]

        #
        # pattern1 = [{"LOWER": {"IN": ["sentença"]}},
        #             {"LOWER": "vistos"},
        #             {"LOWER": "etc"}
        #             ]

        matcher.add("sentença", [pattern1])
        matches = matcher(doc)

        # com prahse matcher
        pattern_prase_matcher = [
            "homologo a transação penal realizada nestes autos, aplicando as penas restritivas de direito mencionadas acima"]

        pattern_prase_matcher = DICT_PATTERN_SPACY["sentença"]["prase_matcher"]

        phrase_patterns = [self.nlp.make_doc(text) for text in pattern_prase_matcher]
        phrase_matcher = PhraseMatcher(self.nlp.vocab)
        phrase_matcher.add("sentença", phrase_patterns)
        phrase_matches = [(match_id, start, end) for match_id, start, end, label in
                          phrase_matcher(doc)]  # Extraímos somente as partes relevantes

        combined_matches = matches + phrase_matches

        if combined_matches:
            for match_id, start, end in combined_matches:
                span = doc[start:end]
                print('Achei sentença via SPACY')
                print(start, end, span.text)
            self.sentenciado = True  # Armazena o resultado da verificação
            return
        print('Não localizei sentença pelo Spacy')
        return

    @timer_decorator
    def verifica_representacao_regex_spacy(self):

        # patterns = [r"representar? criminalmente",
        #             r"termo de representação / requerimento"
        #             ]

        patterns = DICT_PATTERN_REGEX["representacao"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"Representação encontrada")
                self.representacao_criminal = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Nenhum texto encontrado a título de representação por meio de regex")
        print("Iniciando pesquisa pelo Spacy")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["representacao"]["pattern1"]

        # pattern1 = [{"LOWER": { "IN": ["representar", "representação"]}},
        #             {"LOWER": {"IN": [ "criminal"]}}]

        matcher.add("representação criminal", [pattern1])

        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                span = doc[start:end]
                print('Achei representação criminal via SPACY')
                print(start, end, span.text)
            self.representacao_criminal = True  # Armazena o resultado da verificação
            return
        print('Não localizei representação criminal pelo Spacy')
        self.representacao_criminal = False
        return

    @timer_decorator
    def verifica_queixa_crime_regex_spacy(self):

        # patterns = [r"Apresentar queixa[-\s]?crime",
        #             ]

        patterns = DICT_PATTERN_REGEX["queixa_crime"]

        for pattern in patterns:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"Queixa Crime encontrada")
                self.queixa_crime = True  # Armazena o resultado da verificação
                return  # Se uma correspondência foi encontrada, saímos da função
        # Se nenhuma correspondência foi encontrada para nenhum dos padrões, imprimimos uma mensagem e continuamos com método spacy
        print("Nenhum texto encontrado a título de queixa-crime por meio de regex")
        print("Iniciando pesquisa pelo Spacy")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["queixa_crime"]["pattern1"]

        # pattern1 = [{"LOWER": { "IN": ["apresentar", "ajuizar", "interpor", "oferecer"]}},
        #             {"LOWER": {"IN": [ "queixa-crime"]}}]
        #

        matcher.add("queixa-crime", [pattern1])

        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                span = doc[start:end]
                print('Achei queixa-crime  via SPACY')
                print(start, end, span.text)
            self.queixa_crime = True  # Armazena o resultado da verificação
            return
        print('Não localizei queixa-crime pelo Spacy')
        self.queixa_crime = None
        return

    @timer_decorator
    def verifica_data_crime_regex_spacy(self):
        # patterns = [ r"DATA:\s*(\d{2}/\d{2}/\d{4})(?:\s*HORA:\s*\d{2}:\d{2})?\s*LOCAL",
        #              r"(?<=data do fato):?\s?(\d{2}/\d{2}/\d{4})\s?(?=hora\b)",
        #              r"(?<=data\/hora fim):? (\d{2}/\d{2}/\d{4}).+(?=Delegado\b)"]

        patterns = DICT_PATTERN_REGEX["data_crime"]

        for pattern in patterns:
            # Use re.search para encontrar a correspondência
            match = re.search(pattern, self.texto, re.IGNORECASE)
            # Se uma correspondência foi encontrada, imprima-a
            if match:
                date = match.group(1)  # group(1) pega o primeiro grupo capturado, que é a data
                print(f"Data do crime encontrada: {date}")

                self.data_do_crime = date

                # atualiza prazo de decadencia
                self.verifica_decadencia_seis_meses(self.data_do_crime)
                return

        print("Nenhuma data encontrada para o crime via regex")
        print("Iniciando pesquisa de data do crime via SPACY")

        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)
        # pattern = [
        #     {"LOWER": "data"},
        #     {"IS_PUNCT": True, "OP": "*"},
        #     {"SHAPE": {"IN": ["dd/dd/dddd", "dd/dd/dd"]}},
        #     {"LOWER": "hora:", "OP": "?"},
        #     {"SHAPE": "dd:dd", "OP": "?"}
        # ]

        pattern1 = DICT_PATTERN_SPACY["data_crime"]["pattern1"]
        pattern2 = DICT_PATTERN_SPACY["data_crime"]["pattern2"]

        #
        # pattern2 = [
        #     {"LOWER": "data"},
        #     {"LOWER": "do"},
        #     {"LOWER": "fato"},
        #     {"IS_PUNCT": True, "OP": "*"},
        #     {"SHAPE": {"IN": ["dd/dd/dddd", "dd/dd/dd"]}},
        #     {"LOWER": "hora:", "OP": "?"},
        # ]

        matcher.add("data_crime_localizada_spacy", [pattern1, pattern2])
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                span = doc[start:end]
                print(start, end, span.text)

                # lista de palavras para remover
                words_to_remove = ["Data", "DATA:",
                                   "Data:",
                                   'data', "Data:", ":", "hora",
                                   "DATA;"]
                result = span.text

                # remove todas as palavras da lista
                for word in words_to_remove:
                    result = re.sub(word, '', result)

            self.data_do_crime = result  # Armazena o resultado da verificação

            # atualiza prazo de decadencia
            self.verifica_decadencia_seis_meses(self.data_do_crime)

            return

        self.data_do_crime = None  # Armazena o resultado da verificação se nenhuma condição for satisfeita

    @timer_decorator
    def verifica_certidao_regex_spacy(self):
        # patterns_certidao_positiva = r"certid.o.n..(.+?) Certifico que, pesquisando(.+?) Rio Grande do Norte, ((?!NADA).)*CONSTAR as? distribui.."
        # patterns_certidao_negativa = r"certid.o.n..(.+?) Certifico que, pesquisando(.+?) Rio Grande do Norte, (.+?) NADA CONSTAR em nome de"

        patterns_certidao_positiva = DICT_PATTERN_REGEX["certidao_positiva"]
        patterns_certidao_negativa = DICT_PATTERN_REGEX["certidao_negativa"]

        for pattern in patterns_certidao_positiva:
            match_positiva = re.search(pattern, self.texto, re.IGNORECASE)
            if match_positiva:
                print(f"Certidão positiva encontrada!")
                self.certidao = "Positiva"
                return

        for pattern in patterns_certidao_negativa:
            match_negativa = re.search(pattern, self.texto, re.IGNORECASE)
            if match_negativa:
                print(f"Certidão negativa encontrada!")
                self.certidao = "Negativa"
                return

        print('Certidão não encontrada com regex. Iniciando pesquisa com Spacy')
        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)
        pattern_postiva = DICT_PATTERN_SPACY["certidao_positiva"]["pattern1"]

        # pattern_postiva = [
        #     {"LOWER": "verifiquei"},
        #     {"LOWER": "constar"},
        #     {"LOWER":  {"IN": ["as", "a"]}},
        #     {"LOWER": {"IN": ["distribuições", "distribuição"]}},
        #     {"LOWER": "abaixo"},
        #     {"LOWER": {"IN": ["relacionadas", "relacionada"]}},
        #     {"LOWER": "em"},
        #     {"OP": "*"},
        #     {"LOWER": "nome"},
        #     {"LOWER": "de"}
        # ]

        pattern_negativa = DICT_PATTERN_SPACY["certidao_negativa"]["pattern1"]

        # pattern_negativa = [
        #     {"LOWER": "verifiquei"},
        #     {"LOWER": "nada"},
        #     {"LOWER": "constar"},
        #     {"LOWER": "em"},
        #     {"OP": "*"},
        #     {"LOWER": "nome"},
        #     {"LOWER": "de"}
        # ]

        matcher.add("certidao_positiva", [pattern_postiva])
        matcher.add("certidao_negativa", [pattern_negativa])
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                string_id = self.nlp.vocab.strings[match_id]
                if string_id == 'certidao_positiva':
                    print('Imprimindo match para certidão positiva')
                    print(start, end)

                    self.certidao = "Positiva"
                    return
                elif string_id == "certidao_negativa":
                    print('Imprimindo match para certidão negativa')
                    print(start, end)

                    self.certidao = "Negativa"
                    return
        else:

            self.certidao = None

    @timer_decorator
    def verifica_procuracao_poderes_regex_spacy(self):
        # pattern_procuracao = r"procura..(.{1,500})ad judicia(.{1,300})queixa-crime"
        #
        # match_procuracao_poderes = re.search(pattern_procuracao, self.texto, re.IGNORECASE)
        #
        # # Se uma correspondência foi encontrada, imprima-a
        # if match_procuracao_poderes:
        #     print(f"Procuracão com poderes encontrada!")
        #     self.procuracao = True
        #     return

        patterns_procuracao = DICT_PATTERN_REGEX["procuracao_poderes"]

        for pattern in patterns_procuracao:
            match = re.search(pattern, self.texto, re.IGNORECASE)
            if match:
                print(f"Procuracão com poderes encontrada!")
                self.procuracao = True
                return

        print('Procuração não encontrada com regex. Iniciando pesquisa com Spacy')
        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        # pattern_postiva = [
        #
        #     {"LOWER": "ad"},
        #     {"LOWER": "judicia"},
        #     {"LOWER": "et"},
        #     {"LOWER": "extra"}]

        pattern1 = DICT_PATTERN_SPACY["procuracao_poderes"]["pattern1"]

        matcher.add("procuracao", [pattern1])
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                string_id = self.nlp.vocab.strings[match_id]
                if string_id == 'Procuração com poderes encontrada':
                    print('Imprimindo match para procuração ')
                    print(start, end)
                    self.procuracao = True  # Armazena o resultado da verificação
                    return

        else:
            self.procuracao = None

    @timer_decorator
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

    @timer_decorator
    def verifica_autor_fato(self):
        doc = self.nlp.make_doc(self.texto)
        matcher = Matcher(self.nlp.vocab)

        pattern1 = DICT_PATTERN_SPACY["nome_autor_fato"]["pattern1"]
        pattern2 = DICT_PATTERN_SPACY["nome_autor_fato"]["pattern2"]
        pattern3 = DICT_PATTERN_SPACY["nome_autor_fato"]["pattern3"]
        pattern4 = DICT_PATTERN_SPACY["nome_autor_fato"]["pattern4"]
        pattern5 = DICT_PATTERN_SPACY["nome_autor_fato"]["pattern5"]

        #
        #
        # patter_nome_autor = [
        #     {"LOWER": "autor"},
        #     {"IS_PUNCT": True, "OP": "*"},
        #     {"IS_ALPHA": True, "OP": "*"},
        #     {"ENT_TYPE": "PER"}
        # ]
        #
        # patter_nome_autor2 = [
        #     {"LOWER": "autor"},
        #     {"IS_SPACE": True, "OP": "*"},
        #     {"ENT_TYPE": "PER"}
        # ]
        #
        # patter_nome_autor3 = [
        #     {"LOWER": "autor"},
        #     {"IS_ALPHA": False, "OP": "*"},
        #     {"ENT_TYPE": "PER"}
        # ]
        #
        # patter_nome_autor4 = [
        #     {"LOWER": "autor"},
        #     {"IS_ASCII": True, "OP": "*"},
        #     {"ENT_TYPE": "PER"}
        # ]
        # patter_nome_autor5 = [
        #     {"LOWER": {"IN": ["autor", "autor(a)", "autor(a) (es):",
        #                       "autor(a)(es):", "autor(a) do fato",
        #                       "Autores do Fato:"]}},
        #     {"IS_PUNCT": True, "OP": "*"},
        #     {"IS_SPACE": True, "OP": "*"},
        #     {"ENT_TYPE": "PER"}
        # ]

        matcher.add("nome_autor", [pattern1, pattern2,
                                   pattern3, pattern4,
                                   pattern5])
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                string_id = self.nlp.vocab.strings[match_id]
                span = doc[start:end]
                print(f'Imprimindo nome do autor localizado: ')
                print(start, end, span.text)

                # lista de palavras para remover
                words_to_remove = ["Autor do Fato", "Autor:", "Autor;"]
                texto_limpo = span.text

                # remove todas as palavras da lista
                for word in words_to_remove:
                    texto_limpo = re.sub(word, '', span.text)

                self.nome_autor_spacy = texto_limpo  # Armazena o resultado da verificação


