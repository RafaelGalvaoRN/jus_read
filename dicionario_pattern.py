DICT_PATTERN_REGEX = {

    "proposta_transacao": [
        r'a fim de oportunizar, .quele, a seguinte PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das op..es abaixo,',
        r'oferece PROPOSTA DE TRANSAÇÃO  PENAL a(o) autor(a) do fato, consistente em uma das seguintes propostas:?',
        r'oferece proposta de transacao penal a',
        r'oferece PROPOSTA DE TRANSAÇÃO PENAL a(o) autor(a) do fato,'
        r'PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das opções abaixo:',
        r'oferece PROPOSTA DE TRANSAÇÃO PENAL',
        r"presta..o pecuni.ria, no valor de (.{,70})dividida em, at.,(.{,30})a ser efetuada"
    ],
    "numero_processo": [r"\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}"],

    "nome_autor_fato": [r"(?:\s?autor:?\s?)(\D+?)(?:infra..o penal)",
                        ],

    "infracao_penal": [
        r"(?<=INFRA..O PENAL.)(.{1,100})(?=AUTUA..O\b)",
        r"(?<=infra..o penal.)(.{1,100})(?=Autorizando\b)",
        r"(?<=infra..es penais)(.{1,100})(?=testemunha\(s\))",
        r"(?<=INFRA..ES)(.{1,100})(?=AUTUA..O\b)",
        r"(?<=INFRA..O\(.ES\) PENAL\(IS\):)(.{1,100})(?=AUTUA..O\b)",
        r"(?<=il.cito PENAL)(.{1,100})(?=infratora?:?\b)",
        r"(?<=il.cito PENAL):?(.{1,100})(?=autor? do fato:?\b)",
        r"(?<=enquadramento legal):?(.{1,100})(?=relato\b)",
        r"(?<=il.cito PENAL)(.{1,50})\.",
        r"(?<=enquadramentos legais )(.{1,50})(?=hist.rico da)",
        r"(?<=infra..o penal:)(.{0,50})(?=v.tima)",
        "(?<=infra..o penal)(.{0,50})(?=v.tima)"
    ],
    "crimes": [
        r"(Art\.?\s*\d+\s*.*?\sdo\sCPB?)"
    ],

    "retratacao": [r"se retrata em representar em face do autor do fato",
                   r"se retrata em representar"],

    "sentença": [r"SENTENÇA Vistos etc.,",
                 r"poder judici.rio(.{1,300})processo(.{1,300})senten.a",
                 r"isto posto,?(.+)homologo[o/s]o? pedido de arquivamento",
                 r"DECLARO EXTINTA A PUNIBILIDADE,"
                 ],

    "representacao": [r"representar? criminalmente",
                      r"termo de representação / requerimento"
                      ],

    "queixa_crime": [r"Apresentar queixa[-\s]?crime",
                     ],

    "data_crime": [r"DATA:\s*(\d{2}/\d{2}/\d{4})(?:\s*HORA:\s*\d{2}:\d{2})?\s*LOCAL",
                   r"(?<=data do fato):?\s?(\d{2}/\d{2}/\d{4})\s?(?=hora\b)",
                   r"(?<=data\/hora fim):? (\d{2}/\d{2}/\d{4}).+(?=Delegado\b)"],

    "certidao_positiva": [
        r"certid.o.n..(.+?) Certifico que, pesquisando(.+?) Rio Grande do Norte, ((?!NADA).)*CONSTAR as? distribui.."],
    "certidao_negativa": [
        r"certid.o.n..(.+?) Certifico que, pesquisando(.+?) Rio Grande do Norte, (.+?) NADA CONSTAR em nome de"],
    "procuracao_poderes": [r"procura..(.{1,500})ad judicia(.{1,300})queixa-crime"]

}

DICT_PATTERN_SPACY = {
    "proposta_transacao": {
        "pattern1": [{"LOWER": "oferece"},
                     {"LOWER": "proposta"},
                     {"LOWER": "de"},
                     {"LOWER": "transação"},
                     {"LOWER": "penal"},
                     {"IS_PUNCT": True, "OP": "*"},
                     {"LOWER": {"IN": ["consistente", "a"]}},
                     ],
        "pattern2": [{"LOWER": "oferece"},
                     {"LOWER": "proposta"},
                     {"LOWER": "de"},
                     {"LOWER": "transação"},
                     {"LOWER": "penal"},
                     {"IS_PUNCT": True, "OP": "*"},
                     {"LOWER": "a(o)"},
                     {"LOWER": "autor(a)"},
                     {"LOWER": "do"},
                     {"LOWER": "fato,"},
                     {"LOWER": "consistente"},
                     ],

        "phrase_matcher":
            [
                r'a fim de oportunizar, .quele, a seguinte PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das op..es abaixo,',
                r'oferece PROPOSTA DE TRANSAÇÃO  PENAL a(o) autor(a) do fato, consistente em uma das seguintes propostas:?',
                r'oferece proposta de transacao penal a',
                r'oferece PROPOSTA DE TRANSAÇÃO PENAL a(o) autor(a) do fato,'
                r'PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das opções abaixo:'
            ]

    },
    "retratacao": {
        "pattern1": [{"LOWER": {"IN": ["retratou", "retirou", "desistiu", "retrata"]}},
                     {"IS_PUNCT": True, "OP": "*"},
                     {"LOWER": "se", "OP": "*"},
                     {"IS_PUNCT": True, "OP": "*"},
                     {"LOWER": {"IN": ["da", "a", "o", "em"]}},
                     {"IS_PUNCT": True, "OP": "*"},
                     {"LOWER": {
                         "IN": ["acusação", "representação", "queixa", "denuncia", "depoimento", "representar"]}}]},
    "sentença": {
        "pattern1": [{"LOWER": {"IN": ["sentença"]}},
                     {"LOWER": "vistos"},
                     {"LOWER": "etc"}
                     ],
        "phrase_matcher": [
            "homologo a transação penal realizada nestes autos, aplicando as penas restritivas de direito mencionadas acima"]},
    "representacao": {
        "pattern1": [{"LOWER": {"IN": ["representar", "representação"]}},
                     {"LOWER": {"IN": ["criminal"]}}]
    },
    "queixa_crime": {
        "pattern1": [{"LOWER": {"IN": ["apresentar", "ajuizar", "interpor", "oferecer"]}},
                     {"LOWER": {"IN": ["queixa-crime"]}}]},
    "data_crime": {
        "pattern1":
            [{"LOWER": "data"},
             {"IS_PUNCT": True, "OP": "*"},
             {"SHAPE": {"IN": ["dd/dd/dddd", "dd/dd/dd"]}},
             {"LOWER": "hora:", "OP": "?"},
             {"SHAPE": "dd:dd", "OP": "?"}
             ],
        "pattern2": [
            {"LOWER": "data"},
            {"LOWER": "do"},
            {"LOWER": "fato"},
            {"IS_PUNCT": True, "OP": "*"},
            {"SHAPE": {"IN": ["dd/dd/dddd", "dd/dd/dd"]}},
            {"LOWER": "hora:", "OP": "?"},
        ]

    },
    "certidao_positiva": {
        "pattern1": [
            {"LOWER": "verifiquei"},
            {"LOWER": "constar"},
            {"LOWER": {"IN": ["as", "a"]}},
            {"LOWER": {"IN": ["distribuições", "distribuição"]}},
            {"LOWER": "abaixo"},
            {"LOWER": {"IN": ["relacionadas", "relacionada"]}},
            {"LOWER": "em"},
            {"OP": "*"},
            {"LOWER": "nome"},
            {"LOWER": "de"}
        ]},
    "certidao_negativa": {
        "pattern1": [
            {"LOWER": "verifiquei"},
            {"LOWER": "nada"},
            {"LOWER": "constar"},
            {"LOWER": "em"},
            {"OP": "*"},
            {"LOWER": "nome"},
            {"LOWER": "de"}
        ]},
    "procuracao_poderes": {"pattern1": [
        {"LOWER": "ad"},
        {"LOWER": "judicia"},
        {"LOWER": "et"},
        {"LOWER": "extra"}]},
    "nome_autor_fato":
        {"pattern1": [{"LOWER": "autor"},
                      {"IS_PUNCT": True, "OP": "*"},
                      {"IS_ALPHA": True, "OP": "*"},
                      {"ENT_TYPE": "PER"}],
         "pattern2": [{"LOWER": "autor"},
                      {"IS_SPACE": True, "OP": "*"},
                      {"ENT_TYPE": "PER"}
                      ],
         "pattern3": [{"LOWER": "autor"},
                      {"IS_ALPHA": False, "OP": "*"},
                      {"ENT_TYPE": "PER"}
                      ],
         "pattern4": [{"LOWER": "autor"},
                      {"IS_ASCII": True, "OP": "*"},
                      {"ENT_TYPE": "PER"}
                      ],
         "pattern5": [{"LOWER": {"IN": ["autor", "autor(a)", "autor(a) (es):",
                                        "autor(a)(es):", "autor(a) do fato",
                                        "Autores do Fato:", "Autor do Fato"]}},
                      {"IS_PUNCT": True, "OP": "*"},
                      {"IS_SPACE": True, "OP": "*"},
                      {"ENT_TYPE": "PER"}
                      ],
         "pattern6": [{"LOWER": "autor"},
                      {"IS_PUNCT": True, "OP": "?"},
                      {"IS_SPACE": True, "OP": "?"},
                      {"IS_ALPHA": True, "OP": "{1,10}"}],

         }
}
