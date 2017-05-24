import re
import numpy as np
import ast
si_header = """
\\documentclass[../si.tex]{subfiles}
\\begin{document} """
si_end = '\\end{document}'


graph = """
\\begin{figure}[h!]
\\centering
\\includegraphics[width=.9\\linewidth]{%.pdf}
\\end{figure}"""

def make_si(infile,outfile,group): 
    out = ''
    out += si_header
    out +='\n'
    for g in group:
        if g == 2:
            basissets = ['dz','tz','qz','fz']
            atoms = ['B','C','N','O','F']
            ncore = [0,1]
        elif g == 3:
            basissets = ['dz','tz','qz']
            atoms = ['Al','Si','P','S','Cl']
            ncore = [5]
        elif g == 4:
            basissets = ['dz','tz','qz']
            atoms = ['Ga','Ge','As','Se','Br']
            ncore = [14]
        elif g == 5:
            basissets = ['tz','qz']
            atoms = ['In','Sn','Sb','Te','I']
            ncore = [23]
        for basisset in basissets:
            for atom in atoms:
                for n in ncore:           
                    #print(atom, basisset,n)
                    table = make_table(infile, atom, basisset, n)   
                    out += table
    out += si_end

    open(outfile,'w').write(out)

def make_table(filename,atom,bs,ncore):

    table_header = """
    \\begin{table} [!htbp]
    \\caption{%s at cc-pV%s freezing %d orbitals}
    \\centering
    \\scalebox{1.0}{
    \\begin{tabular}{c c c c}
    \\hline
    \\\\
    State & CASSCF & CASPT2 & MRCI\\\\ [0.5ex]
    \\hline
    \\\\ """

    line = '{:3}&{: > 7.5f}&{: > 7.5f}&{: > 7.5f} \\\\ [1ex]'

    table_end = """
    \\hline
    \\end{tabular}
    }
    \\end{table}"""

    out = ''

    with open(filename) as f:
        lines = f.readlines()
    if bs == 'fz':
        out += table_header %(atom,'5Z',ncore) 
    else:
        out += table_header %(atom,bs.upper(),ncore) 
    scf, pt2, mrci = energies(lines,atom,bs,ncore)
    for i,e in enumerate(scf):
        if len(scf) == 0:
            out += line.format(i+1,np.nan,np.nan,np.nan)
        elif len(scf) !=0 and len(pt2)==0:
            out += line.format(i+1,float(e),np.nan,np.nan)
        elif len(pt2) != 0 and len(mrci)==0:
            out += line.format(i+1,float(e),float(pt2[i]),np.nan)
        else:
            out += line.format(i+1,float(e),float(pt2[i]),float(mrci[i]))
                        
    out += table_end
    return out

def energies(lines,atom,bs,ncore):

    line = 'atom: {:2} method: {:7} bs: {} ncore:{:4}'
    casscf = line.format(atom, 'casscf', bs,ncore)
    caspt2 = line.format(atom, 'caspt2', bs,ncore)
    mrci =   line.format(atom, 'mrci', bs, ncore)
    scf = []
    pt2 = []
    ci = []

    for line in lines:
        if casscf == line[:42]:
            scf = ast.literal_eval(line[43:])
        if caspt2 == line[:42]:
            pt2 = ast.literal_eval(line[43:])
        if mrci == line[:42]:
            ci = ast.literal_eval(line[43:])

    return scf, pt2, ci
make_si('energy.dat','si/sections/energy_uncontracted.tex',[2,3,4,5])
make_si('energy_contracted.dat','si/sections/energy_contracted.tex',[2,3,4])
