import sys
import os
from numpy import zeros, array
from numpy.linalg import inv
sys.path.append('/usr/local/facet/tools/python/F2_live_model')
from bmad import BmadLiveModel

def orbit_fit(f2m, bpmnames, x_raw, y_raw):
    """
    fits BPM data using linear maps, returns orbit at single position s0
    args:
        f2m: BmadLiveModel
        bpmnames: numpy array of BPM names
        x_raw, y_raw: numpy arrays of X and Y BPM readings
    return:
        x0, y0: fitted orbit parameters (x,x',delta), (y,y')
        x_fit, y_fit: numpy arrays (Nx3) of reconstructed orbits
    """
    N_bpms = len(bpmnames)
    bpm0 = bpmnames[0]
    bpm_s = array([f2m.S[f2m.ix[bpm]] for bpm in bpmnames])
    devnames = array([f2m.device_names[f2m.ix[bpm]] for bpm in bpmnames])

    Mx = zeros((N_bpms, 3))
    My = zeros((N_bpms, 2))
    
    # iterate over all bpms, for each one get the R matrix from bpm0 to that bpm
    # the construct rows of "M matrix" as defined in eqn 4
    for i, (dev,ele) in enumerate(zip(devnames,bpmnames)):
        
        # skip BPMs with problematic names/nonexistant
        ds = dev.split(':')
        dev2 = f'{ds[1]}:{ds[0]}:{ds[2]}'
        if (dev not in devnames) and (dev2 not in devnames):
            continue
        
        r = f2m.tao.matrix(bpm0, ele)['mat6']
    
        # matrix rows are made of r11,r12,r16 & r33,r34
        Mx[i] = array([r[0][0], r[0][1], r[0][5]])
        My[i] = array([r[2][2], r[2][3]])

    # calculate x0, y0 vectors using eqn 5 from docs
    x0 = inv(Mx.T @ Mx) @ Mx.T @ x_raw
    y0 = inv(My.T @ My) @ My.T @ y_raw

    return x0, y0, Mx @ x0, My @ y0
