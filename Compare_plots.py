import h5py
import os
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import pandas as pd

p=[1,1,0,0,0]

stimFile="/global/homes/k/ktub1999/mainDL4/DL4neurons2/stims/5k50kInterChaoticB.csv"
directoryV = '/pscratch/sd/k/ktub1999/BBP_TEST1/runs2/10025599_1/L5_TTPC1_cADpyr232_1/c1/L5_TTPC1_cADpyr232_1-v3-0-1-c1.h5'
with h5py.File(directoryV, 'r') as f:
    volts_sim=f['volts']
    directoryK= '/global/homes/k/ktub1999/ExperimentalData/PyForEphys/Data3/WithoutNormExp.h5' #H.RUN
    with h5py.File(directoryK, 'r') as f2:
        volts = f2['test_volts_norm']    
    
        pdf = matplotlib.backends.backend_pdf.PdfPages("compareExp_New_Wide11_MinMax.pdf")

        for i in range(volts_sim.shape[0]):
                fig, axs = plt.subplots(3,sharex = False,sharey = False, gridspec_kw = {'height_ratios':[1,4,4]})
                # fig.suptitle("cm_axon,soma"+str( f2['phys_par'][i][12])+"epass:"+str( f2['phys_par'][i][18]))
                probeVyas=0
                # for probe in range(f['voltages'].shape[2]):
                df = pd.read_csv(stimFile)
                axs[0].plot(df[df.columns[0]][1000:],label= 'I', color = 'pink', linewidth=0.5)
                aV=[]
                for a1 in range(len(volts_sim[i])):
                        aV.append(volts_sim[i][a1][probeVyas])
                axs[1].plot(aV,color='r',linewidth=0.5)
                
                probe=0
                stim_select=5
                aK=[]
                for a1 in range(len(volts[i])):
                        aK.append(volts[i][a1][probe][stim_select])
                # print("Orignal Exp",aK[0]+6)
                # print("Current Exp",aK[0])
                # print("Simulated",aV[0])


                axs[2].plot(aK,color='b',linewidth=0.5)
                axs[1].set_ylabel("Simulated")
                axs[2].set_ylabel("Experimental")
                pdf.savefig(fig)
                fig = plt.figure()
                
                plt.plot(aV,color='r',linewidth=0.5)
                plt.plot(aK,color='b',linewidth=0.5)
                plt.legend(['Simulated ','Exp Interpolated'])

                pdf.savefig(fig)
                
                # fig, axs = plt.subplots(2,sharex = True,sharey = False, gridspec_kw = {'height_ratios':[1,1]})
                # axs[0].scatter(range(len(f['norm_par'][i])),f['phys_par'][i],color='r')
                # axs[1].scatter(range(len(f2['phys_par'][i])),f2['phys_par'][i],color='b')
                # plt.legend(['Current'])
                
                
                # # break
                # pdf.savefig(fig)
        pdf.close()



    



