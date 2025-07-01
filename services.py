def criarAFD(conteudo):
    from automata.fa.dfa import DFA

    alfabeto = conteudo[0][9:].split(',')
    print('alfabeto: ',alfabeto)
    estados = conteudo[1].strip("estados:").split(',')
    print('estados: ',estados)
    inicial = conteudo[2].strip("inicial:").split(',')
    print('inicial: ',inicial)
    finais = conteudo[3].strip("finais:").split(',')
    print('finais: ',finais)

    # Cria lista com a base para todas as transicoes
    transicoes = []
    for estado in estados:
        transicoes.append({estado : {}})
    #print(transicoes)

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

def selecionarArquivo():
    filetypes = (("Arquivos de texto", "*.txt"))
    from tkinter import filedialog
    from tkinter import messagebox
    path = filedialog.askopenfile(title="Abrir arquivo txt", filetypes=[("texto", "*.txt")])
    with open(path.name) as arquivo:
        conteudo = arquivo.readlines()
    conteudo = [x.strip('\n') for x in conteudo]
    try:
        criarAFD(conteudo)
    except:
        messagebox.showerror(title="Erro de leitura", message="Verifique se o formato do documento está correto e se segue o padrão estabelecido no exemplo(Se atente para virgulas e espaços). Após isso tente novamente!  ")
    


    
    

def criarExemplo():

    from pathlib import Path
    from tkinter import messagebox

    path = Path.home() / "Desktop"

    exemplo = open(f"{path}\\exemplo.txt", "w")
    exemplo.write("alfabeto:a,b,c,d\nestados:q0,q1,q2\ninicial:q0\nfinais:q1,q2\ntransicoes\nq0,q1,a\nq0,q0,b\nq1,q0,a\nq1,q2,b\nq2,q1,a\nq2,q2,b")
        
    messagebox.showinfo(title="Exemplo .txt criado com sucesso!", message="O exemplo de .txt contendo uma AFD foi criado na sua area de trabalho.")