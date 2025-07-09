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
    from automata.fa.dfa import DFA

    alfabeto = sorted(afd.input_symbols)
    estados = sorted(list(afd.states))
    estadosFinais = sorted(list(afd.final_states))
    transicoes = afd.transitions
    n = len(estados)
    matriz = [[False] * n for _ in range(n)]

    # Passo 1: Marcar todos os itens da diagonal principal e acima dela
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if (i <= j):
                matriz[i][j] = None
    mostrarIteraçãoTabela(estados, matriz, "Passo 1: Desconsiderar as diagonais \nprincipais e todos os valores \nacima dela", 1)

    # Passo 2: Marcar todos onde P é um estado final e Q não é um estado final
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            # Vê se a iteração não está marcada
            if(matriz[i][j] == False):
                if(((estados[i] in estadosFinais) and (estados[j] not in estadosFinais)) or ((estados[j] in estadosFinais) and (estados[i] not in estadosFinais))):
                    matriz[i][j] = True
    mostrarIteraçãoTabela(estados, matriz, "Passo 2: Marcar os pares onde P∈F e Q∉F", 2)
    
    # Passo 3: Propagar distinções
    alterado = True
    while alterado:
        alterado = False  # Começa assumindo que nada será marcado
        for i in range(len(matriz)):
                for j in range(len(matriz[i])):
                    # Vê se a iteração está na parte valida da matriz triangular
                    if not (i <= j):
                        # Vê se a iteração atual não está marcada
                        if (matriz[i][j] == False):
                            p = estados[j]
                            q = estados[i]
                            # Itera sobre os simbolos do alfabeto da afd
                            for simbolo in alfabeto:
                                pIndex = estados.index(p)
                                qIndex = estados.index(q)

                                δP = transicoes.get(p).get(simbolo)
                                δQ = transicoes.get(q).get(simbolo)

                                if (δP > δQ):
                                    if (matriz[estados.index(δP)][estados.index(δQ)] == True):
                                        matriz[pIndex][qIndex] = True
                                        alterado = True  # Houve alteração, então repete o while
                                        break  # Não precisa testar mais símbolos para esse par
                                else:
                                    if (matriz[estados.index(δQ)][estados.index(δP)] == True):
                                        matriz[qIndex][pIndex] = True
                                        alterado = True  # Houve alteração, então repete o while
                                        break  # Não precisa testar mais símbolos para esse par
    mostrarIteraçãoTabela(estados, matriz, "Passo 3: Para pares não marcados [P,Q], \ntal que (δ[P,x],δ[Q,x]) está marcado, \nmarcar [P,Q]", 3)

    # Passo 4: Criar estados simplificadas
    from util import agruparEstadosComuns

    combinacoes = []
    for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if (matriz[i][j] == False):
                    combinacao = []

                    p = estados[j]
                    q = estados[i]

                    combinacao.append(p)
                    combinacao.append(q)

                    combinacoes.append(combinacao)
    agrupamentos = agruparEstadosComuns(combinacoes)
    for estado in estados:
        if estado not in (set().union(*agrupamentos)):
            agrupamentos.append([estado])
    novosEstados = []
    for agrupamento in agrupamentos:
        agrupamento_ordenado = sorted(agrupamento)
        nome_estado = '_'.join(agrupamento_ordenado)
        novosEstados.append(nome_estado)
    mostrarIteraçãoTabela(estados, False, "Passo 4: Criar os estados simplificados: "+str(novosEstados), 4)

    print('estados antigos: ',estados)
    print('transicoes antigas:',transicoes)
    print('novosEstados:',novosEstados)

    # Finalmente, criar a afd simplificada

    # Definir estado inicial
    novoEstadoInicial = []
    for estado in novosEstados:
        if (afd.initial_state in estado):
            novoEstadoInicial.append(estado)
            break

    # Definir estados finais
    novosEstadosFinais = []
    for estadoFinal in estadosFinais:
        for estado in novosEstados:
            if (estadoFinal in estado):
                novosEstadosFinais.append(estado)
    novosEstadosFinais = list(set(novosEstadosFinais))

    # Definir transições
    from util import extrair_membros

    # Mapeia cada estado original para seu grupo minimizado
    mapeamento = {}
    for grupo in novosEstados:
        membros = extrair_membros(grupo, estados)
        for estado in membros:
            mapeamento[estado] = grupo

    novasTransicoes = {grupo: {} for grupo in novosEstados}

    # Para cada novo estado (grupo), analisar as transições de seus membros
    try:
        for grupo in novosEstados:
            membros = extrair_membros(grupo, estados)
            for simbolo in alfabeto:
                destinos = set()
                for estado in membros:
                    if simbolo in transicoes[estado]:
                        destino = transicoes[estado][simbolo]
                        grupo_destino = mapeamento[destino]
                        destinos.add(grupo_destino)

                if len(destinos) == 1:
                    destino_unico = destinos.pop()
                    novasTransicoes[grupo][simbolo] = destino_unico
                elif len(destinos) > 1:
                        from tkinter import messagebox
                        messagebox.showerror(
                            title="Erro: AFD inválido",
                            message=(
                                f"Erro ao tentar simplificar o AFD.\n\n"
                                f"O grupo {grupo} tem múltiplos destinos para o símbolo '{simbolo}':\n{destinos}\n\n"
                                "Isso indica que a simplificação produziu um AFN (não-determinístico), o que não é permitido.\n\n"
                                "Verifique a implementação da tabela de minimização."
                            )
                        )
                        raise ValueError("Minimização inválida — resultou em não-determinismo.")
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror(title="Erro ao criar novas transições", message=f"Diagnostico:\n{str(e)}")
    except ValueError as e:
        pass
    print(novasTransicoes)

    try:
        afdSimplificada = DFA(
            states={*novosEstados},
            input_symbols={*alfabeto},
            transitions=novasTransicoes,
            initial_state=novoEstadoInicial[0],
            final_states={*novosEstadosFinais}
        )
        return afdSimplificada
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror(title="Erro ao gerar AFD simplificada!", message=f"Diagnostico:\n{str(e)}")

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
            afdMinimizada = aplicarMyhillNerode(afd)
            imagem = VisualDFA(afdMinimizada)
            imagem.show_diagram(view=True)
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
        exemplo.write("alfabeto:0,1\nestados:a,b,c,d,e,f\ninicial:a\nfinais:c,d,e\ntransicoes\na,c,1\na,b,0\nb,d,1\nb,a,0\nc,e,0\nc,f,1\nd,f,1\nd,e,0\ne,e,0\ne,f,1\nf,f,1\nf,f,0")  
        messagebox.showinfo(title="Exemplo .txt criado com sucesso!", message="O exemplo de .txt contendo uma AFD foi criado na pasta selecionada.")