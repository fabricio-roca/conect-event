import random, os
from datetime import datetime as dt, timedelta as td

def time(type='str', date=None):
  if date == None:
    if type == 'str': return(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
    elif type == 'timestamp': return(dt.timestamp(dt.now()))
    elif type == 'obj': return(dt.now())
  else:
    if 'T' in date: date = date.replace('T', ' ')+':00'
    if type == 'str': 
      try: return(date.strftime("%Y-%m-%d %H:%M:%S"))
      except: return(dt.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S"))
    elif type == 'timestamp': return(dt.timestamp(time('obj', date)))
    elif type == 'obj': return(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))

def dateFormat(date, format):
  obj = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
  return(obj.strftime(format))

def exists(self, file):
  result = os.path.exists(self.sysPath+'/'+file)
  if not result: result = os.path.exists(file)
  return(result)

def saudation():
  hour = int(dt.now().strftime("%H"))
  if hour < 1: return('Boa noite')
  elif hour < 12: return('Bom dia')
  elif hour < 19: return('Boa tarde')
  else: return('Boa noite')

def getKey(characters=8, list=[]):
  alfa = [
		'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
		'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
		'0','1','2','3','4','5','6','7','8','9']
  while True:
    key = ''
    for i in range(characters): key += random.choice(alfa)
    if not key in list: return(key)

def dateCalc(date='%Y-%m-%d %H:%M:%S', calc=['+','-'], qt=0, method=['second','minute','hour']):
  if type(calc) == type([]): calc = '+'
  if type(method) == type([]): method = 'second'
  if '%' in date: date = dt.now()
  else: date = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
  if calc == '+':
    if method == 'second': new = (date + td(seconds=qt)).strftime('%Y-%m-%d %H:%M:%S')
    elif method == 'minute': new = (date + td(minutes=qt)).strftime('%Y-%m-%d %H:%M:%S')
    elif method == 'hour': new = (date + td(hours=qt)).strftime('%Y-%m-%d %H:%M:%S')
  elif calc == '-':
    if method == 'second': new = (date - td(seconds=qt)).strftime('%Y-%m-%d %H:%M:%S')
    elif method == 'minute': new = (date - td(minutes=qt)).strftime('%Y-%m-%d %H:%M:%S')
    elif method == 'hour': new = (date - td(hours=qt)).strftime('%Y-%m-%d %H:%M:%S')
  return(new)

class Instance:
  def __init__(self):
    self.list_repeat = {}

  def non_repeat(self, string, id='all'):
    if not id in self.list_repeat: self.list_repeat[id] = []
    if string == 'reset': 
      self.list_repeat[id] = []
      return(None)
    else:
      if string in self.list_repeat[id]: return(False)
      else:
        self.list_repeat[id].append(string)
        return(True)

  def time(self, type='str', date=None):
    if date == None:
      if type == 'str': return(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
      elif type == 'timestamp': return(dt.timestamp(dt.now()))
      elif type == 'obj': return(dt.now())
    else:
      if 'T' in date: date = date.replace('T', ' ')+':00'
      if type == 'str': 
        try: return(date.strftime("%Y-%m-%d %H:%M:%S"))
        except: return(dt.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S"))
      elif type == 'timestamp': return(dt.timestamp(self.time('obj', date)))
      elif type == 'obj': return(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))

  def dateFormat(self, date, format):
    obj = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
    return(obj.strftime(format))

  def exists(self, sysPath, file):
    result = os.path.exists(sysPath+'/'+file)
    if not result: result = os.path.exists(file)
    return(result)

  def saudation(self):
    hour = int(dt.now().strftime("%H"))
    if hour < 1: return('Boa noite')
    elif hour < 12: return('Bom dia')
    elif hour < 19: return('Boa tarde')
    else: return('Boa noite')

  def getKey(self, characters=8, list=[]):
    alfa = [
      'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
      'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
      '0','1','2','3','4','5','6','7','8','9']
    while True:
      key = ''
      for i in range(characters): key += random.choice(alfa)
      if not key in list: return(key)

  def dateCalc(self, date='%Y-%m-%d %H:%M:%S', calc=['+','-'], qt=0, method=['second','minute','hour']):
    if type(calc) == type([]): calc = '+'
    if type(method) == type([]): method = 'second'
    if '%' in date: date = dt.now()
    else: date = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
    if calc == '+':
      if method == 'second': new = (date + td(seconds=qt)).strftime('%Y-%m-%d %H:%M:%S')
      elif method == 'minute': new = (date + td(minutes=qt)).strftime('%Y-%m-%d %H:%M:%S')
      elif method == 'hour': new = (date + td(hours=qt)).strftime('%Y-%m-%d %H:%M:%S')
    elif calc == '-':
      if method == 'second': new = (date - td(seconds=qt)).strftime('%Y-%m-%d %H:%M:%S')
      elif method == 'minute': new = (date - td(minutes=qt)).strftime('%Y-%m-%d %H:%M:%S')
      elif method == 'hour': new = (date - td(hours=qt)).strftime('%Y-%m-%d %H:%M:%S')
    return(new)