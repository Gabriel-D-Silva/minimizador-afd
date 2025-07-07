def criarAFD(conteudo):
    from automata.fa.dfa import DFA

    alfabeto = conteudo[0][9:].split(',')
    print('alfabeto: ',alfabeto)
    estados = conteudo[1][8:].split(',')
    print('estados: ',estados)
    inicial = conteudo[2][8:].split(',')
    print('inicial: ',inicial)
    finais = conteudo[3][7:].split(',')
    print('finais: ',finais)

    # Cria lista com a base para todas as transicoes
    transicoes = []
    for estado in estados:
        transicoes.append({estado : {}})

    # Deixa somente as transições na lista 'conteudo'
    for i in range(0,5):
        conteudo.pop(0)

    # Iterando por cada transicao do documento   
    for i in conteudo:

        # Transofrmando a transicao numa lista e definindo seus valores
        transicao = i.split(',')

        estado = transicao[0]
        destino = transicao[1]
        valor = transicao[2]

        # Procura o dicionario correspondente a transicao atual e faz a inserção da transição nela
        for j in transicoes:
            if estado in j:
                j[estado][valor] = destino
                break

    # Convertendo a lista 'transicoes' pra um dicionario só
    transicoes_dict = {}
    for item in transicoes:
        transicoes_dict.update(item)
    
    print('transicoes: ',transicoes_dict)
    
    # Definindo a AFD
    afd = DFA(
        states={*estados},
        input_symbols={*alfabeto},
        transitions=transicoes_dict,
        initial_state=inicial[0],
        final_states={*finais}
    )

    return afd

def verificarFormatacao(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]

        # Checa se tem pelo menos as 5 primeiras linhas essenciais
        if len(linhas) < 6:
            return False

        # Checa se as primeiras 5 linhas começam com os cabeçalhos esperados
        if not linhas[0].startswith("alfabeto:"):
            return False
        if not linhas[1].startswith("estados:"):
            return False
        if not linhas[2].startswith("inicial:"):
            return False
        if not linhas[3].startswith("finais:"):
            return False
        if linhas[4].strip().lower() != "transicoes":
            return False

        # Divide e remove espaços de cada item
        alfabeto = set(s.strip() for s in linhas[0].split(":", 1)[1].split(","))
        estados = set(s.strip() for s in linhas[1].split(":", 1)[1].split(","))
        estadoInicial = linhas[2].split(":", 1)[1].strip()
        finais = set(s.strip() for s in linhas[3].split(":", 1)[1].split(","))

        # Checa a validade do estado inicial
        if estadoInicial not in estados:
            return False

        # Checa a validade dos estados finais
        if not finais.issubset(estados):
            return False
        
        # Checa a validade das transições presentes no arquivo
        for i, linha in enumerate(linhas[5:], start=6):
            partes = [p.strip() for p in linha.split(",")]
            if len(partes) != 3:
                return False
            origem, destino, simbolo = partes
            if origem not in estados:
                return False
            if destino not in estados:
                return False
            if simbolo not in alfabeto:
                return False

        return True

    except FileNotFoundError:
        return False
    except Exception as e:
        return False

def aplicarMyhillNerode(afd):
    from gui import mostrarIteraçãoTabela

    estados = sorted(list(afd.states))
    estadosFinais = sorted(list(afd.final_states))
    n = len(estados)
    matriz = [[False] * n for _ in range(n)]

    # Passo 1: Marcar todos os itens da diagonal principal e acima dela
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if (i <= j):
                matriz[i][j] = True
    mostrarIteraçãoTabela(estados, matriz, "Passo 1: Marcar as diagonais \nprincipais e todos os valores \nacima dela")

    # Passo 2: Marcar todos onde P é um estado final e Q não é um estado final
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            # Vê se a iteração não está marcada
            if(matriz[i][j] == False):
                if(((estados[i] in estadosFinais) and (estados[j] not in estadosFinais)) or ((estados[j] in estadosFinais) and (estados[i] not in estadosFinais))):
                    matriz[i][j] = True
    mostrarIteraçãoTabela(estados, matriz, "Passo 2: Marcar os pares onde P∈F e Q∉F")
    
    # Passo 3 (Satânico): Vê se tem algum par não marcado (P,Q) e  
    alterado = True
    while alterado:
        alterado = False
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if not matriz[i][j]:  # Se ainda não está marcado
                    for simbolo in afd.input_symbols:
                        p = afd.transitions[estados[i]].get(simbolo)
                        q = afd.transitions[estados[j]].get(simbolo)

                        if p is None or q is None:
                            continue  # Ignora símbolos que não têm transição

                        # Descobrir as posições na matriz dos estados p e q
                        p_index = estados.index(p)
                        q_index = estados.index(q)

                        if p_index > q_index:
                            p_index, q_index = q_index, p_index

                        if matriz[p_index][q_index]:  # Se os destinos já são distinguíveis
                            matriz[i][j] = True
                            alterado = True
                            break  # Sai do loop de símbolos, já marcou
        mostrarIteraçãoTabela(estados, matriz, "Passo 3: Propagar distinções")

    # Passo 4 Combinar todos os pares não marcados e fazer os estados equivalentes
    classes = []
    usados = set()

    for i in range(len(estados)):
        if estados[i] in usados:
            continue

        nova_classe = {estados[i]}
        usados.add(estados[i])

        for j in range(i + 1, len(estados)):
            if not matriz[i][j]:
                nova_classe.add(estados[j])
                usados.add(estados[j])

        classes.append(nova_classe)

    mostrarIteraçãoTabela(estados, matriz, "Passo 4: Classes de equivalência formadas:\n" + str(classes))
    
    estado_para_classe = {}
    for idx, classe in enumerate(classes):
        for estado in classe:
            estado_para_classe[estado] = f'C{idx}'

    # Criar novo conjunto de estados
    novos_estados = set(estado_para_classe.values())

    # Definir novo estado inicial
    novo_estado_inicial = estado_para_classe[afd.initial_state]

    # Definir novos estados finais
    novos_estados_finais = set()
    for estado in estadosFinais:
        novos_estados_finais.add(estado_para_classe[estado])

    # Definir novas transições
    novas_transicoes = {}
    for idx, classe in enumerate(classes):
        representante = list(classe)[0]
        novas_transicoes[f'C{idx}'] = {}
        for simbolo in afd.input_symbols:
            destino = afd.transitions[representante].get(simbolo)
            if destino:
                novas_transicoes[f'C{idx}'][simbolo] = estado_para_classe[destino]

    # fazer AFD minimizado gloria a deus!
    from automata.fa.dfa import DFA

    afdMinimizada = DFA(
        states=novos_estados,
        input_symbols=afd.input_symbols,
        transitions=novas_transicoes,
        initial_state=novo_estado_inicial,
        final_states=novos_estados_finais
    )
    from visual_automata.fa.dfa import VisualDFA
    VisualDFA(afdMinimizada)
    return afdMinimizada

def selecionarArquivo():
    from tkinter import filedialog
    from tkinter import messagebox
    from visual_automata.fa.dfa import VisualDFA
    path = filedialog.askopenfile(title="Abrir arquivo txt", filetypes=[("Arquivo de texto", "*.txt")], initialdir=".")
    if(verificarFormatacao(path.name)):
        with open(path.name) as arquivo:
            conteudo = arquivo.readlines()
        conteudo = [x.strip('\n') for x in conteudo]
        try:
            afd = criarAFD(conteudo)
            # Criando a caralha visualmente
            nova = VisualDFA(afd)
            nova.show_diagram(view=True)
            afdMinimizada = aplicarMyhillNerode(afd)
        except Exception as e:
            import traceback
            print("Erro ao criar AFD: ", e)
            traceback.print_exc() # Mostra o erro completo no console
            messagebox.showerror(title="Erro ao criar AFD!", message=f"Diagnostico:\n{str(e)}")
    else:
        messagebox.showerror(title="Erro de leitura", message="Verifique se o formato do documento está correto e se segue o padrão estabelecido no exemplo (Se atente para virgulas e espaços e para o fato de só poder haver um estado inicial na AFD). Após isso tente novamente!")

def criarExemplo():
    import os
    from tkinter import filedialog
    from tkinter import messagebox

    diretorioArquivo = filedialog.askdirectory(title ="Selecione a pasta que quer o exemplo", initialdir=".")

    if not diretorioArquivo:
        return
    
    diretorioArquivo = os.path.join(diretorioArquivo, "exemplo.txt")

    with open(diretorioArquivo, "w") as exemplo:
        exemplo.write("alfabeto:a,b\nestados:q0,q1,q2\ninicial:q0\nfinais:q1,q2\ntransicoes\nq0,q1,a\nq0,q0,b\nq1,q0,a\nq1,q2,b\nq2,q1,a\nq2,q2,b")  
        messagebox.showinfo(title="Exemplo .txt criado com sucesso!", message="O exemplo de .txt contendo uma AFD foi criado na pasta selecionada.")