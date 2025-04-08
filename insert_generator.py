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
    try:
        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath, delimiter=';', dtype=str)
        else:
            df = pd.read_excel(filepath, dtype=str)
    except ImportError as e:
        messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}\nCertifique-se de que xlrd esteja instalado para arquivos .xls.")
        return

    entrada_tabela.config(state="normal")
    btn_gerar.config(state="normal")
    chk_primeira_linha.config(state="normal")
    entrada_colunas.config(state="normal")

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
        colunas = [col.strip() for col in df.columns]  # Remove espaços dos nomes das colunas
    else:
        colunas_input = entrada_colunas.get().strip()
        if not colunas_input:
            messagebox.showerror("Erro", "Você deve informar os nomes das colunas.")
            return
        colunas = [col.strip() for col in colunas_input.split(',')]

    df.columns = colunas
    df.fillna('', inplace=True)

    valores = []
    for _, row in df.iterrows():
        # Tratamento das aspas simples e espaços em branco nos dados
        valores.append(f"({', '.join([f'\'{str(x).replace('\'', '').strip()}\'' for x in row])})")

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

    caminho_logo = "C:/Users/Igor/Desktop/gerador de insert/logo.png"
    if os.path.exists(caminho_logo):
        img = Image.open(caminho_logo)
        img = img.resize((64, 64))
        icone = ImageTk.PhotoImage(img)
        janela_instrucoes.iconphoto(False, icone)

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

    label_instrucoes = tk.Label(janela_instrucoes, text=instrucoes_texto, font=("Roboto", 12), bg="#313131", fg="white",
                                justify=tk.LEFT)
    label_instrucoes.pack(padx=20, pady=20, fill="both", expand=True)

root = ThemedTk(theme="equilux")
root.title("Gerador de insert por planilha")
root.geometry("700x600")
root.configure(bg="#313131")

caminho_logo = "C:/Users/Igor/Desktop/gerador de insert/logo.png"
if os.path.exists(caminho_logo):
    img = Image.open(caminho_logo)
    img = img.resize((64, 64))
    icone = ImageTk.PhotoImage(img)
    root.iconphoto(False, icone)

frame = tk.Frame(root, bg="#313131")
frame.pack(expand=True, fill="both")

tk.Label(frame, text="Gerador de insert por planilha", font=("Roboto", 17, "bold"), bg="#313131", fg="white").pack(
    pady=(40, 40))

tk.Button(frame, text="Carregar arquivo", command=carregar_arquivo, font=("Roboto", 14), width=25, relief="flat", bd=2,
          fg="black").pack(pady=15)

tk.Label(frame, text="Nome da Tabela (com schema) exemplo: schema.tabela:", font=("Roboto", 14), bg="#313131", fg="white").pack()
entrada_tabela = tk.Entry(frame, state="disabled", font=("Roboto", 14), width=25, relief="flat", bd=2)
entrada_tabela.pack(pady=15)

var_primeira_linha = tk.BooleanVar()
chk_primeira_linha = tk.Checkbutton(frame, text="Usar primeira linha como nome das colunas",
                                    variable=var_primeira_linha, state="normal", font=("Roboto", 10), bg="#313131",
                                    fg="white", selectcolor="#313131")
chk_primeira_linha.pack(pady=15)

label_numero_colunas = tk.Label(frame, text="", font=("Roboto", 10), bg="#313131", fg="white")
label_numero_colunas.pack(pady=5)

entrada_colunas = tk.Entry(frame, font=("Roboto", 14), width=25, relief="flat", bd=2)
entrada_colunas.pack(pady=15)
entrada_colunas.config(state="normal")

def atualizar_colunas():
    if var_primeira_linha.get():
        entrada_colunas.config(state="disabled")
        label_numero_colunas.config(state="disabled")
    else:
        entrada_colunas.config(state="normal")
        label_numero_colunas.config(state="normal")

chk_primeira_linha.config(command=atualizar_colunas)

btn_gerar = tk.Button(frame, text="Gerar insert", command=gerar_sql, state="disabled", font=("Roboto", 14), width=25,
                      relief="flat", bd=2, fg="black")
btn_gerar.pack(pady=20)

btn_ajuda = tk.Button(frame, text="?", command=mostrar_instrucoes, font=("Roboto", 14), width=2, relief="flat",
                      bg="#313131", fg="#0083c1")
btn_ajuda.place(x=10, y=560)

tk.Label(frame, text="Desenvolvido por igorbelo.sup.shop", font=("Roboto", 12, "italic"), bg="#313131",
         fg="#0083c1").pack(pady=20)

df = None
root.mainloop()