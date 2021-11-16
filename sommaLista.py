def sommaLista(lista):
  somma=0
  for i in lista: 
     somma += i

  return somma     

listaNumeri = [3, 5, 6, 7, 4]

print("La somma della lista è {}".format(sommaLista(listaNumeri)))