#--- arquivo de configuracao
import os, sys
sys.path.insert(0, os.path.dirname(__file__)+'/static/py')
import pyess
from datetime import timedelta
class Start:
    sysName='ola'
    sysPath=os.path.dirname(__file__)
    database={'file':'storage','encripted':False}
    sysSession={
        "TYPE":"filesystem",
        "FOLDER":"/sessions",
        "MAX":100,
        "PERMANENT":True,
        "LIFETIME": timedelta(hours=5),
        "REQUESTS": 15,
        "TIME_REQUESTS": timedelta(seconds=10)
    }
    ranks = {
        "00":"adm",
        "01":"diretor",
        "02":"gestor",
        "03":"auxiliar",
        "04":"conferente",
        "05":"financeiro",
        "06":"vendedor",
        "07":"caixa",
        "08":"palestrante",
        "09":"usuario",
        "10":"visitante"
    }
    permissions = {
        "inicio":{"rank":["00","01","02","03","04","05","06","07","08","09","10"]},
        "contato":{"rank":["00","01","02","03","04","05","06","07","08","09","10"]},
        "entrar":{"rank":["10"]},
        "adicionar_usuario":{"rank":["00","01","02","03"]},
        "cadastro":{"rank":["10"]},
        "perfil":{"rank":["00","01","02","03","04","05","06","07","08","09"]},
        "palestra":{"rank":["00","01","02","03","04","05","06","07","08","09"],
            "cadastrar":{"rank":["00","01","02","03","04","05","06","07","08"]}
        },
        "sair":{"rank":["00","01","02","03","04","05","06","07","08","09"]}
    }
    navigation = [
        {"title": "Inicio", "link": "/inicio","icon":"ph:house-line","rank":permissions["inicio"]["rank"]},
        {"title": "Contato", "link": "/contato","icon":"ph:house-line","rank":permissions["contato"]["rank"]},
        {"title": "Entrar", "link": "/entrar","icon":"ph:arrow-square-up-right-line","rank":permissions["entrar"]["rank"]},
        {"title": "Cadastro", "link": "/cadastro","icon":"ph:arrow-square-up-right-line","rank":permissions["cadastro"]["rank"]},
        {"title": "Perfil", "link": "/perfil","icon":"ph:user","rank":permissions["perfil"]["rank"]},
        {"title": "Sair", "link": "/sair","icon":"ph:user","rank":permissions["sair"]["rank"]}
    ]
    tipo_palestras = [
        "Online", "Presencial", "Hibrido"
    ]
    duracao_palestras = [
        5,30,60,90,120,150,180,210,240
    ]
    progresso_palestra = 0.75 # e valor em porcetagem do progresso da palestra
    def __init__(self):
        self.requests,self.sessions={},[]
    def allow_request(self, sid):
        if not sid in self.requests: self.requests[sid] = {'requests':0,'time':pyess.time()}
        if pyess.time('obj', self.requests[sid]['time'])+self.sysSession['TIME_REQUESTS'] <= pyess.time('obj'):
            self.requests[sid]['requests'] = 0
            self.requests[sid]['time'] = pyess.time()
        else:
            if self.requests[sid]['requests'] <= self.sysSession['REQUESTS']: self.requests[sid]['requests'] += 1
            else: return(False)
        return(True)
    def getSid(self):
        sid=pyess.getKey(8,self.sessions)
        self.sessions.append(sid)
        return(sid)