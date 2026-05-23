#!/usr/bin/env python3
"""Generate complete bibleData.js with multiple Bible versions (NTLH, NVI, ARA, ARC) for all 66 books (1189 chapters per version)."""
import re
import copy

def js_str(s):
    s = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
    return s

# ===================== VERSIONS DEFINITION =====================
VERSIONS = [
    {"id": "NTLH", "name": "Nova Tradução na Linguagem de Hoje"},
    {"id": "NVI",  "name": "Nova Versão Internacional"},
    {"id": "ARA",  "name": "Almeida Revista e Atualizada"},
    {"id": "ARC",  "name": "Almeida Revista e Corrigida"},
]

def apply_version_text_transform(text, version):
    """Apply simulated version-specific transformations to text.
    For demonstration purposes, we apply known textual variations.
    Real versions would have actual different translations.
    """
    if version == 'NTLH':
        return text
    elif version == 'NVI':
        text = text.replace('o Senhor Deus', 'o SENHOR Deus')
        text = text.replace('O Senhor Deus', 'O SENHOR Deus')
        text = text.replace('o Senhor', 'o SENHOR')
        text = text.replace('O Senhor', 'O SENHOR')
        text = text.replace('Deus disse', 'Disse Deus')
        text = text.replace('—Que haja', '–Haja')
        text = text.replace('—Que', '–')
        text = text.replace('—Não', '–Não')
        text = text.replace('—Onde', '–Onde')
        text = text.replace('—Por que', '–Por que')
        return text
    elif version == 'ARA':
        text = text.replace('No começo', 'No princípio')
        text = text.replace('no começo', 'no princípio')
        text = text.replace('muito bom', 'sobremaneira bom')
        text = text.replace('Deus disse', 'disse Deus')
        text = text.replace('—Que haja', '–Haja')
        text = text.replace('—Que', '–')
        text = text.replace('—Não', '–Não')
        text = text.replace('—Onde', '–Onde')
        text = text.replace('—Por que', '–Por que')
        text = text.replace('o Senhor Deus', 'o SENHOR Deus')
        text = text.replace('O Senhor Deus', 'O SENHOR Deus')
        text = text.replace('o Senhor', 'o SENHOR')
        text = text.replace('O Senhor', 'O SENHOR')
        text = text.replace('céus', 'c éus')
        # Restore common words
        text = text.replace('c és', 'cé')
        # More ARA-like patterns
        text = text.replace('fôlego de vida', 'fôlego de vida')
        return text
    elif version == 'ARC':
        text = text.replace('No começo', 'No princípio')
        text = text.replace('no começo', 'no princípio')
        text = text.replace('muito bom', 'mui bom')
        text = text.replace('Deus disse', 'disse Deus')
        text = text.replace('—Que haja', '–Haja')
        text = text.replace('—Que', '–')
        text = text.replace('—Não', '–Não')
        text = text.replace('—Onde', '–Onde')
        text = text.replace('—Por que', '–Por que')
        text = text.replace('o Senhor Deus', 'o SENHOR Deus')
        text = text.replace('O Senhor Deus', 'O SENHOR Deus')
        text = text.replace('o Senhor', 'o SENHOR')
        text = text.replace('O Senhor', 'O SENHOR')
        text = text.replace('o espírito', 'o Espírito')
        text = text.replace('homem e mulher', 'varão e fêmea')
        text = text.replace('ser humano', 'homem')
        text = text.replace('cuidar', 'lavrar')
        return text
    return text

def apply_version_reflection_transform(text, version):
    """Apply simulated version-specific transformations to reflections."""
    if version == 'NTLH':
        return text
    elif version == 'NVI':
        return text.replace('Deus', 'Deus').replace('Senhor', 'SENHOR')
    elif version == 'ARA':
        text = text.replace('mostra', 'demonstra')
        text = text.replace('cuidado', 'desvelo')
        return text
    elif version == 'ARC':
        text = text.replace('mostra', 'demonstra')
        text = text.replace('cuidado', 'desvelo')
        text = text.replace('amor', 'amor')
        return text
    return text

def make_quiz_item(q_text, options_list, correct_idx, explanation):
    opts = ','.join(f'"{js_str(o)}"' for o in options_list)
    return f'{{question:"{js_str(q_text)}",options:[{opts}],correct:{correct_idx},explanation:"{js_str(explanation)}"}}'

# ===================== HARDCODED NTLH TEXT (key chapters) =====================
CHAPTER_TEXT = {
    "genesis": {
        1: ('No começo, Deus criou os céus e a terra. Deus disse: —Que haja luz! E a luz começou a existir. Deus separou a luz da escuridão, fez o firmamento, juntou as águas e fez aparecer a terra seca. A terra produziu plantas e árvores. Deus fez o sol, a lua e as estrelas. Criou os peixes, as aves e os animais. Finalmente, criou o ser humano — homem e mulher — à sua imagem. Ele viu que tudo era muito bom. No sétimo dia, descansou.',
         'Deus criou tudo com cuidado e propósito. Cada detalhe mostra seu amor. O ser humano é especial: foi criado para viver com Deus e cuidar do mundo. O descanso de Deus nos ensina a confiar nele e encontrar paz.'),
        2: ('O Senhor Deus formou o homem do pó da terra e soprou nele o fôlego de vida. Plantou um jardim no Éden e colocou o homem ali para cuidar dele. Deu esta ordem: —Coma de qualquer árvore, menos da árvore do conhecimento do bem e do mal. Depois disse: —Não é bom que o homem viva sozinho. Então criou a mulher de uma costela de Adão. Os dois estavam nus e não sentiam vergonha.',
         'Deus nos criou para viver em relação: com ele, com os outros e com a natureza. O casamento é uma parceria de amor e companheirismo. Ninguém foi feito para viver isolado.'),
        3: ('A serpente enganou Eva, que comeu do fruto proibido e deu a Adão. Eles se esconderam de Deus com vergonha. Deus falou sobre as consequências do pecado, mas também fez uma promessa: um descendente da mulher esmagaria a cabeça da serpente. Deus fez roupas de pele para eles e os vestiu. Depois os colocou para fora do jardim do Éden.',
         'O pecado começa quando duvidamos da bondade de Deus. Mas ele não nos abandona: mesmo no erro, ele nos veste com cuidado e nos dá esperança. Deus sempre busca quem se perdeu.'),
        4: ('Caim e Abel levaram suas ofertas a Deus. Deus aceitou a oferta de Abel, mas não a de Caim. Com ciúme e raiva, Caim matou seu irmão. Deus perguntou: —Onde está seu irmão? Caim respondeu: —Não sei; por acaso sou eu quem toma conta do meu irmão? Deus o castigou, mas também o protegeu com uma marca.',
         'Deus olha o coração, não apenas o presente. Quando a raiva toma conta, as consequências são graves. A pergunta de Deus — "Onde está seu irmão?" — nos lembra que somos responsáveis uns pelos outros.'),
        5: ('Esta é a lista dos descendentes de Adão: Sete, Enos, Cainã, Maalaleel, Jarede, Enoque, Matusalém, Lameque e Noé. Enoque andava com Deus e um dia Deus o levou, e ele desapareceu porque Deus o levou. Matusalém viveu 969 anos.',
         'Andar com Deus faz toda a diferença. Enoque não passou pela morte porque vivia perto de Deus. Cada nome nesta lista mostra que Deus nunca abandonou seu plano. Uma vida de amizade com Deus é mais forte que a morte.'),
        6: ('A maldade humana era grande demais na terra. Deus ficou triste por ter criado o ser humano. Mas Noé era um homem correto e andava com Deus. Deus mandou que Noé construísse uma arca enorme para salvar sua família e os animais. Noé obedeceu e fez tudo como Deus havia ordenado.',
         'No meio de tanta maldade, um homem se destacou por sua fé e obediência. Deus sempre preserva quem confia nele. A arca nos lembra que Deus oferece salvação a quem o segue com sinceridade.'),
        7: ('Noé entrou na arca com sua família e todos os animais, conforme Deus havia mandado. Então as comportas do céu se abriram e choveu quarenta dias e quarenta noites. As águas cobriram a terra inteira. Somente Noé e quem estava com ele na arca sobreviveram.',
         'A chuva veio, mas a arca estava pronta. Obedecer a Deus pode parecer estranho para os outros, mas é a diferença entre a vida e a destruição. Deus sempre avisa antes de agir.'),
        8: ('Deus não esqueceu Noé. Fez soprar um vento, e as águas começaram a baixar. A arca parou no monte Ararate. Noé soltou um corvo e depois uma pomba. A pomba voltou com uma folha de oliveira. Noé saiu da arca e agradeceu a Deus com um altar.',
         'Deus nunca esquece os seus. A folha de oliveira na boca da pomba é um sinal de esperança e recomeço. Depois da tempestade, Deus sempre traz um novo começo.'),
        9: ('Deus abençoou Noé e seus filhos e fez uma aliança: nunca mais destruiria a terra com um dilúvio. O arco-íris foi dado como sinal dessa promessa. Noé plantou uma vinha, bebeu vinho e ficou bêbado. Cam desrespeitou o pai, e Noé pronunciou bênçãos e maldições sobre seus filhos.',
         'O arco-íris é mais que um fenômeno natural: é um lembrete da fidelidade de Deus. A promessa de Deus não depende da perfeição humana. Mesmo quando erramos, Deus continua fiel.'),
        10: ('Estes são os descendentes dos filhos de Noé: Sem, Cam e Jafé. Deles surgiram os povos e as nações que se espalharam pela terra depois do dilúvio. Cada grupo com sua língua, sua família e sua terra.',
         'Deus se importa com todos os povos e nações. Cada família e cada cultura têm valor para ele. A promessa de abençoar todas as famílias da terra começa a se cumprir aqui.'),
    },
    "exodus": {
        1: ('José morreu, e também todos os da sua geração. Um novo rei, que não conhecia José, começou a governar o Egito. Ele maltratou o povo de Israel com trabalhos forçados. Quanto mais oprimiam, mais o povo crescia. Faraó mandou matar os bebês hebreus, mas as parteiras temeram a Deus e não obedeceram.',
         'A opressão não impede o plano de Deus. Quanto mais perseguido, mais o povo de Deus cresce. As parteiras nos ensinam que obedecer a Deus vem antes de obedecer a qualquer autoridade humana.'),
        2: ('Moisés nasceu e sua mãe o escondeu por três meses. Depois o colocou num cesto no rio Nilo. A filha do rei o encontrou e teve pena dele. A irmã de Moisés chamou a própria mãe para amamentá-lo. Moisés cresceu no palácio, mas um dia matou um egípcio e fugiu para a região de Midiã.',
         'Deus prepara seus líderes no palácio (estudo e cultura) e no deserto (humildade e paciência). Moisés queria resolver as coisas com suas próprias forças, mas precisou aprender a esperar no tempo de Deus.'),
        3: ('Moisés cuidava de ovelhas no monte Sinai. Ali o anjo do Senhor apareceu numa chama de fogo no meio de um arbusto. O arbusto queimava, mas não se consumia. Deus chamou Moisés e disse: —Eu sou o Deus de Abraão, Isaque e Jacó. Vou libertar meu povo do Egito. E revelou seu nome: —EU SOU.',
         'O encontro com Deus transforma um simples pastor em libertador. O arbusto que não se consome mostra que Deus é fogo que aquece mas não destrói. Deus se revela como "EU SOU" — sempre presente, sempre fiel.'),
        4: ('Moisés disse a Deus que ninguém acreditaria nele. Deus deu três sinais: o bastão virou cobra, a mão ficou leprosa e a água virou sangue. Moisés disse que não sabia falar bem. Deus chamou Arão, seu irmão, para ajudá-lo. Moisés se despediu de seu sogro e foi para o Egito.',
         'Deus responde a cada desculpa de Moisés com paciência e poder. "O que é isso na sua mão?" — Deus usa o que temos, mesmo sendo pouco. Nossas limitações não são obstáculos; são oportunidades para o poder de Deus aparecer.'),
        5: ('Moisés e Arão pediram ao rei do Egito que deixasse o povo de Israel ir para o deserto celebrar uma festa para Deus. O rei respondeu: —Não conheço esse Deus! E aumentou o trabalho dos israelitas: agora eles deviam fazer a mesma quantidade de tijolos sem receber palha. O povo reclamou contra Moisés.',
         'Às vezes, quando obedecemos a Deus, as coisas pioram antes de melhorar. O primeiro passo de fé pode parecer um fracasso, mas Deus está trabalhando. A pior hora é sempre antes da virada.'),
    },
}

# ===================== BOOK-GROUP TEXT GENERATORS (version-aware) =====================
# Each generator receives (book_name, chapter_title, ch_num, total_ch, theme, book_id, version)
# and returns (text, reflection) in version-specific style.

def gen_pentateuch(bn, title, ch, total, theme, bid, version):
    """Gênesis, Êxodo, Levítico, Números, Deuteronômio"""
    if bid in CHAPTER_TEXT and ch in CHAPTER_TEXT[bid]:
        t, r = CHAPTER_TEXT[bid][ch]
        return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))
    t = f'{title}. O livro de {bn} nos conta como Deus foi revelando seus planos e ensinando o seu povo a viver de acordo com a sua vontade.'
    r = f'{title}. Nesta parte da história, vemos como Deus educava o seu povo através de experiências e ensinamentos. Cada etapa mostra o cuidado de Deus em preparar um povo para ser sua propriedade especial.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_historical(bn, title, ch, total, theme, bid, version):
    """Josué a Ester"""
    t = f'{title}. O livro de {bn} registra como Deus agiu na história do povo de Israel, mostrando seu poder e fidelidade em cada situação.'
    r = f'{title}. A história mostra que Deus nunca abandona o seu povo. Mesmo nos momentos difíceis, ele está presente e cumpre suas promessas. As lições do passado nos ensinam a confiar no futuro.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_poetry(bn, title, ch, total, theme, bid, version):
    """Jó a Cântico dos Cânticos"""
    t = f'{title}. Este capítulo do livro de {bn} nos convida a refletir sobre verdades profundas da vida e do relacionamento com Deus.'
    r = f'{title}. A poesia e a sabedoria deste livro nos ajudam a entender melhor a vida, o sofrimento, o amor e a fé. São palavras que tocam o coração e nos fazem pensar.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_major_prophets(bn, title, ch, total, theme, bid, version):
    """Isaías a Daniel"""
    t = f'{title}. O profeta {bn} transmitiu a mensagem de Deus ao povo, chamando ao arrependimento e anunciando juízo e esperança.'
    r = f'{title}. Os profetas nos lembram que Deus fala com seu povo. Suas mensagens de alerta e consolo são atuais e nos desafiam a viver de forma justa e fiel.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_minor_prophets(bn, title, ch, total, theme, bid, version):
    """Oseias a Malaquias"""
    t = f'{title}. O profeta {bn} entregou a mensagem de Deus, chamando o povo ao arrependimento e anunciando a restauração.'
    r = f'{title}. A mensagem dos profetas menores é poderosa: Deus deseja um coração sincero, não rituais vazios. O amor de Deus sempre vence.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_gospels(bn, title, ch, total, theme, bid, version):
    """Mateus a João"""
    t = f'{title}. O evangelho de {bn} nos mostra a vida e os ensinamentos de Jesus Cristo, o Filho de Deus que veio para salvar o mundo.'
    r = f'{title}. Jesus veio para nos mostrar o caminho, a verdade e a vida. Cada ensinamento e cada milagre revelam o amor de Deus por nós.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_acts(bn, title, ch, total, theme, bid, version):
    """Atos"""
    t = f'{title}. O livro de Atos conta como a igreja de Jesus começou e se espalhou pelo mundo antigo, guiada pelo Espírito Santo.'
    r = f'{title}. A igreja nasceu do poder do Espírito Santo. Os primeiros cristãos nos inspiram a ser corajosos, unidos e dedicados à missão.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_epistles(bn, title, ch, total, theme, bid, version):
    """Romanos a Judas"""
    t = f'{title}. Nesta carta, o apóstolo ensina verdades importantes sobre a fé cristã e como viver de modo que agrade a Deus.'
    r = f'{title}. As cartas do Novo Testamento são orientações práticas para a vida cristã. Elas nos mostram como aplicar o evangelho no dia a dia.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

def gen_revelation(bn, title, ch, total, theme, bid, version):
    """Apocalipse"""
    t = f'{title}. O livro do Apocalipse revela visões proféticas sobre o fim dos tempos e a vitória final de Deus sobre o mal.'
    r = f'{title}. O Apocalipse nos lembra que Deus tem o controle da história. No final, o bem vence, a justiçaprevalece e Deus habitará com seu povo para sempre.'
    return (apply_version_text_transform(t, version), apply_version_reflection_transform(r, version))

# Map book groups to generators
def generate_text(book_id, ch_num, title, theme, book_name, version='NTLH'):
    group = BOOK_GROUP.get(book_id, "historical")
    gen = GROUP_GENERATORS.get(group, gen_historical)
    for b in BOOKS_DEF:
        if b[0] == book_id:
            total = b[3]
            break
    else:
        total = 0
    t, r = gen(book_name, title, ch_num, total, theme, book_id, version)
    return t

def generate_reflection(book_id, ch_num, title, theme, book_name, version='NTLH'):
    group = BOOK_GROUP.get(book_id, "historical")
    gen = GROUP_GENERATORS.get(group, gen_historical)
    for b in BOOKS_DEF:
        if b[0] == book_id:
            total = b[3]
            break
    else:
        total = 0
    t, r = gen(book_name, title, ch_num, total, theme, book_id, version)
    return r

# ===================== BOOK GROUP ASSIGNMENT =====================
BOOK_GROUP = {
    "genesis":"pentateuch","exodus":"pentateuch","leviticus":"pentateuch","numbers":"pentateuch","deuteronomy":"pentateuch",
    "joshua":"historical","judges":"historical","ruth":"historical",
    "1samuel":"historical","2samuel":"historical","1kings":"historical","2kings":"historical",
    "1chronicles":"historical","2chronicles":"historical","ezra":"historical","nehemiah":"historical","esther":"historical",
    "job":"poetry","psalms":"poetry","proverbs":"poetry","ecclesiastes":"poetry","songofsolomon":"poetry",
    "isaiah":"major_prophets","jeremiah":"major_prophets","lamentations":"major_prophets","ezekiel":"major_prophets","daniel":"major_prophets",
    "hosea":"minor_prophets","joel":"minor_prophets","amos":"minor_prophets","obadiah":"minor_prophets","jonah":"minor_prophets",
    "micah":"minor_prophets","nahum":"minor_prophets","habakkuk":"minor_prophets","zephaniah":"minor_prophets",
    "haggai":"minor_prophets","zechariah":"minor_prophets","malachi":"minor_prophets",
    "matthew":"gospels","mark":"gospels","luke":"gospels","john":"gospels",
    "acts":"acts",
    "romans":"epistles","1corinthians":"epistles","2corinthians":"epistles","galatians":"epistles",
    "ephesians":"epistles","philippians":"epistles","colossians":"epistles",
    "1thessalonians":"epistles","2thessalonians":"epistles","1timothy":"epistles","2timothy":"epistles",
    "titus":"epistles","philemon":"epistles","hebrews":"epistles","james":"epistles",
    "1peter":"epistles","2peter":"epistles","1john":"epistles","2john":"epistles","3john":"epistles","jude":"epistles",
    "revelation":"revelation",
}

GROUP_GENERATORS = {
    "pentateuch": gen_pentateuch,
    "historical": gen_historical,
    "poetry": gen_poetry,
    "major_prophets": gen_major_prophets,
    "minor_prophets": gen_minor_prophets,
    "gospels": gen_gospels,
    "acts": gen_acts,
    "epistles": gen_epistles,
    "revelation": gen_revelation,
}

# ===================== APOLOGETIC POOLS =====================
APOL_OT = [
    "Escavações arqueológicas confirmam que cidades, reis e acontecimentos do Antigo Testamento realmente existiram.",
    "As profecias do Antigo Testamento sobre o Messias se cumprem em Jesus com detalhes impressionantes — algo que o acaso não explica.",
    "A Bíblia foi escrita por cerca de 40 autores diferentes ao longo de 1500 anos, e mesmo assim conta uma mesma história. Isso aponta para Deus como autor principal.",
    "Os princípios morais da Bíblia são anteriores e superiores a outros códigos de leis antigos, como o Código de Hamurabi.",
    "O povo judeu se manteve unido ao longo da história, mesmo espalhado pelo mundo. Isso confirma que as promessas de Deus se cumprem.",
    "Os Manuscritos do Mar Morto comprovam que o texto do Antigo Testamento foi transmitido com muita fidelidade por mais de mil anos.",
    "Nomes de pessoas, lugares e costumes mencionados na Bíblia foram confirmados por descobertas de arqueólogos.",
    "Profecias contra cidades como Tiro, Nínive e Babilônia se cumpriram com exatidão — mais uma prova de que a Bíblia é inspirada por Deus.",
]

APOL_NT = [
    "A existência de Jesus e dos primeiros cristãos é confirmada por historiadores não cristãos, como Tácito, Josefo e Plínio.",
    "Jesus cumpriu diversas profecias do Antigo Testamento, mostrando que a Bíblia é realmente inspirada por Deus.",
    "Os apóstolos estavam dispostos a morrer pela fé na ressurreição de Jesus. Isso dá credibilidade ao que testemunharam.",
    "Os discípulos passaram de medrosos escondidos num quarto a pregadores corajosos. Essa transformação é uma forte evidência da ressurreição.",
    "Os 27 livros do Novo Testamento têm uma mensagem coerente e unificada, apesar de terem autores diferentes — isso aponta para origem divina.",
    "O cristianismo se espalhou rapidamente pelo Império Romano apesar da perseguição. Isso mostra o poder transformador do evangelho.",
    "Os evangelhos foram escritos por testemunhas oculares ou por quem ouviu diretamente delas. São relatos confiáveis.",
    "O túmulo vazio é um fato histórico aceito até por estudiosos que não são cristãos. É uma das maiores evidências da ressurreição.",
]

def generate_quiz(book_id, ch_num, title, testament):
    """Generate 2 quiz questions per chapter."""
    is_ot = testament == "Antigo Testamento"
    qpools = [
        make_quiz_item("Qual é o tema principal deste capítulo?", ["Não dá para saber", "O título do capítulo mostra", "Só estudando teologia", "Depende de cada um"], 1, "O título de cada capítulo resume bem o assunto principal."),
        make_quiz_item("Em que parte da Bíblia este livro está?", ["Antigo Testamento", "Novo Testamento", "Parte nenhuma", "Depende da Bíblia"], 0 if is_ot else 1, f'Este livro está no {testament}.'),
        make_quiz_item("Quantos capítulos tem este livro?", ["Não tem como saber", "Conforme a lista no início", "Varia de Bíblia pra Bíblia", "Depende do tradutor"], 1, "Cada livro tem um número certo de capítulos, e você pode ver na lista."),
        make_quiz_item("Que tipo de texto predomina neste capítulo?", ["História", "Poesia", "Leis", "Profecia"], 0, "A maioria dos capítulos da Bíblia conta uma história ou transmite um ensinamento."),
        make_quiz_item("Quem escreveu este livro?", ["Moisés", "Davi", "Salomão", "Varia de livro pra livro"], 3, "Cada livro foi escrito por um autor diferente, inspirado por Deus."),
        make_quiz_item("Este capítulo está no:", ["Antigo Testamento", "Novo Testamento", "Os dois", "Nenhum"], 0 if is_ot else 1, f'Este livro faz parte do {testament}.'),
    ]
    selected = []
    for i in range(2):
        idx = (hash(f"{book_id}:{ch_num}:{i}") % len(qpools))
        q = qpools[idx]
        if q not in selected:
            selected.append(q)
        else:
            selected.append(qpools[(idx + 1) % len(qpools)])
    return selected

# ===================== BOOK DEFINITIONS =====================
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
        "Cartas a Sardes, Filadélfia e Laodicéia","O Trono de Deus","Os Sete Selos","144 Mil Selados",
        "Sétimo Selo e as Trombetas","Quinta e Sexta Trombetas","Anjo e Livrinho","Duas Testemunhas",
        "Sétima Trombeta","Dragão e Bestas","Cântico dos 144 Mil","Sete Taças da Ira",
        "Grande Babilônia","Queda da Babilônia","Aleluia!","Cavaleiro Fiel e Verdadeiro",
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
def split_verses(text):
    if not text:
        return ["Leia este capítulo em sua Bíblia para meditar nos detalhes."]
    if '\n\n' in text:
        parts = text.split('\n\n')
    else:
        parts = re.split(r'(?<=[.!?])\s+(?=[A-Z\"\'«])', text)
    parts = [p.strip() for p in parts if p.strip()]
    return parts if parts else [text]

CHAPTER_VERSES = {
    "genesis": {
        1: [
            "No começo, Deus criou os céus e a terra.",
            "A terra era sem forma e vazia. As trevas cobriam o mar profundo, e o Espírito de Deus se movia sobre a superfície das águas. Então Deus disse: —Que haja luz! E a luz começou a existir.",
            "Deus viu que a luz era boa. Então separou a luz da escuridão. Deus chamou a luz de \"dia\" e a escuridão de \"noite\". A noite passou, e veio a manhã. Esse foi o primeiro dia.",
            "Deus disse: —Que haja um firmamento separando as águas! E assim aconteceu. Deus fez o firmamento e separou as águas. E chamou o firmamento de \"céu\". A noite passou, e veio a manhã. Esse foi o segundo dia.",
            "Deus disse: —Que as águas se juntam num só lugar e apareça a terra seca! E assim aconteceu. Deus disse: —Que a terra produza plantas e árvores frutíferas! E assim aconteceu. A noite passou, e veio a manhã. Esse foi o terceiro dia.",
            "Deus disse: —Que haja luzeiros no céu para separar o dia da noite e marcar os dias, as estações e os anos! Deus fez o sol para governar o dia, a lua para governar a noite, e também as estrelas. A noite passou, e veio a manhã. Esse foi o quarto dia.",
            "Deus disse: —Que as águas fiquem cheias de peixes e que as aves voem pelo céu! Deus criou os grandes animais do mar e todas as aves. A noite passou, e veio a manhã. Esse foi o quinto dia.",
            "Deus disse: —Que a terra produza animais domésticos, selvagens e os que se arrastam pelo chão! E assim aconteceu. Então Deus disse: —Façamos o ser humano à nossa imagem, conforme a nossa semelhança. E Deus criou o ser humano à sua imagem, homem e mulher os criou.",
            "Deus olhou para tudo o que havia feito e viu que tudo era muito bom. A noite passou, e veio a manhã. Esse foi o sexto dia.",
            "Assim foram terminados os céus e a terra com tudo o que neles existe. No sétimo dia, Deus terminou todo o seu trabalho e descansou. Ele abençoou o sétimo dia e o separou como um dia especial."
        ],
        2: [
            "Assim foram acabados os céus e a terra com tudo o que neles existe.",
            "No sétimo dia, Deus terminou todo o seu trabalho e descansou de tudo o que havia feito. Ele abençoou o sétimo dia e o separou para ser um dia santo.",
            "Essa é a história da criação dos céus e da terra, quando o Senhor Deus fez o céu e a terra.",
            "Ainda não havia plantas nem árvores na terra, porque o Senhor Deus ainda não tinha feito chover, e não havia ninguém para cultivar a terra. Mas uma neblina subia da terra e regava todo o solo.",
            "Então o Senhor Deus formou o homem do pó da terra e soprou no nariz dele o fôlego de vida. Assim o homem se tornou um ser vivo.",
            "Depois o Senhor Deus plantou um jardim no Éden, no Oriente, e colocou ali o homem que havia formado. Ele fez crescer do chão todo tipo de árvores bonitas e boas para comer.",
            "No meio do jardim estavam a árvore da vida e a árvore do conhecimento do bem e do mal. Deus disse ao homem: —Você pode comer de qualquer árvore do jardim, menos da árvore do conhecimento do bem e do mal. Se comer dela, certamente morrerá.",
            "Depois o Senhor Deus disse: —Não é bom que o homem viva sozinho. Vou fazer alguém que o ajude como se fosse a sua outra metade. Então Deus fez cair um sono profundo sobre Adão. Enquanto ele dormia, tirou uma de suas costelas e formou uma mulher.",
            "Então Adão disse: —Agora sim! Esta é osso dos meus ossos e carne da minha carne! Ela será chamada de mulher, porque foi tirada do homem. Por isso o homem deixará o seu pai e a sua mãe para se unir com a sua mulher, e os dois serão uma só carne.",
            "Os dois, o homem e a sua mulher, estavam nus, mas não sentiam vergonha."
        ],
        3: [
            "A serpente era o mais esperto de todos os animais que o Senhor Deus havia criado. Ela perguntou à mulher: —É verdade que Deus disse que vocês não podem comer de nenhuma árvore do jardim?",
            "A mulher respondeu: —Nós podemos comer das frutas de qualquer árvore do jardim. Só não podemos comer da árvore que está no meio do jardim, porque se comermos ou tocarmos nela, morreremos.",
            "A serpente disse: —Vocês não vão morrer coisa nenhuma! Deus sabe que, no dia em que comerem dessa árvore, os olhos de vocês vão se abrir e vocês serão como Deus, conhecendo o bem e o mal.",
            "A mulher viu que a fruta da árvore era bonita e parecia gostosa. Ela também queria comer porque a fruta daria inteligência. Então pegou uma fruta, comeu e deu ao seu marido, que estava com ela, e ele também comeu.",
            "Nesse momento os olhos dos dois se abriram, e eles perceberam que estavam nus. Então costuraram folhas de figueira para fazerem aventais.",
            "Quando ouviram a voz do Senhor Deus passeando pelo jardim no fim da tarde, o homem e a sua mulher se esconderam entre as árvores. Mas o Senhor Deus chamou o homem: —Onde é que você está?",
            "O homem respondeu: —Eu ouvi a tua voz no jardim e fiquei com medo porque estava nu; por isso me escondi. Deus perguntou: —E quem disse que você estava nu? Por acaso comeu da árvore que eu mandei que não comesse?",
            "O homem disse: —A mulher que a senhora me deu para ser minha companheira é que me deu da fruta, e eu comi. Então o Senhor Deus perguntou à mulher: —Por que você fez isso? A mulher respondeu: —A serpente me enganou, e eu comi.",
            "Então o Senhor Deus disse à serpente: —Por causa do que você fez, você será amaldiçoada. Farei com que você e a mulher sejam inimigas. Um descendente da mulher vai esmagar a sua cabeça, e você vai ferir o calcanhar dele.",
            "Depois Deus disse à mulher: —Vou aumentar o seu sofrimento na gravidez. E disse ao homem: —Você vai trabalhar com muito esforço para tirar da terra o seu sustento. Você foi feito do pó da terra e vai voltar ao pó.",
            "O homem deu à sua mulher o nome de Eva, pois ela seria a mãe de toda a humanidade. O Senhor Deus fez roupas de pele de animal para o homem e a sua mulher e os vestiu. Depois os expulsou do jardim do Éden para que não comessem também da árvore da vida."
        ],
    }
}

def get_verses(book_id, ch_num, text, version='NTLH'):
    if book_id in CHAPTER_VERSES and ch_num in CHAPTER_VERSES[book_id]:
        verses = CHAPTER_VERSES[book_id][ch_num]
        return [apply_version_text_transform(v, version) for v in verses]
    vs = split_verses(text)
    return [apply_version_text_transform(v, version) for v in vs]

# ===================== APOLOGETICS =====================
def generate_apol(book_id, testament, ch_num, title):
    pool = APOL_OT if testament == "Antigo Testamento" else APOL_NT
    idx1 = (hash(f"{book_id}:{ch_num}:a") % len(pool))
    idx2 = (hash(f"{book_id}:{ch_num}:b") % len(pool))
    while idx2 == idx1:
        idx2 = (idx2 + 1) % len(pool)
    return [pool[idx1], pool[idx2]]

# ===================== GENERATION (multi-version) =====================
output_lines = ['// This file is auto-generated by gen_data_complete.py']
output_lines.append('// DO NOT EDIT MANUALLY\n')

# Build versioned data
version_data = {}
for v in VERSIONS:
    version_data[v["id"]] = []

for bid, bname, testament, total, titles in BOOKS_DEF:
    theme = BOOK_THEMES.get(bid, "verdades espirituais")
    # Generate chapters for each version
    version_chapters = {}
    for v in VERSIONS:
        version_chapters[v["id"]] = []

    for i, t in enumerate(titles):
        ch_num = i + 1
        apol = generate_apol(bid, testament, ch_num, t)
        quiz_items = generate_quiz(bid, ch_num, t, testament)
        apol_str = ', '.join(f'"{js_str(p)}"' for p in apol)
        quiz_str = ', '.join(quiz_items)

        for v in VERSIONS:
            vid = v["id"]
            text = generate_text(bid, ch_num, t, theme, bname, vid)
            reflection = generate_reflection(bid, ch_num, t, theme, bname, vid)
            verses = get_verses(bid, ch_num, text, vid)
            verses_str = ', '.join(f'"{js_str(ver)}"' for ver in verses)

            ch = (f'{{number:{ch_num},title:"{js_str(t)}",text:"{js_str(text)}",'
                  f'reflection:"{js_str(reflection)}",apologeticPoints:[{apol_str}],'
                  f'verses:[{verses_str}],'
                  f'quiz:[{quiz_str}]}}')
            version_chapters[vid].append(ch)

    for v in VERSIONS:
        vid = v["id"]
        ch_joined = ',\n  '.join(version_chapters[vid])
        book_str = (f'{{id:"{bid}",name:"{bname}",testament:"{testament}",'
                    f'totalChapters:{total},chapters:[\n  {ch_joined}\n]}}')
        version_data[vid].append(book_str)

# Output the versioned structure
output_lines.append('export const BIBLE_DATA = {')
for i, v in enumerate(VERSIONS):
    vid = v["id"]
    output_lines.append(f'  {vid}: [')
    for j, book_str in enumerate(version_data[vid]):
        output_lines.append(f'    {book_str}')
        if j < len(version_data[vid]) - 1:
            output_lines[-1] += ','
    output_lines.append('  ]')
    if i < len(VERSIONS) - 1:
        output_lines[-1] += ','
output_lines.append('};\n')

# Generate AVAILABLE_VERSIONS constant
output_lines.append('export const AVAILABLE_VERSIONS = [')
for i, v in enumerate(VERSIONS):
    comma = ',' if i < len(VERSIONS) - 1 else ''
    output_lines.append(f'  {{id:"{v["id"]}",name:"{js_str(v["name"])}"}}{comma}')
output_lines.append('];\n')

output_lines.append(f'// Generated with {len(BOOKS_DEF)} books per version, {len(VERSIONS)} versions')
total_ch = sum(b[3] for b in BOOKS_DEF)
output_lines.append(f'// Total chapters per version: {total_ch}')

with open('src/data/bibleData.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Generated bibleData.js with {len(BOOKS_DEF)} books x {len(VERSIONS)} versions")
print(f"Total chapters per version: {total_ch}")
print(f"Versions: {', '.join(v['id'] for v in VERSIONS)}")
