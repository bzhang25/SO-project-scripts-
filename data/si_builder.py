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

def make_si(infile,infile2,outfile,group): 
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
            for a, atom in enumerate(atoms):
                for n in ncore:           
                    #print(atom, basisset,n)
                    table = make_table(infile,infile2, atom,a, basisset, n,g)   
                    out += table
    out += si_end

    open(outfile,'w').write(out)

def make_table(filename, relenergy,atom,a,bs,ncore,g):

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
    line2 = '{:25}&{: > 7.2f}&{: > 7.2f}&{: > 7.2f} \\\\ [1ex]'

    hline = '\\hline \\\\'

    table_end = """
    \\hline
    \\end{tabular}
    }
    \\end{table}"""

    out = ''
#getting absolute energies 
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

    out += hline

#getting splittings 
    with open(relenergy) as f:
        splittings = f.readlines()

    scf_split, pt2_split, mrci_split = energies(splittings,atom,bs,ncore)

    if len(scf) == 0:
        out += line2.format(' Splittings:',np.nan,np.nan,np.nan)
    elif len(scf) !=0 and len(pt2)==0:
        if a == 0:
            out += line2.format('$^2$P$_{1/2}$', float(scf_split[0]),np.nan,np.nan)
            out += line2.format('$^2$P$_{3/2}$', float(scf_split[2]),np.nan,np.nan)
        elif a == 4:
            out += line2.format('$^2$P$_{3/2}$', float(scf_split[0]),np.nan,np.nan)
            out += line2.format('$^2$P$_{1/2}$', float(scf_split[4]),np.nan,np.nan)
        if a == 1:
            out += line2.format('$^3$P$_0$', float(scf_split[0]),np.nan,np.nan)
            out += line2.format('$^3$P$_1$', float(scf_split[1]),np.nan,np.nan)
            out += line2.format('$^3$P$_2$', float(scf_split[4]),np.nan,np.nan)
        if a == 3:
            out += line2.format('$^3$P$_2$', float(scf_split[0]),np.nan,np.nan)
            out += line2.format('$^3$P$_1$', float(scf_split[5]),np.nan,np.nan)
            out += line2.format('$^3$P$_0$', float(scf_split[8]),np.nan,np.nan)
        if a == 2:
            out += line2.format('$^4$S$_{3/2}$', float(scf_split[0]),np.nan,np.nan)
            if g==2:
                out += line2.format('$^2$D$_{5/2}$', float(scf_split[4]), np.nan, np.nan)
                out += line2.format('$^2$D$_{3/2}$', float(scf_split[10]),np.nan,np.nan)
            else:
                out += line2.format('$^2$D$_{3/2}$', float(scf_split[4]),np.nan,np.nan)
                out += line2.format('$^2$D$_{5/2}$', float(scf_split[8]),np.nan,np.nan)
    elif len(pt2) != 0 and len(mrci)==0:
        if a == 0:
            out += line2.format('$^2$P$_{1/2}$', float(scf_split[0]),float(pt2_split[0]),np.nan)
            out += line2.format('$^2$P$_{3/2}$', float(scf_split[2]),float(pt2_split[2]),np.nan)
        elif a == 4:
            out += line2.format('$^2$P$_{3/2}$', float(scf_split[0]),float(pt2_split[0]),np.nan)
            out += line2.format('$^2$P$_{1/2}$', float(scf_split[4]),float(pt2_split[4]),np.nan)
        if a == 1:
            out += line2.format('$^3$P$_0$', float(scf_split[0]),float(pt2_split[0]),np.nan)
            out += line2.format('$^3$P$_1$', float(scf_split[1]),float(pt2_split[1]),np.nan)
            out += line2.format('$^3$P$_2$', float(scf_split[4]),float(pt2_split[4]),np.nan)
        if a == 3:
            out += line2.format('$^3$P$_2$', float(scf_split[0]),float(pt2_split[0]),np.nan)
            out += line2.format('$^3$P$_1$', float(scf_split[5]),float(pt2_split[5]),np.nan)
            out += line2.format('$^3$P$_0$', float(scf_split[8]),float(pt2_split[8]),np.nan)
        if a == 2:
            out += line2.format('$^4$S$_{3/2}$', float(scf_split[0]),float(pt2_split[0]),np.nan)
            if g==2:
                out += line2.format('$^2$D$_{5/2}$', float(scf_split[4]), float(pt2_split[4]) , np.nan)
                out += line2.format('$^2$D$_{3/2}$', float(scf_split[10]),float(pt2_split[10]),np.nan)
            else:
                out += line2.format('$^2$D$_{3/2}$', float(scf_split[4]),float(pt2_split[4]),np.nan)
                out += line2.format('$^2$D$_{5/2}$', float(scf_split[8]),float(pt2_split[8]),np.nan)
    else:
        if a == 0:
            out += line2.format('$^2$P$_{1/2}$', float(scf_split[0]),float(pt2_split[0]),float(mrci_split[0]))
            out += line2.format('$^2$P$_{3/2}$', float(scf_split[2]),float(pt2_split[2]),float(mrci_split[2]))
        elif a == 4:
            out += line2.format('$^2$P$_{3/2}$', float(scf_split[0]),float(pt2_split[0]),float(mrci_split[0]))
            out += line2.format('$^2$P$_{1/2}$', float(scf_split[4]),float(pt2_split[4]),float(mrci_split[4]))
        if a == 1:
            out += line2.format('$^3$P$_0$', float(scf_split[0]),float(pt2_split[0]),float(mrci_split[0]))
            out += line2.format('$^3$P$_1$', float(scf_split[1]),float(pt2_split[1]),float(mrci_split[1]))
            out += line2.format('$^3$P$_2$', float(scf_split[4]),float(pt2_split[4]),float(mrci_split[4]))
        if a == 3:
            out += line2.format('$^3$P$_2$', float(scf_split[0]),float(pt2_split[0]),float(mrci_split[0]))
            out += line2.format('$^3$P$_1$', float(scf_split[5]),float(pt2_split[5]),float(mrci_split[5]))
            out += line2.format('$^3$P$_0$', float(scf_split[8]),float(pt2_split[8]),float(mrci_split[8]))
        if a == 2:
            out += line2.format('$^4$S$_{3/2}$', float(scf_split[0]),float(pt2_split[0]),float(mrci_split[0]))
            if g==2:
                out += line2.format('$^2$D$_{5/2}$', float(scf_split[4]),float(pt2_split[4]),float(mrci_split[4]))
                out += line2.format('$^2$D$_{3/2}$', float(scf_split[10]),float(pt2_split[10]),float(mrci_split[10]))
            else:
                out += line2.format('$^2$D$_{3/2}$', float(scf_split[4]),float(pt2_split[4]),float(mrci_split[4]))
                out += line2.format('$^2$D$_{5/2}$', float(scf_split[8]),float(pt2_split[8]),float(mrci_split[8])) 

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

make_si('energy.dat','relenergy.dat','si/sections/energy_uncontracted.tex',[2,3,4,5])
make_si('energy_contracted.dat','relenergy_contracted.dat','si/sections/energy_contracted.tex',[2,3,4])
