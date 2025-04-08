# Gerador de Inserts

Este é um aplicativo Python que gera arquivos SQL com comandos `INSERT` a partir de dados de planilhas Excel (XLS, XLSX) ou CSV.

![Captura de tela do Gerador de Inserts](https://github.com/igor-belo/Gerador-de-Inserts/images/projeto_screenshot.png)

## Funcionalidades

-   Geração de scripts SQL `INSERT` a partir de planilhas.
-   Suporte para arquivos Excel (.xls e .xlsx) e CSV (.csv).
-   Opção para usar a primeira linha da planilha como nomes de colunas.
-   Tratamento de aspas simples e espaços em branco nos dados.
-   Interface gráfica intuitiva com Tkinter.
-   Geração de executável único com PyInstaller.
-   Ícone personalizado.

## Como usar

1.  Clique em "Carregar arquivo" e selecione sua planilha (XLS, XLSX ou CSV).
2.  Insira o nome da tabela SQL desejada.
3.  Marque a caixa de seleção se a primeira linha da planilha contiver os nomes das colunas.
4.  Se a primeira linha não contiver os nomes das colunas, insira os nomes das colunas manualmente, separados por vírgulas.
5.  Clique em "Gerar insert" para gerar o arquivo SQL.
6.  Escolha o diretório e o nome do arquivo para salvar o arquivo SQL gerado.

## Requisitos

-   Python 3.6 ou superior
-   Bibliotecas Python (instaladas via `requirements.txt`):
    -   `pandas`
    -   `tkinter`
    -   `ttkthemes`
    -   `Pillow (PIL)`

## Instalação

1.  Clone este repositório:

    ```bash
    git clone [https://github.com/seu-usuario/gerador-de-inserts.git](https://www.google.com/search?q=https://github.com/seu-usuario/gerador-de-inserts.git)
    ```

2.  Navegue até o diretório do projeto:

    ```bash
    cd gerador-de-inserts
    ```

3.  Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4.  Execute o script:

    ```bash
    python insert_generator.py
    ```

## Compilação (PyInstaller)

Para gerar um executável único:

1.  Instale o PyInstaller:

    ```bash
    pip install pyinstaller
    ```

2.  Execute o comando de compilação:

    ```bash
    pyinstaller --onefile --windowed --icon=insert_generator.ico insert_generator.py
    ```

3.  O executável será gerado no diretório `dist`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções de bugs.


## Autor

[Igor Belo]


## Contato

<div align="center">
  <a href="https://www.linkedin.com/in/igor-belo/" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"  target="_blank"></a>
  <a href="https://www.instagram.com/igor_belo.py/" target="_blank"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href = "mailto:igorbello170@gmail.com"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
</div>
