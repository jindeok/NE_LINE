import numpy as np
import networkx as nx
import pandas as pd
import random as rnd
import matplotlib.pyplot as plt
import LINE as LINE

## edge sampling 미구현

#data trimming__ Karate
edge1 = pd.read_csv("karate_club.edgelist",sep = ' ', names = ['x','y','z'])

#Karate edgematrix
Karate, KarateMat = LINE.Make_Edgeval(edge1)

### main


# LINE
line = LINE.Line(data_set = Karate, data_set_mat = KarateMat, d = 2, epoch = 200, lr = 0.025, negnum = 5)

for i in range(line.r):
    
   # DW.first_optimizer()    
   line.second_optimizer()

    
# scattering plot

labels = []
labels_num = []
for i in range(len(KarateMat)):
    if(i in list([0,1,2,3,4,5,6,7,10,11,12,13,16,17,19,21])):
        labels.append("red")
        labels_num.append(0)
    else:
        labels.append("blue")
        labels_num.append(1)
        
		
df = pd.DataFrame(line.ui,columns=["x","y"]) ## plot 할 matrix
df_save = pd.DataFrame(line.ui, columns = ["x1","x2"])

df['label'] = labels
df_save['labels_num'] = labels_num

fig1 = plt.figure()
ax1 = fig1.add_subplot()
ax1.scatter(df['x'], df['y'], c = df['label'])

for i in range(len(KarateMat)):
    xtemp = df.get_value(i,'x')
    ytemp = df.get_value(i,'y')    
    ax1.text(xtemp+0.02, ytemp+0.02, i)

df_save.to_csv("embeddedKarate.csv", header = False)