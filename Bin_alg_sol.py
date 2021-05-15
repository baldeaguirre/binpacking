# =============================================================================
# objetos: 10
# contenedores: 10 
# capacidad_contenedores: 10 
# tama~nos_objetos:
# 1.2 5 3 2.5 7 0.8 6.5 5 9 4.5
# =============================================================================

def leerInstancia(filename):
    with open(filename, "r") as entrada:
        algo, n = entrada.readline().split()
        algo, m = entrada.readline().split()
        algo, cap = entrada.readline().split()
        algo = entrada.readline()
        size =[]
        for item in entrada.readline().split():
            size.append( int(item) )
    return int(n), int(m), int(cap), size
  
def bin_MILP(filename, n_obj, n_con, cap, S):
    import gurobipy as gp
    from gurobipy import GRB

    #Crear el modelo
    m = gp.Model("BinPacking")
    
    I = range(n_obj)
    J = range(n_con)
    
    # Agregar variables al modelo
    y = m.addVars( J, vtype=GRB.BINARY, name= "y")
    x = m.addVars( I, J, vtype=GRB.BINARY, name= "x")
    
    # Agregar las restricciones al modelo
    m.addConstrs( ((gp.quicksum(S[j]*x[i,j] for i in I)) <= cap*y[j]  for j in J), "cap")
    m.addConstrs( ( x.sum(i,"*")  == 1  for i in I), "asig")
    m.addConstrs( ( y[j]  >= y[j+1]  for j in range(n_con-1)), "sim")
        
    # Agregar la funcion objetivo
    m.setObjective( (y.sum("*")), GRB.MINIMIZE)
        
    # Resolver el modelo y extraer la informacion relevante
    m.optimize()
    
    #for v in m.getVars():
    #    if(v.x >0.5):
    #        print('%s = %d' % (v.varName, v.x))
    
    with open("tablaBinMip.txt", "a") as salida:
        print('File %s Status %g Obj %.3f ObjBound %.3f GAP %.3f GRB.Time %.4f' %
              (filename, m.Status, m.objVal, m.objBound, m.MIPGAP, m.runtime), file=salida)
    #for j in J:
    #    print("%g %d" %(y[j].varName, y[j].x))
    return


def firstFit_ByObj(filename, n_obj, n_con, cap, S):
    sol=[[]]
    ocu=[0]
    I = list(range(n_obj))
    
    for obj in I:
        J= range(len(sol))
        Nuevo = True
        for con in J:
            if (ocu[con] + S[obj]<= cap):
                sol[con].append(obj)
                ocu[con] += S[obj]
                Nuevo = False
                #print("Insertardo el objeto %d en el contenedor abierto %d" % (obj, con))
                #print(sol, ocu)
                break;
        if (Nuevo==True):
            sol.append([obj])
            ocu.append(S[obj])
            #print("Insertardo el objeto %d en un nuevo contenedor" % obj)
            #print(sol, ocu)
    print("Solucion con %d contenedores" % len(sol))
                
    
def firsFit_ByCont(filename, n_obj, n_con, cap, S):
    import numpy as np
    sol=[[]]
    ocu=[0]
    I = list(range(n_obj))
    I_agg = np.zeros(n_obj)
    con_act =0
    while (I_agg.sum() < n_obj):
        for obj in I:
            if(I_agg[obj]==0):
                if (ocu[con_act] + S[obj] <= cap):
                    sol[con_act].append(obj)
                    ocu[con_act] += S[obj]
                    I_agg[obj]=1
                    #print("Insertardo el objeto %d en el contenedor actual %d" % (obj, con_act))
                    #print(sol, ocu)
                #else:
                    #print("El objeto %d no cabe" % obj)
            #else:
                #print("el objeto %d fap" % obj)
        if(I_agg.sum() < n_obj):
            sol.append([])
            ocu.append(0)
            con_act +=1
            #print(I_agg)
            #print(sol, ocu)
        return

import sys
argv = sys.argv[1:]    # que quedo solo con los argumentos de interes de la lista
filename = argv[0]     # el nombre de la instancia la quedo guardado en la posición 0
    
#filename= "instancias/bin_n_20_m_20_cap_60_rn_15-30_rep_1.txt"   
no, nc, cap, S = leerInstancia(filename) 
       
bin_MILP(filename, no, nc, cap, S)
