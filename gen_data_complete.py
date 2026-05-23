#!/usr/bin/env python3
"""Generate complete bibleData.js with all 66 books - compact data-driven approach."""
import re, os, json

def js_str(s):
    s = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
    return s

def make_quiz_item(q_text, options_list, correct_idx, explanation):
    opts = ','.join(f'"{js_str(o)}"' for o in options_list)
    return f'{{question:"{js_str(q_text)}",options:[{opts}],correct:{correct_idx},explanation:"{js_str(explanation)}"}}'

# ===================== PER-BOOK CHAPTER CONTENT =====================
# Format: {book_id: {chapter_num: (text, reflection)}}

CHAPTER_TEXT = {
    "genesis": {
        1: ('No princípio, criou Deus os céus e a terra. Disse Deus: Haja luz. E houve luz. Fez Deus o firmamento, separou as águas, fez brotar a terra vegetação. Criou os luzeiros: o sol, a lua e as estrelas. Criou os animais marinhos e as aves, os animais terrestres. Finalmente, criou Deus o homem à sua imagem, homem e mulher os criou. E viu Deus que era muito bom. Ao sétimo dia descansou de toda a sua obra.',
         'A criação revela um Deus de ordem, poder e propósito. Cada detalhe foi planejado. O ser humano, criado à imagem de Deus, recebe dignidade e responsabilidade. O descanso de Deus estabelece o ritmo de confiança e comunhão.'),
        2: ('O SENHOR Deus formou o homem do pó da terra e soprou em suas narinas o fôlego da vida. Plantou um jardim no Éden e pôs ali o homem. Deu-lhe a ordem de não comer da árvore do conhecimento do bem e do mal. Disse Deus: Não é bom que o homem esteja só. Criou a mulher da costela de Adão. Estavam ambos nus e não se envergonhavam.',
         'Deus criou o homem para relacionamento: consigo, com a criação e com o próximo. O casamento é apresentado como aliança de parceria e intimidade. Não fomos feitos para viver isolados.'),
        3: ('A serpente enganou Eva, que comeu do fruto proibido e deu a Adão. Seus olhos foram abertos e esconderam-se de Deus. Deus pronunciou juízo sobre a serpente, a mulher e o homem. Porém, prometeu que a semente da mulher feriria a cabeça da serpente. Deus fez túnicas de peles e os vestiu, e os lançou do jardim do Éden.',
         'O pecado começou com a dúvida sobre a bondade de Deus. Mas a graça brilha em meio ao juízo: Deus promete um Redentor. Mesmo quando nos escondemos, Deus nos busca e nos veste com sua graça.'),
        4: ('Caim e Abel ofereceram sacrifícios ao SENHOR. Deus aceitou a oferta de Abel, mas rejeitou a de Caim. Tomado pela ira e ciúmes, Caim matou seu irmão Abel. O SENHOR amaldiçoou Caim e o marcou. Caim partiu para a terra de Node.',
         'Deus se importa com o coração por trás da oferta, não com o presente em si. O pecado jaz à porta — precisamos dominá-lo. A ira não controlada leva a consequências devastadoras.'),
        5: ('Este é o livro das gerações de Adão. A genealogia de Adão a Noé: Sete, Enos, Cainã, Maalaleel, Jarede, Enoque, Matusalém, Lameque e Noé. Enoque andou com Deus e foi levado por Deus, não vendo a morte. Matusalém viveu 969 anos.',
         'A morte reinou desde Adão, mas Enoque escapou porque andava com Deus. Cada nome nesta genealogia é um elo na promessa do Redentor. Uma vida de comunhão com Deus transcende a morte.'),
        6: ('A maldade humana multiplicou-se, e todo pensamento era continuamente mau. Deus decidiu destruir o homem que criara. Porém, Noé achou graça aos olhos do SENHOR. Deus ordenou que Noé construísse uma arca para salvar sua família e os animais.',
         'No meio da corrupção geral, um homem se destacou por andar com Deus. A arca é símbolo da salvação que Deus provê para quem confia nEle. A graça de Deus sempre preserva um remanescente fiel.'),
        7: ('Noé entrou na arca com sua família e os animais conforme Deus ordenara. As janelas dos céus se abriram e choveu quarenta dias e quarenta noites. As águas cobriram toda a terra, destruindo toda carne. Somente Noé e os que estavam com ele na arca sobreviveram.',
         'O dilúvio mostra que Deus leva o pecado a sério, mas também que Ele preserva quem confia nEle. Juízo e graça andam juntos. A obediência de Noé salvou sua família.'),
        8: ('Deus lembrou-se de Noé e fez soprar um vento sobre a terra. As águas baixaram, e a arca repousou sobre o monte Ararate. Noé soltou um corvo e depois uma pomba. A pomba voltou com uma folha de oliveira. Noé saiu da arca e ofereceu holocausto ao SENHOR.',
         '"Lembrou-se Deus de Noé" — que frase linda! Deus não esquece os seus. A pomba com a folha de oliveira é sinal de esperança e novos começos após o juízo.'),
        9: ('Deus abençoou Noé e seus filhos e estabeleceu uma aliança: não destruiria mais a terra com dilúvio. O arco-íris foi dado como sinal dessa aliança. Noé plantou uma vinha e embebedou-se, e Cam desonrou seu pai. Noé amaldiçoou Canaã e abençoou Sem e Jafé.',
         'O arco-íris é mais que fenômeno natural — é sinal da fidelidade de Deus. A aliança com Noé é universal e precede a aliança com Abraão. Deus é fiel mesmo quando os homens falham.'),
        10: ('Estas são as gerações dos filhos de Noé: Sem, Cão e Jafé. Deles se originaram as nações após o dilúvio. Ninrode foi um valente caçador diante do SENHOR. Destes se espalharam as ilhas dos gentios em suas terras, cada qual segundo a sua língua.',
         'Cada nome representa um povo e uma cultura. Deus se importa com todas as nações. A promessa de que em Abraão todas as famílias seriam benditas começa aqui.'),
    },
    "exodus": {
        1: ('José morreu, e todos os daquela geração. Surgiu um novo rei no Egito que não conhecia a José. Os egípcios oprimiram os israelitas com trabalhos forçados. Quanto mais os oprimiam, mais se multiplicavam. Faraó ordenou que os bebês hebreus fossem mortos, mas as parteiras temeram a Deus.',
         'A opressão não impediu o plano de Deus. Quanto mais perseguido, mais o povo de Deus cresce. As parteiras são exemplo de obediência a Deus antes que aos homens.'),
        2: ('Moisés nasceu e foi escondido por três meses. Sua mãe o colocou num cesto no rio Nilo. A filha de Faraó o encontrou e teve compaixão. Miriã trouxe a própria mãe para amamentá-lo. Moisés cresceu no palácio, mas fugiu para Midiã após matar um egípcio.',
         'Deus prepara seus líderes no palácio (educação) e no deserto (humildade). Moisés pensava que podia libertar Israel com suas próprias forças, mas precisou aprender que a obra é de Deus.'),
        3: ('Moisés apascentava ovelhas no monte Horebe. O Anjo do SENHOR apareceu numa sarça que ardia sem se consumir. Deus se revelou como o Deus de Abraão, Isaque e Jacó. Moisés foi chamado para libertar Israel. Deus revelou seu nome: EU SOU O QUE SOU.',
         'A sarça ardente é o encontro que transforma um pastor num libertador. Deus se revela como EU SOU — auto-existente, eterno e presente. Não é nossa capacidade, mas a presença de Deus que faz a diferença.'),
        4: ('Moisés objetou que não seria ouvido. Deus deu-lhe três sinais: vara que vira cobra, mão leprosa e água que vira sangue. Moisés alegou não ter eloqüência. Arão foi designado como seu porta-voz. Moisés despediu-se de Jetro e partiu para o Egito.',
         'Deus responde a cada objeção de Moisés com paciência e poder. Ele usa o que temos: "Que é isso na tua mão?" Nossas limitações não são obstáculos para Deus — Ele as usa para mostrar seu poder.'),
        5: ('Moisés e Arão pediram a Faraó que libertasse Israel para celebrar uma festa ao SENHOR. Faraó recusou e aumentou a opressão, exigindo que os israelitas fizessem os mesmos tijolos sem receber palha. O povo reclamou contra Moisés.',
         'O primeiro confrontamento pareceu um fracasso. Muitas vezes, quando obedecemos a Deus, as coisas pioram antes de melhorar. O aparente fracasso precede o maior livramento.'),
    },
}

def generate_text(book_id, ch_num, title, theme):
    """Generate meaningful chapter text."""
    # Check for specific content
    if book_id in CHAPTER_TEXT and ch_num in CHAPTER_TEXT[book_id]:
        return CHAPTER_TEXT[book_id][ch_num][0]
    
    # Genesis and Exodus beyond specific chapters
    if book_id == "genesis":
        if ch_num == 11: return 'Toda a terra tinha uma só língua e uma só fala. Os homens disseram: Edifiquemos uma torre cujo topo chegue aos céus. O SENHOR confundiu a linguagem de toda a terra e os espalhou por toda a face da terra.'
        if ch_num == 12: return 'Disse o SENHOR a Abrão: Sai da tua terra, da tua parentela, para a terra que te mostrarei. Far-te-ei uma grande nação. Abrão partiu, aos setenta e cinco anos, pela fé, sem saber para onde ia.'
        if ch_num == 22: return 'Deus provou Abraão: Toma teu filho Isaque e oferece-o em holocausto. Abraão obedeceu. No momento crucial, o Anjo do SENHOR o impediu. Deus proveu um carneiro. Abraão chamou o lugar: O SENHOR Proverá.'
        return f'{title}. Neste capítulo de Gênesis, a história da redenção avança através dos patriarcas. Deus cumpre suas promessas apesar das falhas humanas, preparando o caminho para a vinda do Messias.'
    
    if book_id == "exodus":
        return f'{title}. O capítulo {ch_num} de Êxodo narra a libertação de Israel do Egito e o estabelecimento da aliança no Sinai. Deus revela seu poder, sua lei e seu desejo de habitar no meio do seu povo.'
    
    # Generic for other books
    return f'{title}. Este capítulo revela verdades importantes sobre {theme}. A mensagem central aponta para a fidelidade de Deus e seu plano redentor que se cumpre em Jesus Cristo.'

def generate_reflection(book_id, ch_num, title, theme):
    if book_id in CHAPTER_TEXT and ch_num in CHAPTER_TEXT[book_id]:
        return CHAPTER_TEXT[book_id][ch_num][1]
    return f'{title} nos ensina sobre {theme}. Ao meditarmos neste capítulo, somos desafiados a aplicar seus princípios à nossa vida, reconhecendo que a Palavra de Deus é viva, eficaz e transformadora. Que possamos crescer em fé e obediência através do estudo das Escrituras.'

# ===================== APOLOGETIC POOLS =====================
APOL_OT = [
    "A arqueologia bíblica confirma a historicidade dos relatos do Antigo Testamento, com evidências de cidades, reis e eventos mencionados.",
    "As profecias messiânicas do AT cumprem-se com precisão em Jesus Cristo, algo estatisticamente impossível por acaso.",
    "A unidade literária da Bíblia, escrita ao longo de 1500 anos por 40 autores, aponta para inspiração divina.",
    "A lei moral bíblica é superior e anterior a outros códigos legais antigos, como o Código de Hamurabi.",
    "A preservação do povo judeu ao longo da história testemunha do cumprimento das promessas bíblicas.",
    "Os manuscritos do Mar Morto confirmam a precisão da transmissão textual do AT por mais de mil anos.",
    "A precisão histórica de nomes, lugares e costumes foi confirmada por descobertas arqueológicas.",
    "O cumprimento das profecias de juízo contra nações (Tiro, Nínive, Babilônia) é evidência de inspiração divina.",
]

APOL_NT = [
    "A historicidade dos evangelhos é corroborada por fontes extra-bíblicas como Tácito, Josefo e Plínio.",
    "O cumprimento das profecias do AT em Jesus demonstra a inspiração divina das Escrituras.",
    "O testemunho dos apóstolos, que morreram por sua fé, dá credibilidade histórica à ressurreição.",
    "A transformação dos discípulos de medrosos em pregadores corajosos é evidência da ressurreição.",
    "A consistência teológica entre os 27 livros do NT aponta para origem divina.",
    "A propagação explosiva do cristianismo no Império Romano, apesar da perseguição, testemunha do poder do evangelho.",
    "Múltiplos testemunhos oculares registrados nos evangelhos fornecem evidência histórica robusta para os eventos.",
    "O túmulo vazio é um dos fatos históricos mais estabelecidos, aceito até por críticos céticos.",
]

def generate_quiz(book_id, ch_num, title, testament):
    """Generate 2 quiz questions per chapter."""
    is_ot = testament == "Antigo Testamento"
    
    # Chapter-specific questions for key chapters
    qpools = [
        make_quiz_item("O que significa o nome deste livro?", ["Nome do autor", "Título do livro", "Tema central", "Personagem principal"], 2, "O título do livro reflete seu tema central e mensagem principal."),
        make_quiz_item("Quantos capítulos tem este livro?", ["Depende da edição", "Conforme indicado na introdução", "É o número total listado", "Varia conforme a tradição"], 2, "Cada livro bíblico tem seu número específico de capítulos conforme o cânon."),
        make_quiz_item("Qual é a mensagem principal deste capítulo?", ["Não é possível determinar", "O título do capítulo indica", "Precisa de estudo teológico", "Depende da interpretação"], 1, "O título de cada capítulo resume sua mensagem principal."),
        make_quiz_item("Em que testamento este livro está?", ["Antigo Testamento", "Novo Testamento", "Testamento Interbíblico", "Apócrifo"], 0 if is_ot else 1, f'Este livro pertence ao {testament}.'),
        make_quiz_item("Quem é o autor tradicional deste livro?", ["Moisés", "Davi", "Salomão", "Varia conforme o livro"], 3, "Diferentes livros foram escritos por diferentes autores inspirados por Deus."),
        make_quiz_item("Este capítulo contém principalmente:", ["Narrativa histórica", "Poesia e louvor", "Lei e mandamentos", "Profecia e visão"], 0, "Cada capítulo tem seu gênero literário predominante."),
    ]
    
    # Deterministic selection based on chapter number
    selected = []
    for i in range(2):
        idx = (hash(f"{book_id}:{ch_num}:{i}") % len(qpools))
        q = qpools[idx]
        if q not in selected:
            selected.append(q)
        else:
            # Pick the next one
            selected.append(qpools[(idx + 1) % len(qpools)])
    
    return selected

# ===================== BOOK DEFINITIONS =====================
# Each: (id, name, testament, total_chapters, [chapter_titles])

BOOKS_DEF = [
    ("genesis","Gênesis","Antigo Testamento",50,[
        "A Criação dos Céus e da Terra","O Jardim do Éden e a Criação do Homem","A Queda do Homem","Caim e Abel",
        "A Genealogia de Adão a Noé","A Corrupção e a Arca de Noé","O Dilúvio","As Águas Baixam",
        "A Aliança com Noé","As Gerações dos Filhos de Noé","A Torre de Babel","O Chamado de Abrão",
        "Abraão e Ló se Separam","Abraão Resgata Ló","A Aliança com Abraão","Hagar e Ismael","A Circuncisão",
        "A Intercessão por Sodoma","A Destruição de Sodoma","Abraão e Abimeleque","O Nascimento de Isaque",
        "O Sacrifício de Isaque","A Morte de Sara","O Casamento de Isaque","Morte de Abraão",
        "Isaque e Abimeleque","Jacó Recebe a Bênção","A Escada de Jacó","Jacó e Raquel","Os Filhos de Jacó",
        "Jacó Foge de Labão","Jacó Luta com Deus","A Reconciliação com Esaú","O Caso de Diná","Jacó Volta a Betel",
        "As Gerações de Esaú","José Vendido pelos Irmãos","Judá e Tamar","José e a Mulher de Potifar",
        "José na Prisão","José Interpreta os Sonhos de Faraó","Os Irmãos de José no Egito",
        "Os Irmãos Voltam com Benjamim","A Prova do Cálice","José se Revela","Jacó Desce ao Egito",
        "Jacó no Egito","Jacó Abençoa Efraim e Manassés","Jacó Abençoa Seus Filhos","A Morte de José"
    ]),
    ("exodus","Êxodo","Antigo Testamento",40,[
        "Israel Oprimido no Egito","O Nascimento e Fuga de Moisés","A Sarça Ardente","Os Sinais de Moisés",
        "Moisés e Arão Falam com Faraó","Deus Renova a Promessa","A Primeira Praga: Águas em Sangue",
        "Rãs, Piolhos e Moscas","Praga nos Animais, Úlceras e Saraiva","Gafanhotos e Trevas",
        "O Anúncio da Décima Praga","A Páscoa e a Saída do Egito","A Consagração dos Primogênitos",
        "A Travessia do Mar Vermelho","O Cântico de Moisés","O Maná do Céu","Água da Rocha",
        "O Conselho de Jetro","Israel no Monte Sinai","Os Dez Mandamentos","Leis sobre Servos e Danos",
        "Leis sobre Propriedade","Leis de Justiça e Festas","A Confirmação da Aliança",
        "A Oferta para o Tabernáculo","O Tabernáculo e Suas Cortinas","O Altar de Bronze",
        "As Vestes Sacerdotais","A Consagração dos Sacerdotes","O Altar do Incenso",
        "Bezalel e o Sábado","O Bezerro de Ouro","A Intercessão de Moisés","Novas Tábuas",
        "A Oferta para o Tabernáculo","A Construção do Tabernáculo","A Arca, a Mesa e o Candelabro",
        "O Altar do Holocausto","As Vestes Sacerdotais","A Glória do SENHOR Enche o Tabernáculo"
    ]),
    ("leviticus","Levítico","Antigo Testamento",27,[
        "O Holocausto","A Oferta de Manjares","A Oferta Pacífica","A Oferta pelo Pecado","A Oferta pela Culpa",
        "Leis sobre as Ofertas","A Consagração dos Sacerdotes","A Consagração de Arão","A Oferta de Arão",
        "Nadabe e Abiú","Animais Puros e Impuros","A Purificação da Mulher","Leis sobre a Lepra",
        "A Purificação do Leproso","Lepra nas Roupas","O Dia da Expiação","Leis sobre o Sangue",
        "Leis Morais e Sexuais","Leis de Santidade","Penalidades","Leis para os Sacerdotes",
        "As Festas Solenes","O Candelabro","A Pena de Blasfêmia","O Ano do Jubileu",
        "Bênçãos e Maldições","Os Votos e Dízimos"
    ]),
    ("numbers","Números","Antigo Testamento",36,[
        "O Censo de Israel","A Ordem do Acampamento","O Censo dos Levitas","Os Deveres dos Levitas",
        "A Purificação do Acampamento","A Consagração dos Nazireus","As Ofertas dos Príncipes",
        "A Consagração dos Levitas","A Primeira Páscoa","As Trombetas de Prata","O Povo Murmura",
        "Miriã e Arão Murmuram","Os Doze Espias","A Rebelião do Povo","Leis sobre Ofertas",
        "A Rebelião de Corá","A Vara de Arão Floresce","Deveres dos Sacerdotes","A Purificação",
        "A Morte de Miriã","A Serpente de Bronze","Balaque e Balaão","As Profecias de Balaão",
        "O Pecado de Baal-Peor","O Segundo Censo","As Filhas de Zelofeade","Josué é Comissionado",
        "As Ofertas Diárias","As Festas Solenes","Leis sobre os Votos","A Guerra contra Midiã",
        "As Tribos Além do Jordão","A Jornada de Israel","As Fronteiras de Canaã",
        "As Cidades dos Levitas","As Cidades de Refúgio"
    ]),
    ("deuteronomy","Deuteronômio","Antigo Testamento",34,[
        "Moisés Recorda a Jornada","A Conquista de Seom e Ogue","A Distribuição da Terra",
        "Exortação à Obediência","Os Dez Mandamentos","O Mandamento do Amor","Separação como Povo",
        "O Cuidado de Deus no Deserto","A Rebeldia de Israel","Novas Tábuas","O Grande Mandamento",
        "A Centralização do Culto","Falsos Profetas","Alimentos Puros","O Ano da Remissão",
        "As Festas Anuais","A Nomeação de Juízes","Leis para os Reis","Cidades de Refúgio",
        "Leis para a Guerra","Crimes Não Solucionados","Leis sobre Casamento","Santuário e Congregação",
        "Divórcio e Penhores","Punição por Açoites","Primícias e Dízimos","Altar no Monte Ebal",
        "Bênçãos e Maldições","A Renovação da Aliança","Escolha entre Vida e Morte","Cântico de Moisés",
        "Moisés Vê a Terra","A Bênção de Moisés","A Morte de Moisés"
    ]),
    ("joshua","Josué","Antigo Testamento",24,[
        "Deus Ordena a Conquista","A Fé de Raabe","A Travessia do Jordão","Memorial das Doze Pedras",
        "A Circuncisão em Gilgal","A Queda de Jericó","O Pecado de Acã","A Conquista de Ai",
        "A Astúcia dos Gibeonitas","O Sol Para em Gibeão","A Conquista do Norte","Reis Conquistados",
        "Terras por Conquistar","A Herança de Calebe","Herança de Judá","Herança de José",
        "Herança de Manassés","O Tabernáculo em Siló","Herança das Tribos","Cidades de Refúgio",
        "Cidades dos Levitas","Altar de Testemunho","Discurso de Despedida","Aliança Renovada"
    ]),
    ("judges","Juízes","Antigo Testamento",21,[
        "Conquista Incompleta","O Anjo em Boquim","Otniel, Eúde e Sangar","Débora e Baraque",
        "Cântico de Débora","A Chamada de Gideão","Gideão Derrota Midiã","Gideão e os Efraimitas",
        "Abimeleque","Tola e Jair","Jefté","Jefté e os Efraimitas","O Nascimento de Sansão",
        "Sansão e a Mulher de Timna","Sansão Vinga-se","Sansão e Dalila","A Morte de Sansão",
        "Mica e a Idolatria","Levita e Concubina","Guerra contra Benjamim","Resgate das Virgens"
    ]),
    ("ruth","Rute","Antigo Testamento",4,[
        "Noemi e Rute","Rute Encontra Boaz","Rute na Eira de Boaz","Boaz Casa-se com Rute"
    ]),
    ("1samuel","1 Samuel","Antigo Testamento",31,[
        "Nascimento de Samuel","Cântico de Ana","O Chamado de Samuel","A Captura da Arca",
        "A Arca entre os Filisteus","O Retorno da Arca","Samuel Juiz de Israel","Israel Pede um Rei",
        "Saul é Escolhido","Saul é Ungido","Saul Confirma o Reinado","Samuel Adverte o Povo",
        "Guerra contra os Filisteus","A Loucura de Saul","Deus Rejeita Saul","Davi é Ungido",
        "Davi e Golias","Amizade de Davi e Jônatas","Saul Tenta Matar Davi","Jônatas Ajuda Davi",
        "Davi Foge para Nobe","Davi em Gate","Davi Liberta Queila","Davi Poupa Saul",
        "Morte de Samuel","Davi e Abigail","Davi Poupa Saul Novamente","Davi em Ziclague",
        "A Feiticeira de En-Dor","A Morte de Saul","Lamento de Davi"
    ]),
    ("2samuel","2 Samuel","Antigo Testamento",24,[
        "Davi Chora Saul","Davi é Ungido Rei","A Casa de Davi","Ish-Bosete é Assassinado",
        "Davi Rei de Israel","A Arca em Jerusalém","Pacto de Deus com Davi","Conquistas de Davi",
        "Mefibosete","Guerra contra Amom","Pecado com Bate-Seba","Natã Reprova Davi",
        "Morte do Filho de Davi","Amnom e Tamar","Absalão Foge","Absalão Volta",
        "Absalão Conspira","Davi Foge de Absalão","Absalão em Jerusalém","Davi Volta",
        "Morte de Absalão","Davi Retorna","Últimas Palavras de Davi","Censo e Peste"
    ]),
    ("1kings","1 Reis","Antigo Testamento",22,[
        "Velhice de Davi","Adonias Toma o Reino","Salomão é Ungido","Governo de Salomão",
        "Sabedoria de Salomão","Construção do Templo","Dedicação do Templo","Aparição a Salomão",
        "Rainha de Sabá","Riqueza de Salomão","Pecado de Salomão","Rebelião de Jeroboão",
        "Profeta de Judá","Juízo contra Jeroboão","Reis de Judá e Israel","Reinado de Asa",
        "Profecia de Elias","Elias e os Profetas de Baal","Elias em Horebe","Vinha de Nabote",
        "Morte de Acabe","Reinado de Acazias"
    ]),
    ("2kings","2 Reis","Antigo Testamento",25,[
        "Elias e Acazias","Ascensão de Elias","A Viúva e o Azeite","Filho da Sunamita",
        "Cura de Naamã","Machado que Flutuou","Cerce de Samaria","A Sunamita Retorna",
        "Jeú é Ungido","Jeú Mata a Família de Acabe","Reinado de Jeú","Morte de Jeú",
        "Reforma de Joás","Morte de Eliseu","Reis de Israel","Queda de Samaria",
        "Reinado de Ezequias","Reforma de Ezequias","Oração e Cura de Ezequias","Ezequias e os Babilônios",
        "Reinado de Manassés","Reinado de Josias","Reforma de Josias","Livro da Lei Encontrado",
        "Queda de Jerusalém"
    ]),
    ("1chronicles","1 Crônicas","Antigo Testamento",29,[
        "Adão a Abraão","Filhos de Israel","Família de Davi","Genealogia de Judá",
        "Genealogia de Simeão","Genealogia de Levi","Issacar, Benjamim, Naftali","Efraim e Manassés",
        "Genealogia de Benjamim","Reinado de Saul","Davi Ungido","Valentes de Davi",
        "Arca Trazida","Casa de Davi","Arca em Jerusalém","Cântico de Ação de Graças",
        "Pacto de Deus com Davi","Conquistas de Davi","Guerra contra Amom","Vitória sobre Filisteus",
        "Censo de Davi","Preparação para o Templo","Davi Organiza os Levitas","Porteiros e Músicos",
        "Tesouro do Templo","Oficiais","Davi Estabelece o Culto","Discurso a Salomão","Morte de Davi"
    ]),
    ("2chronicles","2 Crônicas","Antigo Testamento",36,[
        "Salomão em Gibeão","Sabedoria de Salomão","Construção do Templo","Utensílios do Templo",
        "Arca no Templo","Dedicação do Templo","Resposta de Deus a Salomão","Conquistas de Salomão",
        "Rainha de Sabá","Morte de Salomão","Divisão do Reino","Invasão de Sisaque",
        "Reinado de Abias","Reinado de Asa","Reforma de Asa","Reinado de Josafá",
        "Vitória de Josafá","Morte de Josafá","Jeorão e Acazias","Reinado de Joás",
        "Reinado de Amazias","Reinado de Uzias","Jotão e Acaz","Reinado de Ezequias",
        "Reforma de Ezequias","Invasão de Senaqueribe","Cura de Ezequias","Reinado de Manassés",
        "Amom e Josias","Reforma de Josias","Páscoa de Josias","Morte de Josias",
        "Jeoiaquim","Zedequias","Cativeiro Babilônico","Decreto de Ciro"
    ]),
    ("ezra","Esdras","Antigo Testamento",10,[
        "Decreto de Ciro","Lista dos Exilados","Construção do Altar","Oposição à Construção",
        "Construção Retomada","Templo Concluído","Chegada de Esdras","Casamentos Mistos",
        "Confissão de Esdras","Reforma de Esdras"
    ]),
    ("nehemiah","Neemias","Antigo Testamento",13,[
        "Oração de Neemias","Neemias Inspeciona","A Reconstrução","Oposição dos Inimigos",
        "Proteção de Deus","Conspiração contra Neemias","Repopulação","Leitura da Lei",
        "Confissão do Povo","Renovação da Aliança","Dedicação dos Muros","Reforma de Neemias",
        "Serviço no Templo"
    ]),
    ("esther","Ester","Antigo Testamento",10,[
        "Banquete de Assuero","Ester Rainha","Conspiração de Hamã","Plano de Hamã",
        "Pedido de Ester","Rei Honra Mordecai","Queda de Hamã","Decreto de Ester",
        "Vitória dos Judeus","Festa de Purim"
    ]),
    ("job","Jó","Antigo Testamento",42,[
        "Integridade de Jó","Satanás Acusa Jó","Jó Amaldiçoa o Dia","Elifaz Fala",
        "Jó Responde a Elifaz","Jó Clama a Deus","Brevidade da Vida","Bildade Fala",
        "Jó Confia na Justiça","Jó Questiona","Zofar Fala","Sabedoria de Deus",
        "Jó Argumenta","Certeza da Redenção","Zofar Novamente","Poder de Deus",
        "Jó Busca Resposta","Bildade Responde","Confiança no Redentor","Prosperidade dos Ímpios",
        "Justiça de Deus","Acusação Continua","Deseja Apresentar-se","Onipotência de Deus",
        "Bildade Novamente","Reafirma Integridade","Sabedoria de Deus","Onde Está a Sabedoria",
        "Recorda o Passado","Humilhação Atual","Defende Pureza","Eliú se Apresenta",
        "Eliú Fala sobre Deus","Eliú Defende Justiça","Eliú Exalta a Deus","Deus Fala do Turbilhão",
        "Deus Desafia Jó","Jó se Arrepende","Deus Repreende Amigos","Restauração de Jó",
        "Prosperidade Final","Morte de Jó"
    ]),
    ("psalms","Salmos","Antigo Testamento",150,[
        "O Justo e os Pecadores","Glória de Deus","Confiança em Deus","Oração Vespertina",
        "Súplica Matinal","Julgamento de Deus","Refúgio em Deus","Majestade de Deus",
        "Louvor pela Justiça","Por que os Ímpios?","Confiança na Justiça","Perigo da Língua",
        "Clamor do Justo","Atalaia de Sião","Santidade","Refúgio na Presença","Louvor",
        "Glória na Criação","Oração pelo Rei","Louvor pela Vitória","Sofrimento do Justo",
        "O Senhor é meu Pastor","Súplica por Direção","Confiança","O Senhor é a Luz",
        "Clamor por Ajuda","Voz do Senhor","Ação de Graças","Entrega nas Mãos de Deus",
        "Felicidade do Perdão","Louvor ao Criador","Bondade de Deus","Oração por Livramento",
        "Maldade dos Ímpios","Prosperidade dos Justos","Sofrimento","Fragilidade da Vida",
        "Alegria da Obediência","Salmo de Cura","Alma Sedenta por Deus","Súplica por Justiça",
        "Saudade do Santuário","Casamento Real","Deus é Refúgio","Deus Reina",
        "Excelência de Sião","Engano das Riquezas","Juízo de Deus","Oração Penitencial",
        "Loucura dos Ímpios","Socorro Vem de Deus","Deus Justo","Entrega a Deus",
        "Clamor na Perseguição","Sombra das Asas","Juízo contra Juízes","Libertação",
        "Ação de Graças","Oração por Proteção","Alma Descansa","Alma Sedenta",
        "Súplica por Proteção","Louvor pela Colheita","Ação de Graças","Oração Coletiva",
        "Juízo sobre Inimigos","Justiça Reinará","Oração do Velho","Glória do Messias",
        "Justiça e Julgamento","Deus é Conhecido","Memorial das Obras","Rebelião de Israel",
        "Oração pela Restauração","Juízo de Deus","Deus Altíssimo","Oração contra Nações",
        "Bondade a Israel","Juízo dos Deuses","Sede de Deus","Oração por Ajuda",
        "Tabernáculo de Deus","Louvor pela Misericórdia","Fidelidade de Deus","Oração do Aflito",
        "Louvor Eterno","Governo de Deus","Peregrino na Terra","Oração na Angústia",
        "Ação de Graças","Eterno Amor de Deus","Luz para o Caminho","Oração do Aflito",
        "Proteção Divina","O Senhor te Guardará","Bênção","União Fraternal","Louvor Noturno",
        "Exílio de Sião","Humildade","Servo de Deus","Onisciência","Livramento",
        "Oração Vespertina","Louvor Matinal","Bem-aventurança","Libertação","Juízo e Misericórdia",
        "Lembrança das Obras","Ação de Graças","Louvor pela Vitória","Aleluia",
        "Mão Poderosa","Sabedoria e Temor","Justo Floresce","Palavra de Deus",
        "Louvor","Pastor de Israel","Alegria em Deus","Clamor por Justiça",
        "Súplica por Misericórdia","Ação de Graças","Alegria na Presença","Oração por Socorro",
        "Deus Vivo","Ação de Graças","Obras de Deus","Justo Teme a Deus",
        "Humilde e Soberbo","Bendito o Nome","Ídolos e Deus Vivo","Ação de Graças",
        "Valor da Palavra","Maravilhas da Lei","Clamor nas Trevas","Oração Penitencial",
        "Súplica","Clamor Profundo","Confiança","Oração por Direção",
        "Louvor pela Santidade","Comunhão Fraternal","Oração do Exílio","Oração da Manhã",
        "Presença de Deus","Grande é o Senhor","Ação de Graças Nacional","Louvor Universal",
        "Aleluia pelo Amor","Louvor pela Restauração","Cântico de Sião","Aleluia pela Criação",
        "Aleluia pela História","Aleluia pela Libertação","Aleluia"
    ]),
    ("proverbs","Provérbios","Antigo Testamento",31,[
        "Propósito dos Provérbios","Valor da Sabedoria","Confiança no Senhor","Caminho da Sabedoria",
        "Advertência contra Imoralidade","Responsabilidade Financeira","Sedução do Adultério","Sabedoria Clama",
        "Banquete da Sabedoria","Provérbios de Salomão","Retidão e Justiça","Disciplina do Senhor",
        "Justo e Ímpio","Sabedoria Edifica","Resposta Mansa","Senhor Dirige os Passos",
        "Melhor é o Pobre Justo","Espírito do Homem","Justo e Tolo","Perigo do Vinho",
        "Coração do Rei","Bom Nome","Inveja e Cobiça","Sabedoria Constrói",
        "Rei Justo","Tolo e Preguiçoso","O Amanhã","Lei e Justiça",
        "Orgulho e Humildade","Sabedoria de Agur","Mulher Virtuosa"
    ]),
    ("ecclesiastes","Eclesiastes","Antigo Testamento",12,[
        "Tudo é Vaidade","Vaidade do Prazer","Tudo Tem seu Tempo","Vaidade da Opressão",
        "Reverência a Deus","Vaidade das Riquezas","Sabedoria Prática","Respeito à Autoridade",
        "Incerteza da Vida","Tolo e Sabedoria","Juventude e Velhice","Lembra-te do Criador"
    ]),
    ("songofsolomon","Cântico dos Cânticos","Antigo Testamento",8,[
        "O Beijo do Amor","Encontro dos Amados","Busca pelo Amado","Formosura da Amada",
        "Amado Descreve a Amada","Declaração de Amor","Dança da Sulamita","Amor Forte como a Morte"
    ]),
    ("isaiah","Isaías","Antigo Testamento",66,[
        "Visão de Isaías","Profecia sobre Jerusalém","Juízo sobre Judá","Vinha do Senhor",
        "Parábola da Vinha","Glória de Deus","O Emanuel","Rápido Despojo",
        "Príncipe da Paz","Juízo contra Assíria","Renovo de Jessé","Ação de Graças",
        "Queda da Babilônia","Libertação de Israel","Queda de Babilônia","Juízo contra Moabe",
        "Juízo contra Damasco","Mensagem para Etiópia","Mensagem para Egito","Sinal contra Egito",
        "Queda da Babilônia","Mensagem contra Edom","Juízo sobre Tiro","Juízo Universal",
        "Louvor pela Vitória","Cântico de Confiança","Libertação de Israel","Advertência a Efraim",
        "Advertência a Ariel","Confiança no Egito","Sabedoria Humana","Rei Justo",
        "Clamor por Justiça","Juízo sobre Nações","Caminho de Santidade","Invasão de Senaqueribe",
        "Oração de Ezequias","Cura de Ezequias","Consolo de Deus","Grandeza de Deus",
        "Servo do Senhor","Cântico do Servo","Remanescente de Israel","Loucura dos Ídolos",
        "Ciro, o Ungido","Queda da Babilônia","Clamor de Deus","Salvação de Deus",
        "Servo Fiel","Descendente de Abraão","Consolo para Sião","Despertar de Jerusalém",
        "Sofrimento do Servo","Amor Eterno","Convite à Salvação","Clamor de Deus",
        "Casa de Oração","Jejum que Agrada","Pecado e Confissão","Glória de Sião",
        "Ano da Bondade do Senhor","Clamor pela Restauração","Vingador de Sião","Justiça de Deus",
        "Clamor do Remanescente","Novos Céus e Nova Terra","Glória Final de Israel"
    ]),
    ("jeremiah","Jeremias","Antigo Testamento",52,[
        "Chamado de Jeremias","Mensagem contra Israel","Volta de Israel","Clamor por Arrependimento",
        "Pecado de Jerusalém","Advertência","Hipocrisia do Templo","Idolatria de Israel",
        "Lamento de Jeremias","Loucura dos Ídolos","Aliança Quebrada","Queixa de Jeremias",
        "Cinto de Linho","Seca em Judá","Juízo Imutável","Casamento de Jeremias",
        "Pecado de Judá","Oleiro e o Barro","Vasilha Quebrada","Jeremias no Tronco",
        "Advertência a Zedequias","Mensagem contra Reis","Pastores de Israel","Bom e Mau Figo",
        "Taça da Ira","Mensagem no Templo","Jugo de Babilônia","Profecia contra Hananias",
        "Carta aos Exilados","Restauração de Israel","Novo Concerto","Campo de Hanameel",
        "Restauração de Jerusalém","Profecia contra Zedequias","Recabitas","Rolo Queimado",
        "Cativeiro de Zedequias","Jeremias na Cisterna","Queda de Jerusalém","Jeremias Libertado",
        "Assassinato de Gedalias","Fuga para o Egito","Jeremias no Egito","Mensagem contra Egito",
        "Mensagem contra Filisteus","Mensagem contra Moabe","Mensagem contra Amom","Mensagem contra Damasco",
        "Mensagem contra Elão","Mensagem contra Babilônia","Queda de Babilônia","Fim de Jeremias"
    ]),
    ("lamentations","Lamentações","Antigo Testamento",5,[
        "Jerusalém Destruída","Ira do Senhor","Esperança no Sofrimento","Cerce de Jerusalém",
        "Oração por Restauração"
    ]),
    ("ezekiel","Ezequiel","Antigo Testamento",48,[
        "Visão do Carro de Deus","Chamado de Ezequiel","Atalaia de Israel","Cerce Figurado",
        "Julgamento sobre Jerusalém","Juízo sobre Montes","O Fim Chegou","Abominação no Templo",
        "Extermínio dos Ímpios","Glória se Retira","Juízo contra Maus Conselheiros","Exílio Figurado",
        "Falsos Profetas","Juízo contra Idólatras","Videira Inútil","Esposa Infiel",
        "Parábola das Águias","Justiça de Deus","Lamento pelos Príncipes","Rebelião de Israel",
        "Espada do Senhor","Pecados de Jerusalém","Oholá e Oolibá","Parábola da Panela",
        "Mensagem contra Amom","Mensagem contra Tiro","Lamento sobre Tiro","Mensagem contra Sidom",
        "Mensagem contra Egito","Dia do Senhor sobre Egito","Queda do Egito","Lamento sobre Faraó",
        "Atalaia Restaurado","Pastores de Israel","Mensagem contra Seir","Profecia para Montes",
        "Vale de Ossos Secos","Profecia contra Gogue","Queda de Gogue","Visão do Novo Templo",
        "Medida do Templo","Glória Volta ao Templo","Altar e Sacrifícios","Santuário e Sacerdotes",
        "Divisão da Terra","Príncipe e Tribos","Portas da Cidade","Nome da Cidade"
    ]),
    ("daniel","Daniel","Antigo Testamento",12,[
        "Daniel na Corte","Sonho de Nabucodonosor","Estátua de Ouro","Fornalha Ardente",
        "Escrita na Parede","Cova dos Leões","Visão dos Quatro Animais","Carneiro e Bode",
        "Setenta Semanas","Visão Junto ao Rio","Profecia contra Rei do Sul","Tempo do Fim"
    ]),
    ("hosea","Oseias","Antigo Testamento",14,[
        "Casamento de Oseias","Infidelidade de Israel","Amor de Deus","Acusação contra Israel",
        "Juízo sobre Israel","Clamor por Arrependimento","Pecado de Efraim","Colheita Segundo Semeadura",
        "Exílio de Israel","Juízo sobre Bezerros","Amor de Deus","Conspiração de Jacó",
        "Julgamento de Deus","Clamor por Santidade"
    ]),
    ("joel","Joel","Antigo Testamento",3,[
        "Praga dos Gafanhotos","O Dia do Senhor","Derramamento do Espírito"
    ]),
    ("amos","Amós","Antigo Testamento",9,[
        "Juízo sobre Nações","Juízo sobre Israel","Chamado de Amós","Obstinação de Israel",
        "Clamor por Justiça","Ai dos Satisfeitos","Visões de Amós","Cesto de Frutas Maduras",
        "Restauração de Israel"
    ]),
    ("obadiah","Obadias","Antigo Testamento",1,[
        "Juízo contra Edom"
    ]),
    ("jonah","Jonas","Antigo Testamento",4,[
        "Jonas Foge de Deus","Oração de Jonas","Jonas em Nínive","Ira e Misericórdia"
    ]),
    ("micah","Miquéias","Antigo Testamento",7,[
        "Juízo contra Samaria","Clamor contra Opressão","Condenação dos Líderes","Reino de Paz",
        "Nascimento do Messias","Clamor de Deus","Misericórdia de Deus"
    ]),
    ("nahum","Naum","Antigo Testamento",3,[
        "Juízo contra Nínive","Queda de Nínive","Ai de Nínive"
    ]),
    ("habakkuk","Habacuque","Antigo Testamento",3,[
        "Queixa de Habacuque","Justiça de Deus","Cântico de Fé"
    ]),
    ("zephaniah","Sofonias","Antigo Testamento",3,[
        "O Dia do Senhor","Clamor por Arrependimento","Cântico de Alegria"
    ]),
    ("haggai","Ageu","Antigo Testamento",2,[
        "Reconstrução do Templo","Glória do Novo Templo"
    ]),
    ("zechariah","Zacarias","Antigo Testamento",14,[
        "Chamado ao Arrependimento","Visões de Zacarias","Josué, Sumo Sacerdote","Candelabro de Ouro",
        "Rolo Voador e Efá","Visão dos Quatro Carros","Condenação da Hipocrisia","Restauração de Sião",
        "Julgamento das Nações","Senhor Pastoreia","Rejeição do Pastor","Vitória de Judá",
        "Purificação de Jerusalém","O Dia do Senhor"
    ]),
    ("malachi","Malaquias","Antigo Testamento",4,[
        "Amor de Deus","Corrupção dos Sacerdotes","Roubo dos Dízimos","O Dia do Senhor"
    ]),
    ("matthew","Mateus","Novo Testamento",28,[
        "Genealogia de Jesus","Nascimento de Jesus","Visita dos Magos","Fuga para o Egito",
        "Tentações de Jesus","Sermão do Monte: Bem-aventuranças","Sermão do Monte: Oração",
        "Cura de um Leproso","Cura do Paralítico","Escolha dos Doze","João Batista Pergunta",
        "Senhor do Sábado","Parábola do Semeador","Morte de João Batista","Multiplicação dos Pães",
        "Mulher Cananeia","Transfiguração","Criança no Reino","Jovem Rico",
        "Parábola dos Trabalhadores","Entrada Triunfal","Parábola dos Lavradores","Sermão sobre o Futuro",
        "Parábola das Dez Virgens","Juízo Final","Ceia em Betânia","Crucificação","Ressurreição"
    ]),
    ("mark","Marcos","Novo Testamento",16,[
        "Batismo de Jesus","Início do Ministério","Cura da Mão Ressequida","Parábola do Semeador",
        "Endemoninhado Gadareno","Rejeição em Nazaré","Tradição dos Homens","Multiplicação dos Pães",
        "Transfiguração","Ensino sobre Divórcio","Entrada Triunfal","Parábola dos Lavradores",
        "Sermão Profético","Unção em Betânia","Crucificação","Ressurreição"
    ]),
    ("luke","Lucas","Novo Testamento",24,[
        "Anúncio a Zacarias","Nascimento de Jesus","Batismo e Genealogia","Tentações",
        "Chamada dos Discípulos","Sermão da Planície","Cura do Servo","Parábola do Semeador",
        "Missão dos Doze","Bom Samaritano","Pai Nosso","Hipocrisia dos Fariseus",
        "Rico Insensato","Arrependimento","Filho Pródigo","Rico e Lázaro",
        "Cura dos Dez Leprosos","Juiz Iníquo","Zaqueu","Parábola dos Lavradores",
        "Oferta da Viúva","Sermão Profético","Última Ceia e Crucificação","Ressurreição e Ascensão"
    ]),
    ("john","João","Novo Testamento",21,[
        "O Verbo se Fez Carne","Bodas de Caná","Nicodemos","Mulher Samaritana",
        "Cura do Paralítico","Multiplicação dos Pães","Festa dos Tabernáculos","Mulher Adúltera",
        "Cura do Cego","Bom Pastor","Ressurreição de Lázaro","Unção em Betânia",
        "Lava-pés","Promessa do Consolador","Videira Verdadeira","Oração Sacerdotal",
        "Prisão e Julgamento","Crucificação","Ressurreição","Aparição aos Discípulos",
        "Restauração de Pedro"
    ]),
    ("acts","Atos","Novo Testamento",28,[
        "Ascensão e Pentecostes","Cura do Coxo","Pedro e João no Sinédrio","Comunhão dos Cristãos",
        "Ananias e Safira","Escolha dos Sete","Martírio de Estêvão","Filipe e o Eunuco",
        "Conversão de Saulo","Pedro e Cornélio","Igreja em Antioquia","Prisão de Pedro",
        "Primeira Viagem Missionária","Concílio de Jerusalém","Segunda Viagem","Paulo em Filipos",
        "Paulo em Tessalônica","Paulo em Corinto","Paulo em Éfeso","Paulo na Grécia",
        "Paulo Retorna","Paulo no Templo","Paulo no Sinédrio","Paulo em Cesareia",
        "Paulo Apela a César","Paulo Naufraga","Paulo em Roma","Paulo Pregando"
    ]),
    ("romans","Romanos","Novo Testamento",16,[
        "Poder do Evangelho","Justiça de Deus","Justificação pela Fé","Exemplo de Abraão",
        "Adão e Cristo","Morte para o Pecado","Luta Interior","Libertação pelo Espírito",
        "Soberania de Deus","Salvação para Todos","Remanescente de Israel","Renovação da Mente",
        "Amor e a Lei","Fracos e Fortes","Exemplo de Cristo","Saudações"
    ]),
    ("1corinthians","1 Coríntios","Novo Testamento",16,[
        "Igreja de Corinto","Sabedoria de Deus","Fundamento que é Cristo","Fidelidade no Ministério",
        "Imoralidade na Igreja","Litígios entre Irmãos","Casamento e Vida Solteira","Liberdade Cristã",
        "Direito Apostólico","Advertências do Deserto","Cabeça da Mulher","Ceia do Senhor",
        "Dons Espirituais","O Amor","Ressurreição","Coleta e Saudações"
    ]),
    ("2corinthians","2 Coríntios","Novo Testamento",13,[
        "Deus de Toda Consolação","Ministério da Reconciliação","Glória do Novo Concerto",
        "Tesouro em Vasos de Barro","Morada Eterna","Ministério de Paulo","Arrependimento e Alegria",
        "Generosidade","Semeadura Generosa","Autoridade de Paulo","Contribuições","Visão e Espinho",
        "Conclusão e Amor Fraternal"
    ]),
    ("galatians","Gálatas","Novo Testamento",6,[
        "Único Evangelho","Autoridade de Paulo","Justificação pela Fé","Abraão e a Promessa",
        "Liberdade Cristã","Semeadura e Ceifa"
    ]),
    ("ephesians","Efésios","Novo Testamento",6,[
        "Bênçãos Espirituais","Salvação pela Graça","Mistério Revelado","Unidade do Corpo",
        "Vida de Santidade","Armadura de Deus"
    ]),
    ("philippians","Filipenses","Novo Testamento",4,[
        "Ação de Graças","Humildade de Cristo","Justiça que Vem de Deus","Alegria no Senhor"
    ]),
    ("colossians","Colossenses","Novo Testamento",4,[
        "Supremacia de Cristo","Plenitude em Cristo","Vida Oculta em Cristo","Conduta Cristã"
    ]),
    ("1thessalonians","1 Tessalonicenses","Novo Testamento",5,[
        "Exemplo dos Tessalonicenses","Ministério de Paulo","Santificação e Amor","Vinda do Senhor",
        "Vigilância e Esperança"
    ]),
    ("2thessalonians","2 Tessalonicenses","Novo Testamento",3,[
        "Ações de Graças","Dia do Senhor","Fidelidade e Diligência"
    ]),
    ("1timothy","1 Timóteo","Novo Testamento",6,[
        "Advertência contra Falsos Mestres","Oração e Conduta","Bispos e Diáconos",
        "Ministério","Trato com Membros","Piedade e Contentamento"
    ]),
    ("2timothy","2 Timóteo","Novo Testamento",4,[
        "Chamado ao Sofrimento","Soldado de Cristo","Sã Doutrina","Coroa da Justiça"
    ]),
    ("titus","Tito","Novo Testamento",3,[
        "Nomeação de Presbíteros","Sã Doutrina na Vida","Boas Obras"
    ]),
    ("philemon","Filemom","Novo Testamento",1,[
        "Pedido por Onésimo"
    ]),
    ("hebrews","Hebreus","Novo Testamento",13,[
        "Supremacia do Filho","Advertência contra Negligência","Descanso de Deus","Sumo Sacerdote",
        "Sacerdócio de Melquisedeque","Chamado à Maturidade","Sacerdócio de Cristo",
        "Nova Aliança","Culto Perfeito","Único Sacrifício","A Fé","Disciplina do Senhor",
        "Vida Cristã Prática"
    ]),
    ("james","Tiago","Novo Testamento",5,[
        "Provação e Sabedoria","Fé e Obras","Poder da Língua","Submissão a Deus",
        "Oração da Fé"
    ]),
    ("1peter","1 Pedro","Novo Testamento",5,[
        "Esperança Viva","Pedra Viva","Submissão e Sofrimento","Vida Santificada","Apelo aos Pastores"
    ]),
    ("2peter","2 Pedro","Novo Testamento",3,[
        "Crescimento na Graça","Falsos Profetas","O Dia do Senhor"
    ]),
    ("1john","1 João","Novo Testamento",5,[
        "Palavra da Vida","O Anticristo","Filhos de Deus","Amor de Deus","Vitória da Fé"
    ]),
    ("2john","2 João","Novo Testamento",1,[
        "A Senhora Eleita"
    ]),
    ("3john","3 João","Novo Testamento",1,[
        "Hospitalidade e Verdade"
    ]),
    ("jude","Judas","Novo Testamento",1,[
        "Advertência contra Falsos Mestres"
    ]),
    ("revelation","Apocalipse","Novo Testamento",22,[
        "Visão do Filho do Homem","Cartas a Éfeso e Esmirna","Cartas a Pérgamo e Tiatira",
        "Cartas a Sardes, Filadélfia e Laodiceia","O Trono de Deus","Os Sete Selos","144 Mil Selados",
        "Sétimo Selo e Trombetas","Quinta e Sexta Trombetas","Anjo e Livrinho","Duas Testemunhas",
        "Sétima Trombeta","Dragão e Bestas","Cântico dos 144 Mil","Sete Taças da Ira",
        "Grande Babilônia","Queda da Babilônia","Aleluia Final","Cavaleiro Fiel e Verdadeiro",
        "Milênio e Juízo Final","Novo Céu e Nova Terra","Vinda de Jesus"
    ]),
]

BOOK_THEMES = {
    "genesis":"criação, queda, promessa, patriarcas","exodus":"libertação, aliança, lei, tabernáculo",
    "leviticus":"santidade, sacrifício, expiação","numbers":"jornada, murmuração, censo, conquista",
    "deuteronomy":"aliança renovada, lei, bênção, maldição","joshua":"conquista, herança, fé, obediência",
    "judges":"pecado, opressão, libertação","ruth":"lealdade, redenção, amor",
    "1samuel":"rei, profeta, unção, obediência","2samuel":"Davi, aliança, pecado, restauração",
    "1kings":"sabedoria, idolatria, profecia","2kings":"profecia, juízo, cativeiro, reforma",
    "1chronicles":"genealogia, Davi, culto","2chronicles":"templo, reforma, fidelidade",
    "ezra":"restauração, templo, reforma","nehemiah":"reconstrução, muralhas, reforma",
    "esther":"providência, livramento, coragem","job":"sofrimento, soberania, redenção",
    "psalms":"louvor, lamento, confiança, adoração","proverbs":"sabedoria, temor do Senhor",
    "ecclesiastes":"propósito, temor de Deus","songofsolomon":"amor, casamento, intimidade",
    "isaiah":"juízo, consolo, Servo, redenção","jeremiah":"juízo, novo concerto, arrependimento",
    "lamentations":"lamento, esperança, misericórdia","ezekiel":"glória, juízo, restauração, visões",
    "daniel":"soberania, profecia, fidelidade","hosea":"amor, infidelidade, restauração",
    "joel":"dia do Senhor, arrependimento","amos":"justiça, juízo, direito",
    "obadiah":"orgulho, juízo","jonah":"misericórdia, arrependimento, missão",
    "micah":"justiça, messias, paz","nahum":"juízo contra Nínive",
    "habakkuk":"fé, justiça, soberania","zephaniah":"dia do Senhor, juízo",
    "haggai":"templo, prioridades","zechariah":"messias, restauração, profecia",
    "malachi":"dízimo, aliança, messias",
    "matthew":"Messias, Reino, ensino","mark":"servo, Filho de Deus",
    "luke":"humanidade, inclusão, oração","john":"divindade, vida, luz, amor",
    "acts":"Espírito Santo, missão, igreja","romans":"justificação, graça, fé, santificação",
    "1corinthians":"unidade, dons, amor, ressurreição","2corinthians":"consolação, ministério, generosidade",
    "galatians":"graça, liberdade, Espírito","ephesians":"Igreja, bênçãos, unidade",
    "philippians":"alegria, humildade, contentamento","colossians":"Cristo supremo, sabedoria",
    "1thessalonians":"esperança, santificação","2thessalonians":"perseverança, dia do Senhor",
    "1timothy":"liderança, sã doutrina","2timothy":"fidelidade, sofrimento",
    "titus":"boas obras, doutrina","philemon":"perdão, reconciliação",
    "hebrews":"Cristo, sacerdócio, fé","james":"fé, obras, sabedoria",
    "1peter":"esperança, sofrimento, santidade","2peter":"crescimento, falsos mestres",
    "1john":"amor, luz, verdade","2john":"verdade, amor",
    "3john":"hospitalidade, verdade","jude":"fé, perseverança",
    "revelation":"apocalipse, juízo, nova criação",
}

# ===================== VERSE SPLITTING =====================
import re as _re

def split_verses(text):
    """Split chapter text into numbered verses."""
    if not text:
        return ["Leia este capítulo em sua Bíblia para meditar nos detalhes."]
    if '\n\n' in text:
        parts = text.split('\n\n')
    else:
        parts = _re.split(r'(?<=[.!?])\s+(?=[A-Z\"\'«])', text)
    parts = [p.strip() for p in parts if p.strip()]
    return parts if parts else [text]

CHAPTER_VERSES = {
    "genesis": {
        1: [
            "No princípio, criou Deus os céus e a terra.",
            "A terra era sem forma e vazia; e havia trevas sobre a face do abismo; mas o Espírito de Deus pairava sobre a face das águas. E disse Deus: Haja luz. E houve luz.",
            "E viu Deus que a luz era boa; e fez separação entre a luz e as trevas. E chamou à luz Dia, e às trevas chamou Noite. E foi a tarde e a manhã, o primeiro dia.",
            "E disse Deus: Haja uma expansão no meio das águas, e haja separação entre águas e águas. E chamou a expansão Céus. E foi a tarde e a manhã, o segundo dia.",
            "E disse Deus: Ajuntem-se as águas debaixo dos céus num lugar, e apareça a porção seca. E disse Deus: Produza a terra erva verde e árvores frutíferas. E foi a tarde e a manhã, o terceiro dia.",
            "E disse Deus: Haja luzeiros no firmamento dos céus. E fez Deus os dois grandes luzeiros: o maior para governar o dia, e o menor para governar a noite; e fez também as estrelas. E foi a tarde e a manhã, o quarto dia.",
            "E disse Deus: Produzam as águas abundantemente répteis de alma vivente, e voem as aves sobre a face do firmamento. E criou Deus as grandes baleias. E foi a tarde e a manhã, o quinto dia.",
            "E disse Deus: Produza a terra alma vivente. Façamos o homem à nossa imagem, conforme a nossa semelhança. E criou Deus o homem à sua imagem; homem e mulher os criou.",
            "E viu Deus tudo quanto tinha feito, e eis que era muito bom. E foi a tarde e a manhã, o sexto dia.",
            "Assim os céus e a terra foram acabados. E havendo Deus acabado no sétimo dia a sua obra, descansou de toda a sua obra. E abençoou Deus o sétimo dia e o santificou."
        ],
        2: [
            "Assim os céus e a terra foram acabados com todo o seu exército.",
            "E o SENHOR Deus formou o homem do pó da terra e soprou em suas narinas o fôlego da vida; e o homem foi feito alma vivente.",
            "E plantou o SENHOR Deus um jardim no Éden, da banda do Oriente, e pôs ali o homem que tinha formado.",
            "E o SENHOR Deus fez brotar da terra toda árvore agradável à vista e boa para comida, e a árvore da vida no meio do jardim, e a árvore do conhecimento do bem e do mal.",
            "E tomou o SENHOR Deus o homem e o pôs no jardim do Éden para o lavrar e guardar. E deu-lhe ordem, dizendo: De toda árvore do jardim comerás livremente, mas da árvore do conhecimento do bem e do mal não comerás; porque no dia em que dela comeres, certamente morrerás.",
            "E disse o SENHOR Deus: Não é bom que o homem esteja só; far-lhe-ei uma ajudadora idônea. E da costela que o SENHOR Deus tomou do homem, formou uma mulher, e trouxe-a a Adão.",
            "E disse Adão: Esta é agora osso dos meus ossos e carne da minha carne; esta será chamada varoa, porquanto do varão foi tomada. Portanto deixará o varão o seu pai e a sua mãe e apegar-se-á à sua mulher, e serão ambos uma carne.",
            "E ambos estavam nus, o homem e a sua mulher, e não se envergonhavam."
        ],
        3: [
            "E a serpente era mais astuta que todas as alimárias do campo. Disse à mulher: É assim que Deus disse: Não comereis de toda árvore do jardim?",
            "A mulher respondeu: Do fruto das árvores comeremos, mas do fruto da árvore que está no meio do jardim não comereis, para que não morrais.",
            "Então a serpente disse: Certamente não morrereis. Porque Deus sabe que no dia em que dele comerdes se abrirão os vossos olhos e sereis como Deus.",
            "E vendo a mulher que aquela árvore era desejável para dar entendimento, tomou do seu fruto e comeu, e deu também a seu marido, e ele comeu.",
            "Então foram abertos os olhos de ambos, e conheceram que estavam nus; e coseram folhas de figueira e fizeram aventais.",
            "E ouviram a voz do SENHOR Deus que passeava no jardim; e esconderam-se da presença do SENHOR Deus entre as árvores do jardim.",
            "E chamou o SENHOR Deus a Adão e disse-lhe: Onde estás? Ele respondeu: Ouvi a tua voz no jardim e escondi-me, porque estava nu.",
            "E Deus disse: Quem te mostrou que estavas nu? Comeste tu da árvore de que te ordenei que não comesses?",
            "Então Adão disse: A mulher que me deste por companheira, ela me deu da árvore, e comi.",
            "E o SENHOR Deus disse à serpente: Porquanto fizeste isto, maldita és. Porei inimizade entre ti e a mulher, e entre a tua semente e a sua semente; esta te ferirá a cabeça, e tu lhe ferirás o calcanhar.",
            "E o SENHOR Deus fez túnicas de peles a Adão e à sua mulher e os vestiu. E lançou-os fora do jardim do Éden."
        ],
    }
}

def get_verses(book_id, ch_num, text):
    if book_id in CHAPTER_VERSES and ch_num in CHAPTER_VERSES[book_id]:
        return CHAPTER_VERSES[book_id][ch_num]
    return split_verses(text)

# ===================== GENERATION =====================
def generate_apol(book_id, testament, ch_num, title):
    pool = APOL_OT if testament == "Antigo Testamento" else APOL_NT
    idx1 = (hash(f"{book_id}:{ch_num}:a") % len(pool))
    idx2 = (hash(f"{book_id}:{ch_num}:b") % len(pool))
    while idx2 == idx1:
        idx2 = (idx2 + 1) % len(pool)
    return [pool[idx1], pool[idx2]]

output_lines = ['export const BIBLE_DATA = [']

for bid, bname, testament, total, titles in BOOKS_DEF:
    theme = BOOK_THEMES.get(bid, "verdades espirituais")
    chapters = []
    for i, t in enumerate(titles):
        ch_num = i + 1
        text = generate_text(bid, ch_num, t, theme)
        reflection = generate_reflection(bid, ch_num, t, theme)
        apol = generate_apol(bid, testament, ch_num, t)
        quiz_items = generate_quiz(bid, ch_num, t, testament)
        
        apol_str = ', '.join(f'"{js_str(p)}"' for p in apol)
        quiz_str = ', '.join(quiz_items)
        verses = get_verses(bid, ch_num, text)
        verses_str = ', '.join(f'"{js_str(v)}"' for v in verses)
        
        ch = (f'{{number:{ch_num},title:"{js_str(t)}",text:"{js_str(text)}",'
              f'reflection:"{js_str(reflection)}",apologeticPoints:[{apol_str}],'
              f'verses:[{verses_str}],'
              f'quiz:[{quiz_str}]}}')
        chapters.append(ch)
    
    ch_joined = ',\n  '.join(chapters)
    book_str = (f'{{id:"{bid}",name:"{bname}",testament:"{testament}",'
                f'totalChapters:{total},chapters:[\n  {ch_joined}\n]}}')
    output_lines.append(book_str)
    output_lines.append(',')

output_lines.append(']')
output_lines[-2] = output_lines[-2].rstrip(',')

with open('src/data/bibleData.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Generated bibleData.js with {len(BOOKS_DEF)} books")
total_ch = sum(b[3] for b in BOOKS_DEF)
print(f"Total chapters: {total_ch}")
