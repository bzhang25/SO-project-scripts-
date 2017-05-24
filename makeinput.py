import sys 
import os
import subprocess 
import shutil as sh 


root = os.getcwd() 

template = """{ "bagel" : [
{
  "title" : "molecule",
  "symmetry" : "C1",
  "basis" : "%s",
  "df_basis" : "%s",
  "angstrom" : true,
  "geometry" : [ 
            { "atom": "%s", "xyz":[ 0.000,   0.000,   0.000]}
  ]
},

{
    "title"     :"zcasscf",
    "state"     :%s,
    "nact_cas"  :4,
    "nclosed"   :%d,
    "thresh" : 1.0e-10,
    "only_electrons"    :false,
    "finite_nucleus"    :true,
    "breit" : true,
    "gaunt" : true,
    "maxiter" : 1000
},

{   "title"     : "relsmith",
    "method" : "%s",
    "ncore" : %d
} 
]}"""

methods = ['caspt2', 'mrci']
group = [3, 4, 5]
for g in group:
    if g == 2:
        nclosed = 1        
        basissets = ['dz','tz','qz','fz']
        atoms = ['B','C','N','O','F']
        n = [0,1]
    elif g == 3:
        nclosed = 5
        basissets = ['dz','tz','qz']
        atoms = ['Al','Si','P','S','Cl']
        n = [5]
    elif g == 4:
        nclosed = 14
        basissets = ['dz','tz','qz']
        atoms = ['Ga','Ge','As','Se','Br']
        n = [14]
    elif g == 5:
        nclosed = 23
        basissets = ['tz','qz']
        atoms = ['In','Sn','Sb','Te','I']
        n = [23]
    for basisset in basissets:
        for a, atom in enumerate(atoms):
            for method in methods:
                for ncore in n:
                    if a == 0 or a == 4:
                        state = '[0,3]'
                    elif a == 1 or a == 3:
                        state = '[0,0,3]'
                    else:
                        state = '[0,8,0,1]' 
                    path = '{}/{}/{}/{}/'.format(g, basisset, atom, method)
                    if g == 2:
                        path += 'ncore' + str(ncore) + '/'
                    os.makedirs(path, exist_ok=True)
                    
                    bs = basisset + '.json'
                    fbs = basisset + '_jkfit.json'

                    with open(path + 'input.json', 'w') as f: 
                        f.write(template % (bs, fbs, atom, state, nclosed, method, ncore))
                    
                    sh.copy(bs,path)
                    sh.copy(fbs,path)
                    script = 'bagel6.sh'
                    if method == 'caspt2':
                        script = 'bagel4.sh'
                    elif method == 'mrci' and basisset == 'dz' and g != 5:
                        script = 'bagel4.sh'
                    elif g == 2 and method == 'mrci' and basisset == 'fz':
                        script = 'bagel5.sh'
                    
                    sh.copy(script, path)
                    os.chdir(path)
                    print(os.getcwd())
                    subprocess.check_call('qsub ' + script,shell=True)
                    os.chdir(root) 
