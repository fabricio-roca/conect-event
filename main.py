#--- arquivo principal
import sys,os,json,conf
sys.path.insert(0, os.path.dirname(__file__)+'/static/py')
import pyjson,pyess

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
        self.refresh(self.sessions[sid])
        return(self)

    def security(self,sid,urlPath):
        if not sid in self.sessions or urlPath[0] == 'sair':
            self.sessions[sid] = {"user":{"ativo":None, "rank":"10", "email":"visitante", "nome":"visitante"}}
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

    def refresh(self,session):
        if self.page == "inicio":
            self.usuarios = self.storage.get("usuarios")

    def listener(self,content):
        try:
            if self.conf.allow_request(content['sid']):
                result,description=self.run(content["method"][0], content["method"][1], content,self.sessions[content["sid"]])
            else:result, description = False, "limite de requisicoes atingido! tente novamente mais tarde"
        except:result, description = False, "erro no servidor, contato o suporte!"
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
                if session["user"]["rank"] in self.conf.permissions["palestra"]["rank"]:
                    palestras = self.storage.get("palestras")
                nova_palestra = {
                    "titulo": data["titulo"],
                    "descricao": data["descricao"],
                    "data": data["data"],
                    "duracao": data["duracao"],
                    "id": len(palestras),
                    "ativo": True
                }
                self.sessions[data["sid"]]["user"] = nova_palestra
                self.storage.append("palestras", nova_palestra)
            elif comm == "teste":
                print(data)
            else: return(False,"Comando Desconhecido")
        else: return(False,"acao desconhecida")
        return(True,"Success!")