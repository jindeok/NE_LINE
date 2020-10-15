import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import LINE as LINE

# Dataset settings (Football Team)

G = nx.read_gml('football.gml')
H = nx.convert_node_labels_to_integers(G) # str to int numbering 
nx.write_edgelist(H, 'edgelistFile.csv', delimiter=' ')
edge1 = pd.read_csv("edgelistFile.csv",sep = ' ', names = ['x','y','z'])

Football, FootballMat = LINE.Make_Edgeval(edge1)





## ------------ main ------------------ --

LINE = LINE.Line(data_set = Football, data_set_mat = FootballMat, d = 2, epoch = 80, lr = 0.025, negnum = 8)

for i in range(LINE.r):
    LINE.first_optimizer()    
    #LINE.second_optimizer()
    
    







    
# ------------ Draw scattering graph ------------
    
I = open('football.gml','r')
IndexList = I.readlines()
grp1,grp2,grp3,grp4,grp5,grp6,grp7,grp8,grp9,grp10,grp11 = [],[],[],[],[],[],[],[],[],[],[]

for i in range(len(IndexList)):
    if 'id' in IndexList[i].split():
        node=int(IndexList[i].split()[1])
        grp=int(IndexList[i+2].split()[1])
        if grp == 0:
            grp1.append(node)
        elif grp == 1:
            grp2.append(node)
        elif grp == 2:
            grp3.append(node)            
        elif grp == 3:
            grp4.append(node)    
        elif grp == 4:
            grp5.append(node)
        elif grp == 5:
            grp6.append(node)
        elif grp == 6:
            grp7.append(node)
        elif grp == 7:
            grp8.append(node)
        elif grp == 8:
            grp9.append(node)            
        elif grp == 9:
            grp10.append(node)    
        else:
            grp11.append(node)
            
labels = []
labels_num = []

for i in range(len(FootballMat)):
    if(i in grp1):
        labels.append("r")
        labels_num.append(0)
    elif(i in grp2):
        labels.append("b")
        labels_num.append(1)
    elif(i in grp3):
        labels.append("g")
        labels_num.append(2)
    elif(i in grp4):
        labels.append("c")
        labels_num.append(3)
    elif(i in grp5):
        labels.append("m")
        labels_num.append(4)
    elif(i in grp6):
        labels.append("y")
        labels_num.append(5)
    elif(i in grp7):
        labels.append("k")
        labels_num.append(6)
    elif(i in grp8):
        labels.append("#9900cc")
        labels_num.append(7)              
    elif(i in grp9):
        labels.append("#993300")
        labels_num.append(8)              
    elif(i in grp10):
        labels.append("#552211")
        labels_num.append(9)             
    elif(i in grp11):
        labels.append("#3355cc")      
        labels_num.append(10)              

df = pd.DataFrame(LINE.ui,columns=["x","y"]) ## plot 할 matrix
df_save = pd.DataFrame(LINE.ui, columns = ["x1","x2"])

df['label'] = labels
df_save['labels_num'] = labels_num

fig1 = plt.figure()
ax1 = fig1.add_subplot()
ax1.scatter(df['x'], df['y'], c = df['label'])
def textshowing(dataMat):
    for i in range(len(dataMat)):
        xtemp = df.get_value(i,'x')
        ytemp = df.get_value(i,'y')
        ax1.text(xtemp+0.02, ytemp+0.02, i)

#textshowing(FootballMat)

df_save.to_csv("embeddedFootball.csv", header = False)