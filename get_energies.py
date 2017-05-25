import sys 
import os.path
from qgrep import bagel 
import pandas as pd
import numpy as np

sos_exp = {2 : pd.Series([15.287, 16.41671, 8.713, 158.265, 404.141]),
        3 : pd.Series([112.061,77.112,15.61,396.055,882.35]),
        4 : pd.Series([826.19,557.1341,322.2,1989.497,3685.24]),
        5 : pd.Series([2212.598,1691.806,1341.893,4750.712,7603.15])}
sos_exp = pd.DataFrame(sos_exp)
energy = []
sos = 0
energy_cas = []
sos_cas = 0
conv = 219474.63
line_form = 'atom: {:2} method: {:7} bs: {} ncore:{:4} {}'
line_form_sos = 'atom: {} method: {:7} bs: {} ncore:{} {:5.6E} hartree {:8.4f} cm^-1'

def get_data():
    #initializing files 
    with open('data/energy.dat', 'w') as f:
        f.write('\n') 
    with open('data/relenergy.dat', 'w') as f:
        f.write('\n')
    with open('data/sos.dat', 'w') as f:
        f.write('\n')

    #forming pandas multiindex dataframe structure 
    col = [[2,3,4,5],[0,1,2,3,4]]
    row = [['zcasscf','caspt2', 'mrci'],['dz','tz','qz','fz'],['fc','nfc']]
    cols = pd.MultiIndex.from_product(col, names = ['period','group'])
    rows = pd.MultiIndex.from_product(row, names = ['methods','basisset','frozencore'])

    data = pd.DataFrame(np.zeros((24,20)), index = rows, columns = cols).sort_index().sort_index(axis=1) #np.zeros is row by columns

    #initializing variables
    methods = ['caspt2','mrci']
    group = [2,3,4,5]

    for g in group:
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
        for basisset in basissets:
            for a, atom in enumerate(atoms):
                for method in methods:
                    for n in ncore:           
                        relenergy = []
                        relenergy_cas = []
                        path = '{}/{}/{}/{}/'.format(g, basisset, atom, method)
                        if g==2:
                            path += 'ncore' + str(n) + '/'
                        path += 'output.dat'
                        #print(path)
                        if os.path.isfile(path) == True:
                            with open(path, 'r') as f:
                                lines = f.readlines()

                            if method == 'caspt2':

                                energy_cas = bagel.get_energy(lines, 'zcasscf') 

                                for i,e in enumerate(energy_cas):
                                    relenergy_cas.append(float(energy_cas[i])-float(energy_cas[0])) 
                                if len(relenergy_cas) == 0 :
                                    sos_cas = 0
                                else:
                                    if a == 0:
                                        sos_cas = relenergy_cas[2]    
                                    elif a == 1:    
                                        sos_cas = relenergy_cas[1]    
                                    elif a == 4:
                                        sos_cas = relenergy_cas[4]    
                                    elif a==2:
                                        sos_cas = relenergy_cas[8]-relenergy_cas[4]    
                                        if g==2:
                                            sos_cas = relenergy_cas[10]-relenergy_cas[4]    
                                    elif a == 3:
                                        sos_cas = relenergy_cas[5]    

                                   # elif a == 1:    
                                   #     sos_cas = relenergy_cas[4]    
                                   # elif a ==2:
                                   #     sos_cas = relenergy_cas[10]-relenergy_cas[4]    
                                   # elif a == 3:
                                   #     sos_cas = relenergy_cas[8]    

                                if n==0:
                                    frocore = 'nfc'
                                else:
                                    frocore = 'fc'

                                data[g,a]['zcasscf',basisset, frocore] =sos_cas*conv

                                with open('data/energy.dat', 'a') as f:
                                    f.write(line_form.format(atom, 'casscf', basisset, n, energy_cas))
                                    f.write('\n')

                                with open('data/relenergy.dat', 'a') as f:
                                    f.write(line_form.format(atom, 'casscf', basisset, n, relenergy_cas))
                                    f.write('\n')

                                with open('data/sos.dat', 'a') as f:
                                    f.write(line_form_sos.format(atom,  'casscf' , basisset, n, sos_cas, sos_cas*conv))
                                    f.write('\n')

                            energy = bagel.get_energy(lines, method) 

                            for i,e in enumerate(energy):
                                relenergy.append(float(energy[i])-float(energy[0]))

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

#                                elif a == 1:    
#                                    sos = relenergy[4]    
#                                elif a ==2:
#                                    sos = relenergy[10]-relenergy[4]    
#                                elif a == 3:

                            if n==0:
                                frocore = 'nfc'
                            else:
                                frocore = 'fc'

                            data[g,a][method, basisset,frocore] =sos*conv

                            with open('data/energy.dat', 'a') as f:
                                f.write(line_form.format(atom, method, basisset, n, energy))
                                f.write('\n')

                            with open('data/relenergy.dat', 'a') as f:
                                f.write(line_form.format(atom, method, basisset, n, relenergy))
                                f.write('\n')

                            with open('data/sos.dat', 'a') as f:
                                f.write(line_form_sos.format(atom, method, basisset, n, sos, sos*conv))
                                f.write('\n')
                        else:
                            pass  
        
    return data

def get_data_contracted():

    #initializing files 
    with open('data/energy_contracted.dat', 'w') as f:
        f.write('\n') 
    with open('data/relenergy_contracted.dat', 'w') as f:
        f.write('\n')
    with open('data/sos_contracted.dat', 'w') as f:
        f.write('\n')

    #forming pandas multiindex dataframe structure 
    col = [[2,3,4],[0,1,2,3,4]]
    row = [['zcasscf','caspt2', 'mrci'],['dz','tz','qz','fz'],['fc','nfc']]
    cols = pd.MultiIndex.from_product(col, names = ['period','group'])
    rows = pd.MultiIndex.from_product(row, names = ['methods','basisset','frozencore'])

    datac = pd.DataFrame(np.zeros((24,15)), index = rows, columns = cols).sort_index().sort_index(axis=1) #np.zeros is row by columns

    #initializing variables
    methods = ['caspt2','mrci']
    group = [2,3,4]

    for g in group:
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
        for basisset in basissets:
            for a, atom in enumerate(atoms):
                for method in methods:
                    for n in ncore:           
                        relenergy = []
                        relenergy_cas = []
                        path = 'contracted/{}/{}/{}/{}/'.format(g, basisset, atom, method)
                        if g==2:
                            path += 'ncore' + str(n) + '/'
                        path += 'output.dat'
                        print(path)

                        if os.path.isfile(path) == True:
                            with open(path, 'r') as f:
                                lines = f.readlines()

                            if method == 'caspt2':

                                energy_cas = bagel.get_energy(lines, 'zcasscf') 

                                for i,e in enumerate(energy_cas):
                                    relenergy_cas.append(float(energy_cas[i])-float(energy_cas[0])) 
                                if len(relenergy_cas) == 0 :
                                    sos_cas = 0
                                else:
                                    if a == 0:
                                        sos_cas = relenergy_cas[2]    
                                    elif a == 1:    
                                        sos_cas = relenergy_cas[1]    
                                    elif a == 4:
                                        sos_cas = relenergy_cas[4]    
                                    elif a==2:
                                        sos_cas = relenergy_cas[8]-relenergy_cas[4]    
                                        if g==2:
                                            sos_cas = relenergy_cas[10]-relenergy_cas[4]    
                                    elif a == 3:
                                        sos_cas = relenergy_cas[5]    

                                   # elif a == 1:    
                                   #     sos_cas = relenergy_cas[4]    
                                   # elif a ==2:
                                   #     sos_cas = relenergy_cas[10]-relenergy_cas[4]    
                                   # elif a == 3:
                                   #     sos_cas = relenergy_cas[8]    

                                if n==0:
                                    frocore = 'nfc'
                                else:
                                    frocore = 'fc'

                                datac[g,a]['zcasscf',basisset, frocore] =sos_cas*conv

                                with open('data/energy_contracted.dat', 'a') as f:
                                    f.write(line_form.format(atom, 'casscf', basisset, n, energy_cas))
                                    f.write('\n')

                                with open('data/relenergy_contracted.dat', 'a') as f:
                                    f.write(line_form.format(atom, 'casscf', basisset, n, relenergy_cas))
                                    f.write('\n')

                                with open('data/sos_contracted.dat', 'a') as f:
                                    f.write(line_form_sos.format(atom,  'casscf' , basisset, n, sos_cas, sos_cas*conv))
                                    f.write('\n')

                            energy = bagel.get_energy(lines, method) 

                            for i,e in enumerate(energy):
                                relenergy.append(float(energy[i])-float(energy[0]))

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

                                #elif a == 1:    
                                #    sos = relenergy[4]    
                                #elif a ==2:
                                #    sos = relenergy[10]-relenergy[4]    
                                #elif a == 3:
                                #    sos = relenergy[8]    

                            if n==0:
                                frocore = 'nfc'
                            else:
                                frocore = 'fc'

                            datac[g,a][method, basisset,frocore] =sos*conv

                            with open('data/energy_contracted.dat', 'a') as f:
                                f.write(line_form.format(atom, method, basisset, n, energy))
                                f.write('\n')

                            with open('data/relenergy_contracted.dat', 'a') as f:
                                f.write(line_form.format(atom, method, basisset, n, relenergy))
                                f.write('\n')

                            with open('data/sos_contracted.dat', 'a') as f:
                                f.write(line_form_sos.format(atom, method, basisset, n, sos, sos*conv))
                                f.write('\n')
                        else:
                            pass  
        
    return datac

def get_error(data):
    idx = pd.IndexSlice
    group = [0,1,2,3,4]
    period = [2,3,4,5]
    basisset= ['dz','tz','qz','fz']
    method = ['zcasscf','caspt2','mrci']
    frozencore = ['fc','nfc']
    data_abs_error = data.copy() 
    data_perc_error = data.copy()
    #print(data_abs_error.loc[:,idx[2,0]])
    #print(sos_exp[2][0])
    
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
#    print(data_abs_error.loc[idx['caspt2','fz','fc'],idx[2,4]])
 #   print(data_abs_error[2,4]['caspt2','fz','fc'])
    return data_abs_error, data_perc_error

def get_error_contracted(data):
    idx = pd.IndexSlice
    group = [0,1,2,3,4]
    period = [2,3,4]
    basisset= ['dz','tz','qz','fz']
    method = ['zcasscf','caspt2','mrci']
    frozencore = ['fc','nfc']
    #sos_exp[2][3] column by row 
    data_abs_error = data.copy() 
    data_perc_error = data.copy()
    #print(data_abs_error.loc[:,idx[2,0]])
    #print(sos_exp[2][0])
    
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
if __name__=='__main__':
    get_data()
    get_data_contracted()
