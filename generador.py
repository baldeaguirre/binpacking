# =============================================================================
# objetos: 10
# contenedores: 10 
# capacidad_contenedores: 10 
# tama~nos_objetos:
# 1.2 5 3 2.5 7 0.8 6.5 5 9 4.5
# =============================================================================


# Num_obj  10, 20, ... ,150
# Contenedores=num_obj
# Capacidad de los contenedores ={1*max_rango, 2*max_rango} 
# Rango de los tamaños de los objetos 15-30, 30-45, 45-60
# Replicas 5
# Total = 30*15 = 450
# bin_n_10_m_10_cap_30_rn_15-30_rep_1.txt

from random import randint

rango=[(15,30), (30,45), (45,60)]
        
for n in range(10, 151, 10):
    for rnmin,rnmax in rango:
        for i in range(1,3):
            for rep in range(1,6):
                nombre2 = "instancias/bin_n_%d_m_%d_cap_%d_rn_%d-%d_rep_%d.txt" % (n,n,i*rnmax,rnmin,rnmax,rep)
                with open(nombre2, "w") as salida:
                    print("objetos:", n, file=salida)
                    print("contenedores:", n, file=salida)
                    print("capacidad_contenedores:", i*rnmax, file=salida)
                    print("tamaño_objetos:", file=salida)
                    for obj in range(1, n+1):
                        print(randint(rnmin,rnmax), end=" ",file=salida)
