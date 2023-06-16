#--- arquivo principal
import sys,os,json,conf
sys.path.insert(0, os.path.dirname(__file__)+'/static/py')
import pyjson,pyess
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

class Data:
    conf = conf.Start()
    def __init__(self):
        self.storage=pyjson.Storage(self.conf.database["file"],self.conf.database["encripted"])
        self.ess=pyess.Instance()
        self.sessions={}

    def conect(self,sid,urlPath):
        self.urlPath=self.security(sid,urlPath)
        self.sid=sid
        self.page=self.urlPath[0]
        self.detail=self.urlPath[1]
        self.description=self.urlPath[2]
        self.information=self.urlPath[3]
        self.title=self.page.capitalize()
        self.refresh(self.sessions[sid],sid)
        return(self)

    def security(self,sid,urlPath):
        if not sid in self.sessions or urlPath[0] == 'sair':
            self.sessions[sid] = {"user":{"ativo":None, "rank":"10", "email":"visitante", "nome":"visitante", "id":"-1"}}
            if urlPath[0] == 'sair': urlPath=["entrar","","",""]
        url = "/" + urlPath[0]
        url += "/" + urlPath[1] if urlPath[1] != "" else ""
        url += "/" + urlPath[2] if urlPath[2] != "" else ""
        url += "/" + urlPath[3] if urlPath[3] != "" else ""
        session = self.sessions[sid]
        for menu in self.conf.navigation:
            if not session["user"]["rank"] in menu["rank"] and url==menu["link"]:
                if session["user"]["rank"] == "10":urlPath=["entrar","","",""]
                else:urlPath=["inicio","","",""]
        self.url = "/" + urlPath[0]
        self.url += "/" + urlPath[1] if urlPath[1] != "" else ""
        self.url += "/" + urlPath[2] if urlPath[2] != "" else ""
        self.url += "/" + urlPath[3] if urlPath[3] != "" else ""
        return(urlPath)

    def refresh(self,session,sid):
        self.usuarios = self.storage.get("usuarios")
        for usuario in self.usuarios:
            if usuario["id"] == session["user"]["id"]:
                self.sessions[sid]["user"] = usuario
        if self.page == "inicio":
            self.palestras = self.storage.get("palestras")
            self.usuarios = self.storage.get("usuarios")
        elif self.page == "perfil":
            self.usuarios = self.storage.get("usuarios")
            self.palestras = self.storage.get("palestras")
            self.sessions[sid]["assistidos"] = []
            for assistido in session["user"]["assistido"]:
                self.sessions[sid]["assistidos"].append(assistido)
        elif self.page == "palestra":
            self.palestras = self.storage.get("palestras")
            if self.detail != "":
                self.error = "Palestra nao encontrada!"
                for palestra in self.palestras:
                    if palestra["unicode"] == self.detail: self.error = ""
        elif self.page == "sala":
            self.palestras = self.storage.get("palestras")
            if self.detail != "":
                self.error = "Palestra nao encontrada!"
                for palestra in self.palestras:
                    if palestra["unicode"] == self.detail:
                        self.error = ""
                        self.palestra = palestra
        elif self.page == "contato":
            self.menssagem = self.storage.get("menssagem")

    def listener(self,content):
        #try:
        if self.conf.allow_request(content['sid']):
            result,description=self.run(content["method"][0], content["method"][1], content,self.sessions[content["sid"]])
        else:result, description = False, "limite de requisicoes atingido! tente novamente mais tarde"
        #except:result, description = False, "erro no servidor, contato o suporte!"
        return json.dumps({'success':result,'description':description}), 200, {'ContentType':'application/json'}

    def run(self,action,comm,data,session):
        if action == "add":
            if comm == "user":
                if session["user"]["rank"] in self.conf.permissions["entrar"]["rank"]:
                    usuarios=self.storage.get("usuarios")
                    for usuario in usuarios:
                        if usuario["email"]==data["email"]:return(False, "Este email esta sendo usuarios")
                    self.sessions[data["sid"]]["user"]={
                        "nome":data["nome"],
                        "email":data["email"],
                        "senha":data["senha"],
                        "rank":"09",
                        "palestras":[],
                        "assistido":[],
                        "id":len(usuarios),
                        "ativo":True
                    }
                    self.storage.append("usuarios",self.sessions[data["sid"]]["user"])
                else: return(False, "Voce nao tem permissao para isso.")
            elif comm == "login":
                usuarios=self.storage.get("usuarios")
                for usuario in usuarios:
                    if usuario["email"]==data["email"] and usuario["senha"]==data["senha"]:
                        self.sessions[data["sid"]]["user"]=usuario
                        return(True, "success")
                return(False, "Email ou Senha incorreto.")
            elif comm == "palestra":
                palestras = self.storage.get("palestras")
                for palestra in palestras:
                    if palestra["titulo"]==data["titulo"]:return(False, "Este titulo esta sendo usado")
                self.storage.append("palestras", {
                        "titulo": data["titulo"],
                        "tipo": data["tipo"],
                        "descricao": data["descricao"],
                        "data": data["data"].replace("T"," ")+":00",
                        "duracao": data["duracao"],
                        "link": data["link"],
                        'unicode':self.get_unicode(),
                        'palestrante':session["user"]["id"],
                        'participantes':[],
                        "ativo": True
                    })
            elif comm == "participante":
                usuarios = self.storage.get("usuarios")
                palestras = self.storage.get("palestras")
                for palestra in palestras:
                    if palestra["unicode"] == data["unicode"]:
                        for usuario in usuarios:
                            if usuario['id'] == session["user"]["id"]:
                                usuario["palestras"].append(palestra["unicode"])
                                palestra["participantes"].append(usuario["id"])
                self.storage.save("usuarios",usuarios)
                self.storage.save("palestras",palestras)
            elif comm == "menssagem":
                menssagem == self.storage.get("menssagem")
                self.storage.append("menssagem", {
                        'unicode':self.get_unicode(),
                        "nome": data["nome"],
                        "email": data["email"],
                        "menssagem": data["menssagem"],
                        "ativo": True
                    })
            elif comm == "watch_in":
                users=self.storage.get("usuarios")
                lectures = self.storage.get("palestras")
                for user in users:
                    if user["id"] == session["user"]["id"]:
                        for lecture in lectures:
                            if lecture["unicode"] == data["palestra"]:
                                if pyess.time("timestamp",lecture["data"]) > pyess.time("timestamp"):
                                    watching = False
                                    for watched in user["assistido"]:
                                        if watched["unicode"] == data['palestra']:
                                            watching = True
                                    if not watching:
                                        user["assistido"].append({
                                            "unicode":data["palestra"],
                                            "entrada":lecture["data"],
                                            "saida":"",
                                            "certificado": False
                                        })
                                else:
                                    watching = False
                                    for watched in user["assistido"]:
                                        if watched["unicode"] == data['palestra']:
                                            watching = True
                                    if not watching:
                                        user["assistido"].append({
                                            "unicode":data["palestra"],
                                            "entrada":pyess.time(),
                                            "saida":"",
                                            "certificado": False
                                        })
                self.storage.save("usuarios",users)
            elif comm == "watching":
                users=self.storage.get("usuarios")
                for user in users:
                    if user["id"] == session["user"]["id"]:
                        for watched in user["assistido"]:
                            if watched["unicode"] == data["palestra"]:
                                if not watched["certificado"]:
                                    watched["saida"] = pyess.time()
                                    lectures = self.storage.get("palestras")
                                    for lecture in lectures:
                                        if lecture["unicode"] == watched["unicode"]:
                                            assistido = pyess.dateDif([watched["saida"],watched["entrada"]],"minute")
                                            if assistido >= (float(lecture["duracao"])*self.conf.progresso_palestra):
                                                watched["certificado"] = True
                                                self.gerar_certificado(user, lecture)
                self.storage.save("usuarios",users)

            elif comm == "teste":
                print(data)
            else: return(False,"Comando Desconhecido")
        else: return(False,"acao desconhecida")
        return(True,"Success!")

    def get_unicode(self):
        unicode = pyess.getKey(8, self.storage.get('unicodes'))
        self.storage.append('unicodes', unicode)
        return(unicode)

    def quebrar_texto(self,pdf, texto, largura_max):
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
    def gerar_certificado(self,aluno,palestra):
        usuarios = self.storage.get("usuarios")
        for usuario in usuarios:
            if usuario["id"] == palestra["palestrante"]:
                palestrante = usuario
    # Cria um novo arquivo PDF
        pdf = canvas.Canvas(os.path.dirname(__file__)+'/static/certificados/'+palestra["titulo"]+'_'+aluno["nome"]+str(aluno["id"])+'.pdf', pagesize=landscape(letter))
    # Define o conteúdo do certificado
        # Lista de caminhos das assinaturas disponíveis
        assinaturas = [
            "static/img/imagem1.jpg",
            "static/img/imagem2.jpg",
            "static/img/imagem3.jpg",
            "static/img/imagem4.jpg",
            "static/img/imagem5.jpg"
        ]
    # Define o conteúdo do certificado
        texto_titulo = "Certificado"
        texto_nome = aluno["nome"]
        texto_certificado = f"""
        Concluiu com sucesso a {palestra['titulo']}
        em { pyess.dateFormat(pyess.time(), '%d/%m/%Y') }, com carga horária de {palestra['duracao']} minutos, com o Palestrante {palestrante['nome']}.
        """
        logo = "static/img/Logotipo_certificado.jpg"  # Substitua pelo caminho correto da sua imagem
        selo = "static/img/selo.jpg"  # Substitua pelo caminho correto da sua imagem
        lado_a = "static/img/lado_a.jpg"
        lado_b = "static/img/lado_b.jpg"
        assinatura = random.choice(assinaturas)
        largura_max = 600
        linhas = self.quebrar_texto(pdf, texto_certificado, largura_max)

    # Adiciona a imagem ao PDF
        pdf.drawImage(logo, 300, 420, width=2.50*inch, height=2.50*inch)
        pdf.drawImage(selo, 550, 100, width=1*inch, height=1.50*inch)
        pdf.drawImage(assinatura, 300, 30, width=3*inch, height=4*inch)
        pdf.drawImage(lado_a, -20, -20, width=4*inch, height=3*inch)
        pdf.drawImage(lado_b, 520, 440, width=4*inch, height=3*inch)

        y = 400
        pdf.setFont("Helvetica", 14)  # Define a fonte e o tamanho
        for linha in linhas:
            pdf.drawString(100, y, linha)
            y -= 20
        # Adiciona o texto ao PDF
        pdf.setFont("Helvetica-Bold", 18)  # Define a fonte e o tamanho
        pdf.drawString(100, 450, texto_nome)
        pdf.setFont("Helvetica-Bold", 30)  # Define a fonte e o tamanho
        pdf.drawString(100, 500, texto_titulo)

        # Fecha o arquivo PDF
        pdf.save()
