from pyibt.read_ibt import Read_IBT
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_pdf
import csv
import h5py
import os,sys,time
import json


def normalize_volts(volts,name='',verb=1):  # slows down the code a lot
    Ta = time.time()
    #print('WW1',volts.shape,volts.dtype)

    #... for breadcasting to work the 1st dim (=timeBins) must be skipped
    # X=np.swapaxes(volts,0,1).astype(np.float32) # important for correct result
    #print('WW2',X.shape)
    X=volts    
    xm=np.mean(X,axis=0) # average over time bins
    xs=np.std(X,axis=0)
    elaTm=(time.time()-Ta)/60.
    print('Volts norm, xm:',xm.shape,'Xswap:',X.shape,'elaT=%.2f min'%elaTm)

    nZer=np.sum(xs==0)
    zerA=xs==0
    print('   nZer=%d %s  : name=%s'%(nZer,xs.shape,name))
    
    #... to see indices of frames w/ volts==const
    result = np.where(xs==0)  
    xs[xs==0]=1  #hack:  for zero-value samples use mu=1 to allow scaling
    X=(X-xm)/xs

    #... revert indices and reduce bit-size
    # volts_norm=np.swapaxes(X,0,1).astype(np.float16)
    volts_norm=X
    del X
    #print('WW3',volts_norm.shape,volts_norm.dtype)

    if verb>1: # report flat volts for each sample
        na,nb,nc=zerA.shape    
        for i,A in enumerate(zerA):
            if np.sum(A)==0: continue
            zSt=np.sum(A,axis=0)
            zBo=np.sum(A,axis=1)
            print('zer', i,np.sum(A),'stims:',zSt,' body:',zBo)
            #assert nZer==0  # to stop at 1st case
 
    return volts_norm,nZer



def resample_by_interpolation(signal, input_fs, output_fs):

    scale = output_fs / input_fs
    # calculate new length of sample
    n = round(len(signal) * scale)

    resampled_signal = np.interp(
        np.linspace(0.0, 1.0, n, endpoint=False),  # where to interpret
        np.linspace(0.0, 1.0, len(signal), endpoint=False),  # known positions
        signal,  # known data points
    )
    return resampled_signal



# file = open("/global/homes/k/ktub1999/ExperimentalData/PyForEphys/Data/Stims/cahotic_50khz.csv","r")
file = open("/global/homes/k/ktub1999/ExperimentalData/PyForEphys/Data/Stims/chaotic_50khz.csv","r")
data2 = list(csv.reader(file, delimiter=","))
file.close()
stim = [float(row[0]) for row in data2]

ibt = Read_IBT('/global/homes/k/ktub1999/ExperimentalData/PyForEphys/Data/012722B2.ibt')

params = range(66,77)

sweep = ibt.sweeps[75]
data=resample_by_interpolation(sweep.data[:20000],20000,4000)
print(np.count_nonzero(data[:1000]==0))

volts = np.zeros(shape=(11,4000,1,6))
# volts= np.empty(shape=(1,4000,1))
sample=0
probe =0
for sample in range(11):
    # for c,p in enumerate(params):
        c = 5
        sweep = ibt.sweeps[params[sample]]
        data = resample_by_interpolation(sweep.data[:20000],20000,4000)
        data = np.array(data)
        data-=6
        data_load=np.load('/global/homes/k/ktub1999/Neuron/neuron4/neuroninverter/packBBP3/Stats.npz')
        xm=data_load['Mean'][:4000]
        xs=data_load['Std'][:4000]
        # meanD = data.mean()
        # stdD = data.std()
        meanD=xm
        stdD=xs
        data.resize((4000,1))
        data_norm=(data-xm)/xs
        volts[sample,:4000,probe,c]=np.squeeze(data_norm)
        # volts[sample][:4000][probe][c]=data_norm
        # for d1,d in enumerate(data):
        #     volts[sample][d1][probe][c]=  (d-meanD)/stdD
        # data,nFlat = normalize_volts(data)

    # volts=np.append(volts,np.reshape(resample_by_interpolation(sweep.data[:20000],20000,4000),(1,4000,1)))

par = np.zeros((11,19))
meta={"message":"Experimentail data","Stim":'chaotic_50khz_interpolated',"params":[66,77]}
metaJ=json.dumps(meta)
array_data=[metaJ]
# dataset = hdf5_file.create_dataset(dataset_name, shape=(0,), maxshape=(None,), )
structured_array = np.array([json.dumps(meta) for obj in array_data], dtype=h5py.special_dtype(vlen=str))

# dataD['meta.JSON']=metaJ
hf = h5py.File('/global/homes/k/ktub1999/ExperimentalData/PyForEphys/Data_FeatureNorm/L5_TTPC1cADpyr2.mlPack1.h5','w')

hf.create_dataset('test_volts_norm', data=volts)
hf.create_dataset('test_unit_par', data=par)
hf.create_dataset('meta.JSON', data=structured_array,dtype=h5py.special_dtype(vlen=str))

hf.close()

