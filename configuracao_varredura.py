

# Cria um dicionário de configuração para cada ato processual
CONFIG_GERAL = {
    'sentenca': {
        'keywords': ['sentença', 'publique-se'],
        'phrases': ['DECLARO EXTINTA A PUNIBILIDADE',
                    'HOMOLOGO o pedido de arquivamento do inquérito policial',
                    'DECLARO EXTINTA A PENA',
                    ' o Ministério Público pugnou pela extinção da punibilidade pelo',
                    ' com fundamento nos arts. 107, IV, e 109, III, ambos do Código ',
                    'HOMOLOGO o pedido de arquivamento do procedimentoinvestigatório criminal formulado pelo parquet,',
                    ',DECLARO EXTINTA A PUNIBILIDADE, mediante realização da transação penal pelo autor do fato',
                    'com fundamento nos arts. 28 c/c art. 395, inciso III, todos doCódigo de Processo Penal, HOMOLOGO o pedido de arquivamento do ',
                    'tem-se que o prazo trienal de prescrição entre a data do fato e a presente data, já se ultimou',
                    'Diante do exposto, em consonância com o parecer ministerial e, com fundamento no art. 107, V, do Código Penal , DECLARO EXTINTA A PUNIBILIDADE ',
                    'determino o ARQUIVAMENTO do inquérito em exame, ressalvando-se o',
                    'DETERMINO O ARQUIVAMENTO, impondo-se a extinção do feito,',
                    'há deser deferido o pedido de arquivamento do presente procedimento. determino o ARQUIVAMENTO do inquérito em exame, ressalvando-se o ISTO POSTO,disposto no artigo 18 do Código de Processo Penal e na Súmula 524 do STF, ',
                    'ATO ORDINATÓRIOFicam as partes intimadas da sentença condenatória',
                    'determino a abertura de vista dos',
                    'Nada mais havendo, a audiência foi encerrada',
                    'Devolução de precatoria',
                    'foi aberta a audiência',
                    'DETERMINO O ARQUIVAMENTO DO PRESENTE INQUÉRITO POLICIAL,'],
        'exclude': ['determino a abertura de vista dos autosao Ministério Público para apresentar manifestação',
                    'determino a abertura de vista dos autos ao Ministério Público para apresentar manifestação',
                    'determino a abertura de vista dos autosao Ministério Público para apresentar manifestação. Nada mais havendo, a audiência foi encerrada. ',
                    'determino a abertura de vista dos autos ao Ministério Público para apresentar manifestação. Nada mais havendo, a audiência foi encerrada. ',
                    'vista dos autos ao Ministério Público para requerer o que entenderde direito',
                    'vista dos autos ao Ministério Público para requerer o que entender de direito',
                    'DESPACHODetermino a abertura de vista dos autos ao Ministério Público para se manifestar, ',
                    'apresentar contrarrazões aorecurso no prazo legal.Após, ',
                    'abertura de vista dos autos ao Ministério Público',
                    'determino a abertura de vista dos autos ao']

    },
    'audiencia': {
        'keywords': ['intimação', 'audiência'],
        'phrases': ['reaprazada',
                    'híbrida',
                    'VIRTUAL',
                    ' determino o aprazamento de audiência deinstrução e julgamento',
                    'Soldado PMSetor de Pessoal da 10ª CIPMEm ',
                    'A Defensoria Pública manifesta ciência da audiência de instrução e julgamento aprazada.',
                    'dar ciência da audiência designada',
                    'MUTIRÃO DE AUDIÊNCIA DE CONCILIAÇÃO DO JUIZADO ESPECIAL',
                    'Fica(m) intimada(s) a(s) parte(s), abaixo mencionada(s) para participar(em) da Audiência PRELIMINAR de forma',
                    'Fica(m) intimada(s) a(s) parte(s), abaixo mencionada(s) para participar(em) da Audiência de Instrução designada para o dia',
                    "PRONTIFICOU-SE DE PARTICIPAR DA REFERIDA AUDIENCIA. "],
        'exclude': [' procedo a juntada do(s) arquivo(s) audiovisual(is) da  Audiência de Instrução realizada no dia ',
                    'em razão de meu ofício, que procedo a juntada do(s) arquivo(s)audiovisual(is) da  realizada no dia',
                    'Juíza determinou a conclusão dos autos para decisão',
                    ' Nada mais foi requerido, sendo determinado o encerramento do ato,',
                    'CERTIDÃO DE JUNTADA DE ARQUIVO(S) AUDIOVISUAL(IS) DE AUDIÊNCIA',
                    'INDEFIRO o pedido de relaxamento de prisão preventiva',
                    'REVOGO A PRISÃO PREVENTIVA',
                    'Nada mais havendo, a audiência foi encerrada.',
                    'Ministério Público para apresentar manifestação. ',
                    'não consta oferecimento de proposta de transação penal',
                    'determinou a abertura de vista dos autos ao Ministério Público para,',
                    'Audiência Ata da Audiência',
                    'Carta Precatória Criminal',
                    'determinou a abertura de vista dos autos ao Ministério Público',
                    'visto que a peça pórtica não é manifestamente inepta, não falta pressuposto processual,condição da ação ou justa causa ao exercício da ação',
                    "verifica-se que o autuado cumpriu integralmente a obrigação",
                    "HOMOLOGO a composição de danos civis ",
                    "DECLARO EXTINTA A PUNIBILIDADE"]
    },
    'contrarrazoes': {
        'keywords': ['contrarrazões'],
        'phrases': ['para fins de oferecimento dascontrarrazões, no prazo de 08 (oito) dias.Canguaretama']
    },
    'prescricao': {
        'keywords': ['prescrição'],
        'phrases': [],
        'exclude': ['determino o aprazamento de audiência deinstrução e julgamento',
                    'visto que a peça pórtica não é manifestamente inepta, não falta pressuposto',
                    'Devolução de precatoria',
                    'DECLARO EXTINTA A PUNIBILIDADE',
                    ' É o relatório. Fundamento e decido.Consoante o que dispõe o art. 397 do Código de Processo Penal, após aapresentação da resposta à acusação por parte do réu, o juiz deverá absolver sumariamenteo acusado quando verificar a existência manifesta de causa excludente da ilicitude do fato, a existência manifesta de causa excludente da culpabilidade do agente, que o fato narrado, bem assim esteja . evidentemente não constitui crime extinta a punibilidade',
                    'e por tudo mais que dos autos consta, determino o aprazamento deaudiência de instrução e',
                    'FIXO a pena-base em']
    },
    'denuncia': {
        'keywords': ['Inquérito Policial', 'Requerimento', 'Denúncia'],
        'exclude': ['Requerimento e/ou DenúnciaCanguaretama'],
    },
    'anpp': {
        'keywords': ['HOMOLOGO O ACORDO DE NÃO PERSECUÇÃO PENAL'],
    },
    'inquerito': {
        'keywords': ['autuado(a)', 'inquérito policial'],
    },
    'ciencia_mpu': {
        'keywords': ['ofendida ', 'Lei Maria da Penha', 'medidas protetivas de urgência'],
        'phrases': ['DEFIRO o pedido de liminar e concedo as seguintes medidas protetivas',
                    'O pedido possui amparo legal no artigo 22, incisos III, alíneas a, b e c, da Lei nº 11.340/2006',
                    'DEFIRO o pedido de liminar e concedo as seguintes medidas protetivasprevistas no art. 22 da Lei 11.340/2006:1)'],
    },

    'proposta_transacao': {
        'keywords': ['jdsahfgghkjahgskjhahgjkd'],
        "phrases": [
            ' a fim de oportunizar, àquele, a seguinte PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das opções abaixo,',
            'oferece PROPOSTA DE TRANSAÇÃO  PENAL a(o) autor(a) do fato, consistente em uma das seguintes propostas:',
            'oferece proposta de transacao penal a',
            'oferece PROPOSTA DE TRANSAÇÃO PENAL a(o) autor(a) do fato,'
            'PROPOSTA DE TRANSAÇÃO PENAL, consistente na escolha de uma das opções abaixo:'
        ],
        "exclude": []
    },

    'vista_simples': {
        'keywords': ['jdsahfgghkjahgskjhahgjkd'],
        "phrases": [
            'ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a) Representante do Ministério Público desta Comarca, para fins de parecer, e/ou requerer o que entender de direito.',
            'a abertura de vista dos autos ao Ministério Público para se manifestar no prazo de 10 (dez)dias, requerendo o que entender de',
            'e na permissibilidade do Provimento nº 12, de 02 de agosto de 2005, arts. 1º e 2º,Inciso I, da Corregedoria da Justiça do RN, ABRO VISTA destes autos',
            ' ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a)Representante do Ministério Público desta Comarca, para fins de parecer, e/ou requerer o que entender de ',
            'ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a) Representante doMinistério Público desta Comarca, para fins de parecer, e/ou requerer o que entender de',
            'ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a)Representante do Ministério Público desta Comarca, para fins de parecer, e/ou requerer o que entender de direito.Canguaretama',
            'ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a) Representante doMinistério Público desta Comarca, para fins de parecer, e/ou requerer o que entender de direito.Canguaretama'],
        "exclude": []
    },

    'decisao_recebimento_denuncia': {
        'keywords': ['jdsahfgghkjahgskjhahgjkd'],
        "phrases": [
            'visto que a peça pórtica não é manifestamente inepta, não falta pressuposto processual,condição da ação ou justa causa ao exercício da ação',
            'em apreço, não foram levantadas quaisquer das hipóteses elencadas no art. 397 doCPP, que importem a absolvição sumária do',
            'Os elementos de prova até então produzidos não permitem firmar convicção decerteza em torno da pretensão punitiva estatal. Daí porque adequada se apresenta a',
            'Decido.Consoante o que dispõe o art. 397 do Código de Processo Penal, após aapresentação da resposta à acusação por parte do réu, o juiz deverá absolver sumariamente o acusado quando verificar a existência manifesta de causa excludente da ilicitude do fato,a existência manifesta de causa excludente da culpabilidade do agente ,que o fato narrado evidentemente não constitui crime , bem assim esteja extinta a punibilidade doagente.No',
            'Os elementos de prova até então produzidos não permitem firmar convicção decerteza em torno da pretensão punitiva estatal. Daí porque adequada se apresenta a dilaçãoprobatória.Por'],
        "exclude": []
    },

    'fazer_alegacoes_finais': {
        'keywords': ['abro', "vista", "oferecimento", "alegações", "finais", "prazo", "05", "dias"],
        "phrases": [
            ' ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a) Representante do Ministério Público desta Comarca, para fins de alegações finais, e/ou requerer o que entender de direito.',
            "ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a) Representante do Ministério Público desta Comarca, para fins de oferecimento das alegações finais, no prazo de 05 (cinco) dias."],
        "exclude": []
    },

'tomar_ciencia_decisao': {
        'keywords': ["lkjdklsajdlksajkdlajkdljaskdj"],
        "phrases": ['Pelo exposto, MANTENHO a prisão preventiva de'],
        "exclude": ["ABRO VISTA destes autos a(o) Excelentíssimo(a) Senhor(a) Representante doMinistério Público desta Comarca, para fins de parecer,"]
    },
    'sentenca_transacao': {
        'keywords': ['juizado', 'homologo'],
        'phrases': ['DECLARO EXTINTA A PUNIBILIDADE',
                    'Dispensado o relatório, nos termos do artigo 81',
                    'DECLARO EXTINTA A PENA',
                    'O(a) representante do Ministério Público propôs a transação penal nos termos do art. 76 da Lei no 9.099/95.',
                    ' o Ministério Público pugnou pela extinção da punibilidade pelo',
                    'Ciência ao MP. Após, arquive-se o presente TCO',
                    'HOMOLOGO o pedido de arquivamento do Termo Circunstanciado de Ocorrência formulado pelo Parquet,',
                    ',DECLARO EXTINTA A PUNIBILIDADE, mediante realização da transação penal pelo autor do fato',
                    'com fundamento nos arts. 28 c/c art. 395, inciso III, todos doCódigo de Processo Penal, HOMOLOGO o pedido de arquivamento do ',
                    'ATO ORDINATÓRIOFicam as partes intimadas da sentença condenatória',
                    'Nada mais havendo, a audiência foi encerrada',
                    'Ministério Público para apresentar manifestação. Nada mais havendo, a audiência foi encerrada. ',
                    'por ordem da MM. Juíza, determino a abertura de vista dos',
                    'DETERMINO O ARQUIVAMENTO DO PRESENTE INQUÉRITO POLICIAL,'],
        'exclude': ['determino a abertura de vista dos autosao Ministério Público para apresentar manifestação',
                    'determino a abertura de vista dos autos ao Ministério Público para apresentar manifestação',
                    'determino a abertura de vista dos autosao Ministério Público para apresentar manifestação. Nada mais havendo, a audiência foi encerrada. ',
                    'determino a abertura de vista dos autos ao Ministério Público para apresentar manifestação. Nada mais havendo, a audiência foi encerrada. ',
                    'vista dos autos ao Ministério Público para requerer o que entenderde direito',
                    'vista dos autos ao Ministério Público para requerer o que entender de direito',
                    'DESPACHODetermino a abertura de vista dos autos ao Ministério Público para se manifestar, ',
                    'apresentar contrarrazões aorecurso no prazo legal.Após, ',
                    'abertura de vista dos autos ao Ministério Público',
                    'determino a abertura de vista dos autos ao']

    }
}
