import sys 
import os.path
from qgrep import bagel 
import pandas as pd
import numpy as np
import helper as h

energy = []
energy_cas = []

def get_data():
    #initializing files 
    h.write_dat('','w')

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
        nclosed,basissets,atoms,ncore = h.get_var(g)
        for basisset in basissets:
            for a, atom in enumerate(atoms):
                for method in methods:
                    for n in ncore:           
                        frocore = 'fc'
                        if n==0:
                            frocore = 'nfc'
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
                                relenergy_cas,sos_cas = h.get_sos(energy_cas,a,g)

                                data[g,a]['zcasscf',basisset, frocore] =sos_cas
                                
                                h.append_dat('','a',atom,method,basisset,n,energy_cas,relenergy_cas,sos_cas)

                            energy = bagel.get_energy(lines, method) 
                            relenergy,sos = h.get_sos(energy,a,g)
                            data[g,a][method, basisset,frocore] =sos

                            h.append_dat('','a',atom,method,basisset,n,energy,relenergy,sos)
        
    return data

def get_data_aux():

    #forming pandas multiindex dataframe structure 
    col = [[2],[0,1,2,3,4]]
    row = [['zcasscf','caspt2', 'mrci'],['dz'],['fc']]
    cols = pd.MultiIndex.from_product(col, names = ['period','group'])
    rows = pd.MultiIndex.from_product(row, names = ['methods','basisset','frozencore'])

    data = pd.DataFrame(np.zeros((3,5)), index = rows, columns = cols).sort_index().sort_index(axis=1) #np.zeros is row by columns

    #initializing variables
    methods = ['caspt2','mrci']
    group = [2]

    for g in group:
        basisset = 'dz'
        atoms = ['B','C','N','O','F']
        for a, atom in enumerate(atoms):
            for method in methods:
                relenergy = []
                relenergy_cas = []
                path = '{}/{}/aux_test/{}/{}/ncore1/'.format(g, basisset, atom, method)
                path += 'output.dat'
                #print(path)
                if os.path.isfile(path) == True:
                    with open(path, 'r') as f:
                        lines = f.readlines()

                    if method == 'caspt2':

                        energy_cas = bagel.get_energy(lines, 'zcasscf') 
                        relenergy_cas,sos_cas = h.get_sos(energy_cas,a,g)
                        data[g,a]['zcasscf',basisset, 'fc'] =sos_cas

                    energy = bagel.get_energy(lines, method) 
                    relenergy,sos = h.get_sos(energy,a,g)
                    data[g,a][method, basisset,'fc'] =sos
    
    return data

def get_data_contracted():

    #initializing files 
    h.write_dat('_contracted','w')

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
        nclosed,basissets,atoms,ncore = h.get_var(g)
        for basisset in basissets:
            for a, atom in enumerate(atoms):
                for method in methods:
                    for n in ncore:           
                        frocore = 'fc'
                        if n==0:
                            frocore = 'nfc'
                        path = 'contracted/{}/{}/{}/{}/'.format(g, basisset, atom, method)
                        if g==2:
                            path += 'ncore' + str(n) + '/'
                        path += 'output.dat'
                        #print(path)

                        if os.path.isfile(path) == True:
                            with open(path, 'r') as f:
                                lines = f.readlines()

                            if method == 'caspt2':

                                energy_cas = bagel.get_energy(lines, 'zcasscf') 
                                relenergy_cas, sos_cas = h.get_sos(energy_cas,a,g)
                                datac[g,a]['zcasscf',basisset, frocore] =sos_cas

                                h.append_dat('_contracted','a',atom,method,basisset,n,energy_cas,relenergy_cas,sos_cas)

                            energy = bagel.get_energy(lines, method) 
                            relenergy, sos = h.get_sos(energy,a,g)
                            datac[g,a][method, basisset,frocore] =sos

                            h.append_dat('_contracted','a',atom,method,basisset,n,energy,relenergy,sos)
        
    return datac

def get_error(data):

    group = [0,1,2,3,4]
    period = [2,3,4,5]
    basisset= ['dz','tz','qz','fz']
    method = ['zcasscf','caspt2','mrci']
    frozencore = ['fc','nfc']
    
    abs_error, perc_error =h.error(period,group,basisset,method,frozencore,data)
    return abs_error, perc_error

def get_error_contracted(data):
    group = [0,1,2,3,4]
    period = [2,3,4]
    basisset= ['dz','tz','qz','fz']
    method = ['zcasscf','caspt2','mrci']
    frozencore = ['fc','nfc']

    abs_error, perc_error =h.error(period,group,basisset,method,frozencore,data)
    return abs_error, perc_error

def get_data_F(btype,con):

    col = [[2],[4]]
    row = [['zcasscf','caspt2'],['dz','tz','qz','fz'],['fc','nfc']]
    cols = pd.MultiIndex.from_product(col, names = ['period','group'])
    rows = pd.MultiIndex.from_product(row, names = ['methods','basisset','frozencore'])

    data = pd.DataFrame(np.zeros((16,1)), index = rows, columns = cols).sort_index().sort_index(axis=1) #np.zeros is row by columns

    methods = ['zcasscf','caspt2']
    group = [2]
    basissets = ['dz','tz','qz','fz']
    ncore = [0,1]
    a = 4

    for g in group:
        for basisset in basissets:
            for n in ncore:
                for met in methods:
                    frocore = 'fc'
                    if n==0:
                        frocore = 'nfc'
                    path = '{}/{}/{}/{}/'.format(btype,con,g, basisset) 
                    if g == 2:
                        path += 'ncore' + str(n) + '/'
                        path += 'output.dat'
                        #print(path)
                    if os.path.isfile(path) == True:
                        with open(path, 'r') as f:
                            lines = f.readlines()
                    
                    energy = bagel.get_energy(lines, method) 
                    relenergy, sos = h.get_sos(energy,a,g)
                    datac[g,a][method, basisset,frocore] =sos

def get_error_F(data):
    group = [4]
    period = [2]
    basisset= ['dz','tz','qz','fz']
    method = ['zcasscf','caspt2']
    frozencore = ['fc','nfc']
    abs_error, perc_error =h.error(period,group,basisset,method,frozencore,data)
    return abs_error, perc_error

if __name__=='__main__':
    dat = get_data()
    datac = get_data_contracted()
    get_data_aux()
    get_error(dat)
    get_error_contracted(datac)
