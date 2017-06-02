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
    "only_electrons"    :false,
    "finite_nucleus"    :true,
    "breit" : true,
    "gaunt" : true,
    "maxiter" : 200
},

{   "title"     : "relsmith",
    "method" : "%s",
    "ncore" : %d
} 
]}"""

methods = ['caspt2']
basistype = ['aVXZ','aCVXZ','CVXZ']
contraction = ['contracted','uncontracted']
group = [2]
for btype in basistype:
    for con in contraction:
        for g in group:
            if g == 2:
                nclosed = 1        
                basissets = ['dz','tz','qz','fz']
                atoms = ['F']
                n = [0,1]
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
                            #path = '{}/{}/{}/{}/'.format(btype,con,g, basisset, atom, method) did this for F caspt2
                            path = '{}/{}/{}/{}/{}/{}/'.format(btype,con,g, basisset, atom, method)
                            if g == 2:
                                path += 'ncore' + str(ncore) + '/'
                            os.makedirs(path, exist_ok=True)
                           
                            bset = 'c' + basisset 
                            if btype == 'aCVXZ':
                                bset = 'ac' + basisset
                            if btype == 'aVXZ':
                                bset = 'aug_cc_' + basisset 

                            if con == 'uncontracted':
                                bset = 'u' + bset

                            bs = bset + '.json'
                            fbs = bset + '_jkfit.json'

                            with open(path + 'input.json', 'w') as f: 
                                f.write(template % (bs, fbs, atom, state, nclosed, method, ncore))

                            print(path) 

                            sh.copy(('basisset/'+bs),path)
                            sh.copy(('basisset/'+fbs),path)

                            script = 'bagel6.sh'
                            if method == 'caspt2' and basisset != 'fz':
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
