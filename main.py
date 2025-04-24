import pickle
fich= open("metro.pkl",'rb')
graphMetroTest=pickle.load(fich)
graphMetro= pickle.load(fich)
dicMetro:dict= pickle.load(fich)
fich.close()
dicMetro[('Bibliothèque François Mitterand', '14')]=376 #On modifie la valeur d'un station car elle ne correspond pas

############################################################
#                            1.1                           #
############################################################


# a)pour une matrice de n sommets, on obtiendra une matrice d’adjacence
# de n² case, avec 2a case utiles et n²-2a case inutiles.
# Avec une liste adjacence, il y a uniquement 2a+n instances,
# avec toujours 2a utiles mais n case inutiles.

# b)
#si n²-2a < n
# n-(2a/n)<1
#       n²<n+2a
#       2a>n²-n
#        a>(n²-n)/2
# Pour un a inférieur à (n²-n)/2, la liste est plus efficace.


############################################################
#                            1.2                           #
############################################################

# Pour métro test, il y a 50 sommets et 100 arrêtes.
# Pour le métro de base, il y a 934  arrêtes et 376 sommets.

############################################################
#                            1.3                           #
############################################################

def indexSommet(station:str ,ligne:str)->int:
    assert isinstance(station,str) or isinstance(ligne,str)
    for i in dicMetro.keys():
        if i== (station,ligne):
            return dicMetro[i]
    return 'Station non-existante'

# print(indexSommet('Cluny, La Sorbonne', '10'))

############################################################
#                            1.4                           #
############################################################

def infoStation(indexSommet:int)->tuple:
    assert isinstance(indexSommet,int)
    for cle,val in dicMetro.items():
        if val ==indexSommet:
            return  cle
    return 'Station non-existante'

# print(infoStation(291))

############################################################
#                            1.5                           #
############################################################

def voisins(indexSommet:int)->list:
    return graphMetro[indexSommet]

# print(voisins(6))

############################################################
#                            1.6                           #
############################################################

def existe(indexSommet1:int,indexSommet2:int)->bool:
    for i in voisins(indexSommet1):
        if indexSommet2 ==i[0]:return True
    return False

# print(existe(291,292))

############################################################
#                            1.7                           #
############################################################

def poids(indexSommet1:int,indexSommet2:int)->int:
    for i in voisins(indexSommet1):
        if indexSommet2 ==i[0]:return i[1]
    return -1

# print (poids(291,292))

############################################################
#                            1.8                           #
############################################################

def aretes(Graph):
    temp=[]
    for i in range(len(Graph)):
        for ii in range(len(Graph[i])):
            temp.append((i,Graph[i][ii][0]))
    return temp

# print(aretes(graphMetroTest))

############################################################
#                            2.1                           #
############################################################

def enleve(L:list,elt:any)->list:
    assert elt in L, "élément non présent"
    L.remove(elt)
    return L

############################################################
#                            2.2                           #
############################################################

def dijkstra(Graph:list,SommetInitial:int)->list:
    nonVisites=[i for i in range(len(Graph))]
    distances=[float('inf') for _ in range(len(Graph))]
    distances[SommetInitial]=0
    while nonVisites!=[]:
        temp = min(j for i, j in enumerate(distances) if i in nonVisites)
        res = [i for i, j in enumerate(distances) if j == temp if i in nonVisites]
        enleve(nonVisites,res[0])
        for v in Graph[res[0]]:
            if distances[v[0]]>distances[res[0]]+v[1]:
                distances[v[0]]=distances[res[0]]+v[1]
    return distances

# print(dijkstra(graphMetroTest,15))

############################################################
#                            2.3                           #
############################################################

# La complexité de cet algorithme est O(n log n)

############################################################
#                            2.4                           #
############################################################

def dijkstraChem(Graph:list,SommetInitial:int)->list:
    nonVisites=[i for i in range(len(Graph))]
    distances=[float('inf') for _ in range(len(Graph))]
    distances[SommetInitial]=0
    Chem=[-1 for _ in range(len(Graph))]
    while nonVisites!=[]:
        temp = min(j for i, j in enumerate(distances) if i in nonVisites)
        res = [i for i, j in enumerate(distances) if j == temp if i in nonVisites]
        enleve(nonVisites,res[0])
        # print(nonVisites)
        for v in Graph[res[0]]:
            if distances[v[0]]>distances[res[0]]+v[1]:
                distances[v[0]]=distances[res[0]]+v[1]
                Chem[v[0]]=res[0]
    return distances,Chem

# print(dijkstraChem(graphMetro,371))

############################################################
#                            2.5                           #
############################################################

def cheminD(Graph:list,SommetInitial:int,SommetArrivée:int)->list:
    distances,Chem=dijkstraChem(Graph,SommetInitial)
    temp=[SommetArrivée,Chem[SommetArrivée]]
    while temp[-1]!=-1:
        temp.append(Chem[temp [-1]])
    return list(reversed(temp))

# print(cheminD(graphMetro,371,238))

############################################################
#                            2.6                           #
############################################################

def afficheChemin(stations:list)->str:
    str1=""
    nbSta=0
    for i in range(len(stations)):
        if stations[i]==-1:
            str1+='Entrez dans la station '
            i+=1
            pass
        elif stations[i]==stations[-1]:
            if nbSta!=0:
                str1+='Empruntez la ligne '+'('+infoStation(stations[i])[1]+')'+' sur '+str(nbSta)+' station(s) puis descendez à '+infoStation(stations[i])[0]+'\n'
            str1+='Vous êtes bien arrivés à '
        elif infoStation(stations[i])[0]==infoStation(stations[i+1])[0]:
            if nbSta!=0:
                str1+='Empruntez la ligne '+'('+infoStation(stations[i])[1]+')'+' sur '+str(nbSta)+' station(s) puis descendez à '+infoStation(stations[i])[0]+'\n'
            nbSta=0
            str1+='Prenez la correspondance entre la ligne '+'('+ infoStation(stations[i])[1]+')'+' et la ligne '+'('+infoStation(stations[i+1])[1]+')'+'\n'
            i+=1
            continue
        elif infoStation(stations[i])[1] == infoStation(stations[i+1])[1]:
            nbSta+=1
            continue
        str1+=  infoStation(stations[i])[0]+' '+'('+infoStation(stations[i])[1]+')'
        str1+='\n'
    return str1

# print(afficheChemin(cheminD(graphMetro,370,238)))