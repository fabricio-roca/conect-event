from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import random

def quebrar_texto(pdf, texto, largura_max):
    palavras = texto.split()
    linhas = []
    linha_atual = ''

    for palavra in palavras:
        if pdf.stringWidth(linha_atual + palavra, "Helvetica", 14) <= largura_max:
            linha_atual += palavra + ' '
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra + ' '

    if linha_atual:
        linhas.append(linha_atual.strip())

    return linhas

def gerar_certificado(nome):
    # Cria um novo arquivo PDF
    pdf = canvas.Canvas('certificado.pdf', pagesize=landscape(letter))

    # Define o conteúdo do certificado
        # Lista de caminhos das imagens disponíveis
    assinaturas = [
        "static/img/imagem1.jpg",
        "static/img/imagem2.jpg",
        "static/img/imagem3.jpg",
        "static/img/imagem4.jpg",
        "static/img/imagem5.jpg"
    ]

    # Escolher aleatoriamente uma imagem da lista

    texto_titulo = "Certificado"
    texto_nome = nome
    texto_certificado = """
    Concluiu com sucesso a trilha Conectar do Discover
    em 14.06.2023, com carga horária de 2h23. O
    currículo de aprendizado inclui: fundamentos da
    programação, funcionamento de computadores,
    internet e mais.
    """
    logo = "static/img/Logotipo_certificado.jpg"  # Substitua pelo caminho correto da sua imagem
    selo = "static/img/selo.jpg"  # Substitua pelo caminho correto da sua imagem
    lado_a = "static/img/lado_a.jpg"
    lado_b = "static/img/lado_b.jpg"
    assinatura = random.choice(assinaturas)
    largura_max = 600
    linhas = quebrar_texto(pdf, texto_certificado, largura_max)

    # Adiciona a imagem ao PDF
    pdf.drawImage(logo, 300, 420, width=2.50*inch, height=2.50*inch)
    pdf.drawImage(selo, 550, 100, width=1*inch, height=1.50*inch)
    pdf.drawImage(assinatura, 300, 30, width=3*inch, height=4*inch)
    pdf.drawImage(lado_a, -20, -20, width=4*inch, height=3*inch)
    pdf.drawImage(lado_b, 520, 440, width=4*inch, height=3*inch)

    # Adiciona o texto ao PDF
    pdf.setFont("Helvetica-Bold", 30)  # Define a fonte e o tamanho
    pdf.setFillColor(colors.black)
    pdf.drawString(100, 400, texto_titulo)
    pdf.setFont("Helvetica-Bold", 18)  # Define a fonte e o tamanho
    pdf.drawString(100, 350, texto_nome)
    pdf.setFont("Helvetica", 14)  # Define a fonte e o tamanho
    y = 300
    for linha in linhas:
        pdf.drawString(100, y, linha)
        y -= 20

    # Fecha o arquivo PDF
    pdf.save()

# Exemplo de chamada da função para gerar o certificado
gerar_certificado("João da Silva")