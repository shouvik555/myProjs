import requests

def tfun(*myVar):
  for i in myVar:
     print(i)

def nfun(**myVar):
  print(__name__)
  for key, val in myVar.items():
     print(key, val)

nfun(mv='1,2', nv='3')
