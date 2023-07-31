import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sweepID = range(66,77)
plt.figure(constrained_layout=True)
plt.ylim(top=3,bottom=-3)

for cell in range(11):
    unit_paramsets = pd.read_csv("/pscratch/sd/k/ktub1999/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/10024729/unitParams/unitParam"+str(sweepID[cell])+".csv")
    # plt.plot()
    x=range(0,19,1)
    
    
    x_val=list(unit_paramsets["param_names"])
    plt.scatter(x,unit_paramsets["unit_params"])
y1 = np.ones_like(x)
plt.plot(x,y1,'_')
y2 = -np.ones_like(x)
# plt.axvline(, color='black', linestyle='dashed')
plt.plot(x,y2,'_',color='b')
plt.xticks(x,x_val,rotation=90)
plt.savefig("unitValues_Norn_Nrow2.png")
