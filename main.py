import tkinter as tk #deixa eu criar janela botao e dialogo
from tkinter import filedialog
import os #operações do sistema!
import shutil #copia arquivo


def processar_foto():
    """Seleciona e copia a foto do usuário."""
    root = tk.Tk()
    root.withdraw()
    foto_original = filedialog.askopenfilename(
        title="Selecione sua foto", 
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
    )
    
    if foto_original:
        foto_nome = "foto_curriculo" + os.path.splitext(foto_original)[1]
        shutil.copy(foto_original, foto_nome)
        return foto_nome
    return ""


def coletar_informacoes():
    """Coleta todas as informações do usuário e salva em arquivos separados."""
    print("=== GERADOR DE CURRÍCULO ===")
    
    # Coleta nome
    nome = input("Digite seu nome completo: ")
    with open("nome.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{nome}\n")
    
    # Coleta email
    email = input("Digite seu email: ")
    with open("email.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{email}\n")
    
    # Coleta telefone
    telefone = input("Digite seu telefone: ")
    with open("telefone.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{telefone}\n")
    
    # Coleta cargo
    cargo = input("Digite seu cargo desejado: ")
    with open("cargo.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{cargo}\n")
    
    # Coleta endereço
    endereco = input("Digite seu endereço: ")
    with open("endereco.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{endereco}\n")
    
    # Coleta objetivo
    objetivo = input("Digite seu objetivo profissional: ")
    with open("objetivo.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{objetivo}\n")
    
    # Coleta escolaridade usando WHILE
    escolaridades = []
    print("\nDigite sua escolaridade (deixe vazio para finalizar):")
    with open("escolaridade.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write("--- Nova execução ---\n")
        while True:
            escolaridade = input("Escolaridade (ex: Ensino Médio, Graduação, etc.): ")
            if escolaridade == "":
                break
            escolaridades.append(escolaridade)
            arquivo.write(f"{escolaridade}\n")
    
    # Coleta idiomas usando WHILE
    idiomas = []
    print("\nDigite os idiomas que você fala (deixe vazio para finalizar):")
    with open("idiomas.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write("--- Nova execução ---\n")
        while True:
            idioma = input("Idioma e nível (ex: Inglês - Intermediário): ")
            if idioma == "":
                break
            idiomas.append(idioma)
            arquivo.write(f"{idioma}\n")
    
    # Seleciona e processa foto
    foto_nome = processar_foto()
    if foto_nome:
        with open("foto.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{foto_nome}\n")
    
    # Coleta habilidades usando WHILE
    habilidades = []
    print("\nDigite suas habilidades (deixe vazio para finalizar):")
    
    with open("habilidades.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write("--- Nova execução ---\n")
        while True:
            habilidade = input("Habilidade: ")
            if habilidade == "":
                break
            habilidades.append(habilidade)
            arquivo.write(f"{habilidade}\n")
    
    return {
        "nome": nome,
        "email": email, 
        "telefone": telefone,
        "cargo": cargo,
        "endereco": endereco,
        "objetivo": objetivo,
        "escolaridades": escolaridades,
        "idiomas": idiomas,
        "foto": foto_nome,
        "habilidades": habilidades
    }

# Função 3: Gera lista HTML das habilidades
def gerar_habilidades_html(lista_habilidades):
    """Converte lista de habilidades em HTML usando WHILE."""
    html = ""
    i = 0
    while i < len(lista_habilidades):
        html += f"        <li>{lista_habilidades[i]}</li>\n"
        i += 1
    return html

# Função 4: Gera lista HTML das escolaridades
def gerar_escolaridade_html(lista_escolaridades):
    """Converte lista de escolaridades em HTML usando WHILE."""
    html = ""
    i = 0
    while i < len(lista_escolaridades):
        html += f"        <li>{lista_escolaridades[i]}</li>\n"
        i += 1
    return html

# Função 5: Gera lista HTML dos idiomas
def gerar_idiomas_html(lista_idiomas):
    """Converte lista de idiomas em HTML usando WHILE."""
    html = ""
    i = 0
    while i < len(lista_idiomas):
        html += f"        <li>{lista_idiomas[i]}</li>\n"
        i += 1
    return html

# ...existing code...

# Função 6: Cria o arquivo HTML do currículo
def criar_curriculo_html(dados):
    """Gera o arquivo HTML do currículo."""
    habilidades_html = gerar_habilidades_html(dados['habilidades'])
    escolaridade_html = gerar_escolaridade_html(dados['escolaridades'])
    idiomas_html = gerar_idiomas_html(dados['idiomas'])
    
    html_curriculo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currículo - {dados['nome']}</title>
    <style>
        body {{
            font-family: Verdana;
            background-color: #f2f2f2;
        }}
        
        .caixa {{
            background: white;
            width: 700px;
            margin: 30px auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px gray;
        }}
        
        h1 {{
            color: #2a4d69;
        }}
        
        h2 {{
            color: #4b86b4;
            border-bottom: 1px solid #ccc;
        }}
        
        .foto {{
            border-radius: 50%;
            float: right;
            margin-left: 24px;
            margin-bottom: 10px;
            margin-top: 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.10);
            width: 120px;
            height: 120px;
            object-fit: cover;
        }}
        
        .contato {{
            margin-bottom: 20px;
        }}
        
        ul {{
            list-style-type: disc;
            margin-left: 20px;
        }}
        
        li {{
            margin-bottom: 5px;
        }}
    </style>
</head>
<body>
    <div class="caixa">
        <img src="{dados['foto']}" alt="Foto" class="foto">
        <h1>{dados['nome']}</h1>
        <p><strong>Cargo:</strong> {dados['cargo']}</p>
        
        <div class="contato">
            <p><strong>Email:</strong> {dados['email']}</p>
            <p><strong>Telefone:</strong> {dados['telefone']}</p>
            <p><strong>Endereço:</strong> {dados['endereco']}</p>
        </div>
        
        <h2>Objetivo</h2>
        <p>{dados['objetivo']}</p>
        
        <h2>Escolaridade</h2>
        <ul>
{escolaridade_html}        </ul>
        
        <h2>Habilidades</h2>
        <ul>
{habilidades_html}        </ul>
        
        <h2>Idiomas</h2>
        <ul>
{idiomas_html}        </ul>
    </div>
</body>
</html>"""


    with open("curriculo.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(html_curriculo)
    print("\n✅ Currículo gerado com sucesso!")
    print("📄 Arquivo: curriculo.html")
    print("📝 Dados salvos em arquivos separados:")
   



# PROGRAMA PRINCIPAL (máximo 10 linhas)
print("Iniciando gerador de currículo...")
dados_usuario = coletar_informacoes()
criar_curriculo_html(dados_usuario)
print("Processo concluído!")
