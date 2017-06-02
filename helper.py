import pandas as pd
import numpy as np
conv = 219474.63
sos_exp = {2 : pd.Series([15.287, 16.41671, 8.713, 158.265, 404.141]),
        3 : pd.Series([112.061,77.112,15.61,396.055,882.35]),
        4 : pd.Series([826.19,557.1341,322.2,1989.497,3685.24]),
        5 : pd.Series([2212.598,1691.806,1341.893,4750.712,7603.15])}
sos_exp = pd.DataFrame(sos_exp)

line_form = 'atom: {:2} method: {:7} bs: {} ncore:{:4} {}'
line_form_sos = 'atom: {} method: {:7} bs: {} ncore:{} {:5.6E} hartree {:8.4f} cm^-1'

def error(period,group,basisset,method,frozencore,data):
    idx = pd.IndexSlice
    data_abs_error = data.copy() 
    data_perc_error = data.copy()

    for a in period:
        for b in group: 
            data_abs_error.loc[:,idx[a,b]] -= sos_exp[a][b]
            for bs in basisset:
                for met in method:
                    for fc in frozencore: 
                        if data_perc_error.loc[idx[met,bs,fc],idx[a,b]] != 0:  
                            data_perc_error.loc[idx[met,bs,fc],idx[a,b]] = 100*((data_perc_error.loc[idx[met,bs,fc],idx[a,b]]- sos_exp[a][b])/sos_exp[a][b])
                        else:
                            data_perc_error.loc[idx[met,bs,fc],idx[a,b]] = np.nan 
                        if data_abs_error.loc[idx[met,bs,fc],idx[a,b]] == -sos_exp[a][b]:
                            data_abs_error.loc[idx[met,bs,fc],idx[a,b]] = np.nan  
    return data_abs_error, data_perc_error

def get_sos(energy,a,g):
    sos = 0
    relenergy = []
    for i,e in enumerate(energy):
        relenergy.append((float(energy[i])-float(energy[0]))*conv)

    if len(relenergy)== 0 :
        sos = 0
    else:

        if a == 0:
            sos = relenergy[2]    
        elif a == 1:    
            sos = relenergy[1]    
        elif a == 4:
            sos = relenergy[4]    
        elif a ==2:
            sos = relenergy[8]-relenergy[4]    
            if g==2:
                sos = relenergy[10]-relenergy[4]    
        elif a == 3:
            sos = relenergy[5]    

#                      elif a == 1:    
#                        sos = relenergy[4]    
#                      elif a ==2:
#                        sos = relenergy[10]-relenergy[4]    
#                      elif a == 3:
    return relenergy, sos

def append_dat(title,mode,atom,method,basisset,n,energy,relenergy,sos):

    with open('data/energy'+title+'.dat', mode) as f:
        f.write(line_form.format(atom, method, basisset, n, energy))
        f.write('\n')

    with open('data/relenergy' + title + '.dat', mode) as f:
        f.write(line_form.format(atom, method, basisset, n, relenergy))
        f.write('\n')

    with open('data/sos' + title + '.dat', mode) as f:
        f.write(line_form_sos.format(atom, method, basisset, n, sos/conv, sos))
        f.write('\n')

def write_dat(title,mode):

    with open('data/energy'+title+'.dat', mode) as f:
        f.write('\n')
    with open('data/relenergy' + title + '.dat', mode) as f:
        f.write('\n')
    with open('data/sos' + title + '.dat', mode) as f:
        f.write('\n')

def get_var(g):

    if g == 2:
        nclosed = 1        
        basissets = ['dz','tz','qz','fz']
        atoms = ['B','C','N','O','F']
        ncore = [0,1]
    elif g == 3:
        nclosed = 5
        basissets = ['dz','tz','qz']
        atoms = ['Al','Si','P','S','Cl']
        ncore = [5]
    elif g == 4:
        nclosed = 14
        basissets = ['dz','tz','qz']
        atoms = ['Ga','Ge','As','Se','Br']
        ncore = [14]
    elif g == 5:
        nclosed = 23
        basissets = ['tz','qz']
        atoms = ['In','Sn','Sb','Te','I']
        ncore = [23]

    return nclosed,basissets,atoms,ncore
