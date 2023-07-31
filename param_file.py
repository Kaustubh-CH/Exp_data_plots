import pandas as pd
import numpy as np

temp_file="/temp_param_min-1+1.csv"

all_params=[]
dir = "/pscratch/sd/k/ktub1999/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/10024729/"
nrow=['e_pas_all','gNaTa_tbar_NaTa_t_axonal','gNaTs2_tbar_NaTs2_t_somatic','gNaTs2_tbar_NaTs2_t_apical','gIhbar_Ih_dend','gNap_Et2bar_Nap_Et2_axonal','gK_Pstbar_K_Pst_axonal','gCa_LVAstbar_Ca_LVAst_somatic']
# nrow=['e_pas_all','gNaTa_tbar_NaTa_t_axonal','gNaTs2_tbar_NaTs2_t_somatic']
nrowTrue=True #For all narrows = True
for unit in range(66,77):
    
    df = pd.read_csv(dir+"/unitParams/unitParam"+str(unit)+".csv")
    params =[]
    
    default_params_wide= pd.read_csv("/pscratch/sd/k/ktub1999/main/DL4neurons2/sensitivity_analysis/NewBase2/NewBase"+str(int(0))+".csv")
    default_params_nrow= pd.read_csv("/pscratch/sd/k/ktub1999/main/DL4neurons2/sensitivity_analysis/NewBase2/MeanParams"+str(int(0))+".csv")
    for i in range(len(df['unit_params'])):
        u = df["unit_params"].iloc[i]
        pram=df["param_names"].iloc[i]
        if(pram not in nrow and nrowTrue==False):
                B=default_params_wide["Values"].iloc[i]
        else:
                B=default_params_nrow["Values"].iloc[i]
        if(u<-1):
              u=-1
        elif(u>1):
              u=1
        # if(u<-1 or u>+1):
        #         params.append(B)
        #         continue
        if(pram=="e_pas_all" ):
                #P = Base*(A+B*u) because Linear Param, Ranges = -125, -25
                
                if(pram not in nrow and nrowTrue==False):
                        a_value=20
                else:
                        a_value=10
                params.append(B+a_value*u)
                # curr_phy_res.append(B*(a_value+b_value*u))

        elif(pram=="cm_somatic" or pram=="cm_axonal"):
                if(pram not in nrow and nrowTrue==False):
                        a_value=1.45 # For Wide
                else:
                        a_value = 0.875
                        B=1.125
                # a_value=1.45
                
                params.append(B+a_value*u)
                # curr_phy_res.append(B*(a_value+b_value*u))
        else:
                # a_value=1.0
                if(pram not in nrow):
                    a_value=1.5
                else:
                    a_value=1.0
                b_value=1.5                
                params.append(B*np.exp((u*a_value)*np.log(10)))
    all_params.append(params)

np.savetxt(dir+temp_file,all_params)
