from gurobipy import Model,GRB,quicksum
import random

 
def lotsizing(T,K,A,h,v,C,f,r,b,GCE,M,betaset,alpha,pmin,pmax,dmax,TimeLimit=None):
    
    m = Model()   
    
    
    z,qmach,x,p,q = {},{},{},{},{}
    
        
    x[0] = 0.0
    
    for t in range(1,T+1):
        p[t] = m.addVar(lb=pmin,ub=pmax[t],vtype='C')
        x[t] = m.addVar(lb=0,vtype='C')
        z[t] =  m.addVar(vtype='B')
        q[t] = m.addVar(lb=0,vtype='C')
        for k in range(1,M+1):
            qmach[k,t] = m.addVar(lb=0,vtype='C')
            z[k,t] =  m.addVar(vtype='B')
            
        
    m.modelSense = GRB.MAXIMIZE
    m.update()
    
    # MAXIMIZE PROFIT
    m.setObjective(quicksum(p[t]*(betaset[t]-alpha*p[t]) - 
                            (h * x[t] + K * z[t] + quicksum(A*z[k,t] + v * qmach[k,t] for k in range(1,M+1)))  
                            for t in range(1,T+1)))


    for t in range(1,T+1):
        m.addConstr(x[t-1] + quicksum(qmach[k,t] for k in range(1,M+1)) - x[t] == (betaset[t]-alpha*p[t]))
        for k in range(1,M+1):
            m.addConstr(qmach[k,t] <= C * z[k,t])

        m.addConstr(q[t] == quicksum(qmach[k,t] for k in range(1,M+1)))
        m.addConstr(q[t] <= quicksum(dmax[i] for i in range(t,T+1))*z[t])
    
    m.addConstr(quicksum(quicksum(f[t]*z[k,t] for k in range(1,M+1)) 
                         + r[t]*q[t] + b[t]*x[t] for t in range(1,T+1)) <= GCE)
    

    m.params.OutputFlag = 0
    
    if TimeLimit:
        m.params.TimeLimit = TimeLimit
   
    m.optimize()
  
    
    if m.status == GRB.OPTIMAL:
        
        totalRev = sum(p[t].x*(betaset[t]-alpha*p[t].x) for t in range(1,T+1))
        
        totalCost = sum(h * x[t].x + K * z[t].x + 
                        sum(A*z[k,t].x + v * qmach[k,t].x 
                            for k in range(1,M+1)) for t in range(1,T+1))
        
        totalCE = sum(sum(f[t]*z[k,t].x for k in range(1,M+1))
                  + r[t]*q[t].x + b[t]*x[t].x for t in range(1,T+1))

        OPT_p = list(range(T))
        
        for t in range(1,T+1):
            OPT_p[t-1] = p[t].x
        

    res = [m.objVal,OPT_p,totalCE,totalRev,totalCost,m.MIPGap,m.Runtime]
    return res

if __name__ == "__main__": 
    
    
    T = 15
    M = 10
    K = 100
    A = 25 
    h = 1
    v = 5
    alpha = 5
    varphi = 1.5
    GCE = 1000 
    
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
    
    res = lotsizing(T,K,A,h,v,C,f,r,b,GCE,M,betaset,alpha,pmin,pmax,dmax,TimeLimit=None)
    print(res)
        