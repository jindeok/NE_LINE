import numpy as np
import networkx as nx
import random as rnd


# LINE class define
class Line:
    
    #initialization
    def __init__(self, data_set, data_set_mat, d, epoch, lr, negnum):        
        
        self.Glen = len(data_set_mat) 
        self.ui = np.random.rand(self.Glen, d) # embedding vector  
        self.uj = np.random.rand(self.Glen, d) # comtext emb vector
        self.data_set = data_set # edge data
        self.data_set_mat = data_set_mat # data_set matrix
        self.d = d # embedding dimension
        self.r = epoch # epoch
        self.negnum = negnum # negsample 
        self.LR = lr # learning rate

             
    
    
    def GetNegPosSampleIndex_dist(self, vi):
        
        #negative sample
        negsamp = np.zeros(self.negnum, dtype = "i")   
        unconnected = np.where(self.data_set_mat[vi] == 0)
        unconnected = np.array(unconnected)[1]
        unconnected = np.delete(unconnected, 0) # vertex 자신 제외   
        negdegree = self.GetEdgeDegree(unconnected)
        negdegree75 = np.power(negdegree, 0.75)
        negdist75 = negdegree75 / np.sum(negdegree75)

        negsamp = np.random.choice(unconnected, self.negnum, replace = True, p = negdist75)

        #positive sample   
        connected = np.where(self.data_set_mat[vi] == 1)
        connected = np.array(connected)[1]
        
        possamp = connected

        return negsamp, possamp        
          

        
        
    def GetEdgeDegree(self, neglist):        

        neglistdeg = []
        
        for i in neglist:
            
            temp = np.sum(self.data_set_mat[i,:])
            neglistdeg.append(temp)
        
        return neglistdeg
        
        
        
    
    def first_optimizer(self):                

        for vi in range(self.Glen): # 모든 node interation      
            
            neg, pos = self.GetNegPosSampleIndex_dist(vi)
            
            for vj in pos: 
                
                self.ui[vj,:]=self.ui[vj,:]-self.LR*(sigmoid(np.dot(self.ui[vi,:],self.ui[vj,:]))-1)*self.ui[vi,:]
                
            for vj in neg:  
                
                self.ui[vj,:]=self.ui[vj,:]-self.LR*(sigmoid(np.dot(self.ui[vi,:],self.ui[vj,:])))*self.ui[vi,:]
        
        
   
    def second_optimizer(self):
        
        for vi in range(self.Glen):
            
            neg, context = self.GetNegPosSampleIndex_dist(vi)
                        
            for vj in context: 
                
                self.uj[vj,:]=self.uj[vj,:]-self.LR*(sigmoid(np.dot(self.ui[vi,:],self.uj[vj,:]))-1)*self.ui[vi,:]
                self.ui[vj,:]=self.ui[vj,:]-self.LR*(sigmoid(np.dot(self.ui[vi,:],self.uj[vj,:]))-1)*self.ui[vi,:]
                
            for vj in neg:  
                
                self.ui[vj,:]=self.ui[vj,:]-self.LR*(sigmoid(np.dot(self.ui[vi,:],self.ui[vj,:])))*self.ui[vi,:]
        
             

# activation func      
                
def softmax(arr):    
    
    m = np.argmax(arr)
    arr = arr - m
    arr = np.exp(arr)
    
    return arr / np.sum(arr)

def sigmoid(arr):
    
    return 1.0/(1.0 + np.exp(-arr))


# 데이터 가공 func
    
def Make_Edgeval(edge):    

    G = nx.Graph()
    
    for i in range(edge.shape[0]):
        
        G.add_node(node_for_adding = edge['x'][i])
        G.add_node(node_for_adding = edge['y'][i])
        G.add_edge(edge['x'][i], edge['y'][i])
    
    edge_val = np.zeros((edge.shape[0],2))
    edge_val[:,0] = edge['x'] ; edge_val[:,1] = edge['y']
    
    EdgeMat = nx.to_numpy_matrix(G,nodelist = sorted(G.nodes())) 
    
    return edge_val,EdgeMat    

