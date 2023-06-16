import json, os

class Storage:
	def __init__(self, file='storage', login='root', senha='', encripted=True):
		self.encripted = encripted
		self.file = file
		if not '.json' in self.file: self.file = self.file+'.json'
		if self.encripted: 
			try: 
				import pycript
				self.security = pycript.Security(4.62)
			except: 
				self.encripted = False
				print('*** ALERTA *** Biblioteca de criptografia não encontrada!')
		self.connected = self.connect(self.file, login, senha)

	def connect(self, file='', login='root', senha=''):
		self.file = file
		if not '.json' in self.file: self.file = self.file+'.json'
		if self.file == '': return(False)
		elif os.path.exists(self.file):
			with open(self.file) as file: data = json.load(file)
			if self.encripted: 
				if 'credencials' in data: self.encripted = False
				else: data = self.decript(data)
			if not 'credencials' in data:
				print('*** ALERTA *** Banco de dados corrompido ou criptografado! Solução: Apague o arquivo "'+self.file+'" e reinicie. OBS.: Todos os dados serão perdidos.')
				return(False)
			if data['credencials']['login'] == login and data['credencials']['senha'] == senha: return(True)
			else: return(False)
		else:
			data = {'credencials':{'login':login,'senha':senha}}
			if self.encripted: data = self.encript(data)
			with open(self.file, 'w') as file: json.dump(data, file, indent=2, sort_keys=True)
			return(True)

	def encript(self, var):
		if type(var) == type([1]):
			list = []
			for item in var: list.append(self.encript(item))
			return(list)
		elif type(var) == type({'a':'a'}):
			dict = {}
			for key in var.keys(): dict[self.security.encript(str(key))] = self.encript(var[key])
			return(dict)
		elif type(var) == type(True): return(self.security.encript(str(var)))
		else: return(self.security.encript(str(var)))

	def decript(self, var):
		if type(var) == type([1]):
			list = []
			for item in var: list.append(self.decript(item))
			return(list)
		elif type(var) == type({'a':'a'}):
			dict = {}
			for key in var.keys(): dict[self.security.decript(str(key))] = self.decript(var[key])
			return(dict)
		else: 
			result = self.security.decript(var)
			if result in ['True', 'False']: return(result=='True')
			else: 
				try: return(int(result))
				except: 
					try: return(float(result))
					except: return(result)

	def save(self, id, var):
		if self.connected:
			try:
				data = self.load()
				data[id] = var
				if self.encripted: data = self.encript(data)
				with open(self.file, 'w') as file: json.dump(data, file, indent=2, sort_keys=True)
				return(True)
			except: return(False)
		else: return('Não conectado.')

	def load(self, id=None):
		if self.connected:
			with open(self.file) as file: data = json.load(file)
			if self.encripted: data = self.decript(data)
			if id != None:
				if id in data: return(data[id])
				else: return(None)
			else: return(data)
		else: return('Não conectado.')
		
	def delete(self, id):
		if self.connected:
			try:
				data = self.load()
				if id in data:
					del data[id]
					if self.encripted: data = self.encript(data)
					with open(self.file, 'w') as file: json.dump(data, file, indent=2, sort_keys=True)
					return(True)
			except: return(False)
		else: return('Não conectado.')

	def get(self, id):
		result = self.load(id)
		if result == None:
			self.save(id, [])
			result = []
		return(result)

	def append(self, id, var):
		try:
			result = self.get(id)
			if type(result) != type([]): return(False, 'Esse item não é uma lista!')
			else:
				result.append(var)
				self.save(id, result)
			return(True)
		except: return(False)

	def help(self, command=''):
		commands = {
			'connect':"""\n*** connect(arquivo, login, senha) ***
Abre e prepara o arquivo para manuseio de dados
Retorna TRUE em caso de sucesso ou FALSE em caso de falha\n""",
			'save':"""\n*** save(id, variavel) ***
Salva uma variável usando ID como identificação
Retorna TRUE em caso de sucesso ou FALSE em caso de falha\n""",
			'load':"""\n*** load(id) ***
Carrega uma variável usando o ID de identificação
Retorna a variável em caso de sucesso ou NONE caso o ID não exista\n""",
			'delete':"""\n*** delete(id) ***
Apaga uma variável usando o ID de identificação
Retorna TRUE em caso de sucesso ou FALSE em caso de falha\n""",
			'get':"""\n*** get(id) ***
Carrega uma variável usando o ID de identificação, caso não exista, a função cria uma lista
Retorna a variável ou uma lista vazia\n""",
			'append':"""\n*** append(id, variavel) ***
Adiciona uma variável ao final de uma lista usando o ID de identificação, caso não exista, a função cria a lista e adiciona
Retorna TRUE em caso de sucesso ou FALSE em caso de falha\n""",
		}
		help = """Comandos:
1 - connect(arquivo, login, senha)
2 - save(id, variavel)
3 - load(id)
4 - delete(id)
5 - get(id)
6 - append(id, variavel)
7 - help(comando)\n
(use help(comando) para detalhes mais específicos)\n"""
		if command in commands: print(commands[command])
		else: print(help)

if __name__ == '__main__':
	db = Storage()
	db.save('test', 'oi')
	print(db.load())