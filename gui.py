from services import *

def iniciarApp():

    import tkinter as tk
    from PIL import Image, ImageTk

    janela = tk.Tk()
    janela.title("Minimizador de AFDs")

    titulo = tk.Label(janela, text="Minimizador de AFDs (Algoritmo de Myhil Nerode)", font=("Arial", 16, "bold"))
    titulo.pack(pady=10)

    frameTutorial = tk.Frame(janela)
    frameTutorial.pack(pady=15)

    tutorialLabel = tk.Label(frameTutorial, 
                        text="Você deve selecionar um arquivo .txt que contenha os \ndados de um AFD como mostrado no exemplo ao lado.\nSelecione esse arquivo você irá ver se há como simplifica-lo", 
                        font=("Arial", 13))
    tutorialLabel.pack(padx=10)

    try:
        imgExemplo = Image.open("exemplo.png")
        imgExemploRedimensionada = imgExemplo.resize((600, 300))
        imagemTk = ImageTk.PhotoImage(imgExemploRedimensionada)

        labelImagem = tk.Label(frameTutorial, image=imagemTk)
        labelImagem.pack(pady=20)
    except FileNotFoundError:
        labelAlt = tk.Label(frameTutorial, text="Erro: não foi possivel carregar a imagem do exemplo pois\nela não foi encontrada, verifique se ela não foi apagada por engano", font=("Arial", 13, "bold"))
        labelAlt.pack(pady=20)

    frameBotoes = tk.Frame(janela)
    frameBotoes.pack(pady=20)

    btn1 = tk.Button(frameBotoes,
                    font=("Arial", 14, "bold"),
                    fg="black",
                    bg="LightGoldenrod1",
                    activebackground="yellow4",
                    activeforeground="black",
                    bd=2,
                    relief="raised",
                    cursor="hand2",
                    padx=10, pady=5,
                    text="Selecionar arquivo com AFD",
                    command=selecionarArquivo)
    btn1.pack(side="left", padx=10)

    btn2 = tk.Button(frameBotoes,
                    font=("Arial", 14, "bold"),
                    fg="black",
                    bg="LightGoldenrod1",
                    activebackground="yellow4",
                    activeforeground="black",
                    bd=2,
                    relief="raised",
                    cursor="hand2",
                    padx=10, pady=5,
                    text="Criar arquivo exemplo de AFD",
                    command=criarExemplo)
    btn2.pack(side="left", padx=10)


    janela.mainloop()

def mostrarIteraçãoTabela(Q, matriz, descricao, iteracao):
    import tkinter as tk

    root = tk.Toplevel()
    root.title("Passo "+str(iteracao))

    n = len(Q)

    # Descrição
    frame_descricao = tk.Frame(root, pady=10)
    frame_descricao.pack()
    tk.Label(frame_descricao, text=descricao, font=("Arial", 12, "italic"), fg="blue").pack()

   # Tabela
    if (matriz):
        frame_tabela = tk.Frame(root, padx=10, pady=10)
        frame_tabela.pack()

        for j, estado in enumerate(Q):
            tk.Label(frame_tabela, text=estado, font=("Consolas", 10, "bold")).grid(row=0, column=j+1)
            tk.Label(frame_tabela, text=estado, font=("Consolas", 10, "bold")).grid(row=j+1, column=0)

        for i in range(n):
            for j in range(n):

                if (matriz[i][j] == False):
                    cor = "#f4f4f4"
                elif (matriz[i][j] == None):
                    cor = "#000000"
                else:
                    cor = "#c62828"

                texto = " " if not matriz[i][j] else "✗"
                
                tk.Label(frame_tabela, text=texto, bg=cor, width=4, height=2, relief="ridge").grid(row=i+1, column=j+1)