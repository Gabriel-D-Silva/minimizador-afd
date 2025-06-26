def selecionarArquivo():
    print("Selecionando arquivo...")

def criarExemplo():

    from pathlib import Path
    from tkinter import messagebox

    path = Path.home() / "Desktop"

    exemplo = open(f"{path}\\exemplo.txt", "w")
    exemplo.write("alfabeto:a,b,c,d\nestados:q0,q1,q2\ninicial:q0\nfinais:q1,q2\ntransicoes\nq0,q1,a\nq0,q0,b\nq1,q0,a\nq1,q2,b\nq2,q1,a\nq2,q2,b")
        
    messagebox.showinfo(title="Exemplo .txt criado com sucesso!", message="O exemplo de .txt contendo uma AFD foi criado na sua area de trabalho.")