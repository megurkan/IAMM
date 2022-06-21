import base_model_GCE as base1
import base_model_PCE as base2
import numpy as np
import random
import matplotlib.pyplot as plt

rep = 20

T = 15
M = 10
K = 100
A = 25 
h = 1
v = 5
alpha = 5
varphi = 1.5


CEdomain = np.linspace(800,1700,num=20)   
     
CEprofit = np.zeros((rep,len(CEdomain)))
CEamount = np.zeros((rep,len(CEdomain)))
CEcost = np.zeros((rep,len(CEdomain)))

CEprofit2 = np.zeros((rep,len(CEdomain)))
CEamount2 = np.zeros((rep,len(CEdomain)))
CEcost2 = np.zeros((rep,len(CEdomain)))

random.seed(215)
for i in range(rep): 
    
        
    betaset,pmax = {},{}        
    betaset = {t: random.randrange(80,120,step=5) for t in range(1,T+1)}
    pmax = {t: (betaset[t] - 20) / alpha for t in range(1,T+1)}
    pmin = 5. 
    
    dmax = {t: betaset[t]-pmin*alpha for t in range(1,T+1)}
    dmin = {t: betaset[t]-pmax[t]*alpha for t in range(1,T+1)}

    C = varphi*(sum(betaset[t]-pmin*alpha for t in range(1,T+1))/T)/M
    
    f = {t: A*0.25 for t in range(1,T+1)}
    r = {t: 2 for t in range(1,T+1)}
    b = {t: 2 for t in range(1,T+1)}
    
    index = 0
    for GCE in CEdomain:
        
        res = base1.lotsizing(T,K,A,h,v,C,f,r,b,GCE,M,betaset,alpha,pmin,pmax,dmax,TimeLimit=None)
        res2 = base2.lotsizing(T,K,A,h,v,C,f,r,b,GCE/T,M,betaset,alpha,pmin,pmax,dmax,TimeLimit=None)


        CEprofit[i][index] = res[0]
        CEamount[i][index] = res[2]
        CEcost[i][index] = res[4]
        
        
        CEprofit2[i][index] = res2[0]
        CEamount2[i][index] = res2[2]
        CEcost2[i][index] = res2[4]

       
        index += 1           
        
        
        
     
CEprofit_avg, CEamount_avg, CEcost_avg  = np.mean(CEprofit,axis=0), np.mean(CEamount,axis=0), \
                                                        np.mean(CEcost,axis=0)

CEprofit_avg2, CEamount_avg2, CEcost_avg2  = np.mean(CEprofit2,axis=0), np.mean(CEamount2,axis=0), \
                                                        np.mean(CEcost2,axis=0)



''' PLOT '''
fig = plt.figure(figsize=(6.2,3.05),dpi=80)
ax1 = fig.add_subplot()
ax2 = ax1.twiny()
ax1.set_xlabel('Global Karbon Salınım Üst Sınırı') 
ax2.set_xlabel('Dönemsel Karbon Salınım Üst Sınırı') 
ax1.set_ylabel('İşletme Karlılığı')
CEdomain2 = CEdomain/15 
ax1.plot(CEdomain,CEprofit_avg,color='black',marker='x',label='Global')
ax2.plot(CEdomain2,CEprofit_avg2,color='black',marker='x',linestyle='dashed',label='Dönemsel')

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
lines = lines_1 + lines_2
labels = labels_1 + labels_2
ax1.legend(lines, labels, loc=0)
plt.show()