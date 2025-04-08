import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import os
from ttkthemes import ThemedTk
from PIL import Image, ImageTk


def carregar_arquivo():
    filepath = filedialog.askopenfilename(filetypes=[("Planilhas", "*.xls;*.xlsx;*.csv")])
    if not filepath:
        return
    
    global df
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath, delimiter=';', dtype=str)  # Lendo como string para evitar problemas
    else:
        df = pd.read_excel(filepath, dtype=str)
    
    entrada_tabela.config(state="normal")
    btn_gerar.config(state="normal")
    chk_primeira_linha.config(state="normal")
    
    # Habilitar o campo de colunas desde a carga do arquivo
    entrada_colunas.config(state="normal")
    
    # Atualizar o número de colunas no texto acima do campo de entrada de colunas
    num_colunas = len(df.columns)
    label_numero_colunas.config(text=f"Foram identificadas {num_colunas} colunas. Digite o nome delas separando por vírgula:")


def gerar_sql():
    if df is None:
        messagebox.showerror("Erro", "Nenhum arquivo foi carregado.")
        return
    
    nome_tabela = entrada_tabela.get().strip()
    if not nome_tabela:
        messagebox.showerror("Erro", "Nome da tabela não pode estar vazio.")
        return
    
    usar_primeira_linha = var_primeira_linha.get()
    
    colunas = []
    if usar_primeira_linha:
        colunas = list(df.columns)
    else:
        colunas_input = entrada_colunas.get().strip()
        if not colunas_input:
            messagebox.showerror("Erro", "Você deve informar os nomes das colunas.")
            return
        colunas = [col.strip() for col in colunas_input.split(',')]
    
    df.columns = colunas
    
    # Substituir NaN por string vazia
    df.fillna('', inplace=True)

    valores = []
    for _, row in df.iterrows():
        valores.append(f"({', '.join([f'\'{str(x)}\'' for x in row])})")  # Colocando todos os valores entre aspas simples
    
    sql_insert = f"INSERT INTO {nome_tabela} ({', '.join(colunas)}) \nVALUES \n    " + ",\n    ".join(valores) + ";"
    
    diretorio = filedialog.askdirectory()
    if not diretorio:
        messagebox.showerror("Erro", "Nenhum diretório selecionado.")
        return
    
    nome_arquivo = simpledialog.askstring("Nome do Arquivo", "Digite o nome do arquivo SQL (sem a extensão):")
    if not nome_arquivo:
        messagebox.showerror("Erro", "O nome do arquivo não pode ser vazio.")
        return
    
    caminho_sql = os.path.join(diretorio, f"{nome_arquivo}.sql")
    with open(caminho_sql, "w", encoding="utf-8") as f:
        f.write(sql_insert)
    
    messagebox.showinfo("Sucesso", f"Arquivo SQL salvo em: {caminho_sql}")


def mostrar_instrucoes():
    janela_instrucoes = tk.Toplevel()
    janela_instrucoes.title("Instruções")
    janela_instrucoes.geometry("800x400")
    janela_instrucoes.configure(bg="#313131")
    
    # Definir ícone personalizado na janela de instruções
    caminho_logo = "C:/Users/Igor/Desktop/gerador de insert/logo.png"
    if os.path.exists(caminho_logo):
        img = Image.open(caminho_logo)
        img = img.resize((64, 64))  # Ajusta o tamanho do ícone
        icone = ImageTk.PhotoImage(img)
        janela_instrucoes.iconphoto(False, icone)

    # Texto explicativo dentro da janela de instruções
    instrucoes_texto = (
        "Esta aplicação gera um arquivo SQL com um INSERT a partir de dados de um arquivo CSV, XLS ou XLSX.\n\n"
        "Passo a passo:\n"
        "1. Clique em 'Carregar Planilha' e selecione o arquivo.\n"
        "2. Preencha o nome da tabela desejada.\n"
        "3. Selecione se a primeira linha contém os nomes das colunas.\n"
        "4. Clique em 'Gerar SQL' para gerar o arquivo SQL.\n"
        "5. Escolha o diretório e nome do arquivo para salvar o SQL gerado.\n\n"
        "O SQL gerado conterá um comando INSERT com os dados da planilha."
    )
    
    label_instrucoes = tk.Label(janela_instrucoes, text=instrucoes_texto, font=("Roboto", 12), bg="#313131", fg="white", justify=tk.LEFT)
    label_instrucoes.pack(padx=20, pady=20, fill="both", expand=True)


# Criando interface com tema Equilux
root = ThemedTk(theme="equilux")
root.title("Gerador de insert por planilha")
root.geometry("700x600")  # Aumentando o tamanho da janela
root.configure(bg="#313131")  # Cor de fundo mais escura

# Definir ícone personalizado
caminho_logo = "C:/Users/Igor/Desktop/gerador de insert/logo.png"
if os.path.exists(caminho_logo):
    img = Image.open(caminho_logo)
    img = img.resize((64, 64))  # Ajusta o tamanho do ícone
    icone = ImageTk.PhotoImage(img)
    root.iconphoto(False, icone)

# Centralizando os componentes
frame = tk.Frame(root, bg="#313131")
frame.pack(expand=True, fill="both")

# Ajustado o pady para aumentar o espaço entre o topo e o primeiro elemento
tk.Label(frame, text="Gerador de insert por planilha", font=("Roboto", 17, "bold"), bg="#313131", fg="white").pack(pady=(40, 40))  # Aumentando o padding superior

tk.Button(frame, text="Carregar arquivo", command=carregar_arquivo, font=("Roboto", 14), width=25, relief="flat", bd=2, fg="black").pack(pady=15)

tk.Label(frame, text="Nome da Tabela:", font=("Roboto", 14), bg="#313131", fg="white").pack()
entrada_tabela = tk.Entry(frame, state="disabled", font=("Roboto", 14), width=25, relief="flat", bd=2)
entrada_tabela.pack(pady=15)

var_primeira_linha = tk.BooleanVar()
chk_primeira_linha = tk.Checkbutton(frame, text="Usar primeira linha como nome das colunas", variable=var_primeira_linha, state="normal", font=("Roboto", 10), bg="#313131", fg="white", selectcolor="#313131")
chk_primeira_linha.pack(pady=15)

# Adicionando o rótulo para mostrar o número de colunas
label_numero_colunas = tk.Label(frame, text="", font=("Roboto", 10), bg="#313131", fg="white")
label_numero_colunas.pack(pady=5)

entrada_colunas = tk.Entry(frame, font=("Roboto", 14), width=25, relief="flat", bd=2)
entrada_colunas.pack(pady=15)
entrada_colunas.config(state="normal") 

# Habilitar/desabilitar campo de entrada de colunas
def atualizar_colunas():
    if var_primeira_linha.get():
        entrada_colunas.config(state="disabled")
        label_numero_colunas.config(state="disabled")
    else:
        entrada_colunas.config(state="normal")
        label_numero_colunas.config(state="normal")

chk_primeira_linha.config(command=atualizar_colunas)

btn_gerar = tk.Button(frame, text="Gerar insert", command=gerar_sql, state="disabled", font=("Roboto", 14), width=25, relief="flat", bd=2, fg="black")
btn_gerar.pack(pady=20)

# Botão de ajuda
btn_ajuda = tk.Button(frame, text="?", command=mostrar_instrucoes, font=("Roboto", 14), width=2, relief="flat", bg="#313131", fg="#0083c1")
btn_ajuda.place(x=10, y=560)  # Coloca o botão no canto inferior esquerdo

tk.Label(frame, text="Desenvolvido por igorbelo.sup.shop", font=("Roboto", 12, "italic"), bg="#313131", fg="#0083c1").pack(pady=20)

df = None
root.mainloop()
