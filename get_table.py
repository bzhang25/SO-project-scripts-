import sys 
import os.path
import pandas as pd
import numpy as np
import get_energies
import scipy

atoms = ['B','C','N','O','F']
method = ['zcasscf','caspt2','mrci']
jkfit = ['dz','fz']

idx = pd.IndexSlice

def get_table(data,data_aux,outfile):
    
    table_header = """
    \\begin{table} [!htbp]
    \\caption{caption}
    \\centering
    \\scalebox{1.0}{
    \\begin{tabular}{c c c c c c c}
    \\hline
    \\\\
     & \multicolumn{2}{c}{CASSCF} & \multicolumn{2}{c}{CASPT2} & \multicolumn{2}{c}{MR-CISD+Q}\\\\ [0.5ex]
    \\hline
        Atom & dz & fz & dz & fz & dz & fz\\\\ [0.5ex]
    \\hline
    \\\\ """

    line = '{:3}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f} \\\\ [1ex]'

    table_end = """
    \\hline
    \\end{tabular}
    }
    \\end{table}"""

    out = ''
    out += table_header
    for a, atom in enumerate(atoms):
        y = []
        for met in method:
            for aux in jkfit:
                if aux == 'dz':
                    y.append(data[2,a][met,'dz','fc'])               
                if aux == 'fz':
                    y.append(data_aux[2,a][met,'dz','fc'])               
        for i,num in enumerate(y):
            if num == 0:
                y[i] = np.nan
        #print(y)
        out += line.format(atom, y[0],y[1],y[2],y[3],y[4],y[5])
    out += table_end

    open(outfile, 'w').write(out)
    
    return out

def get_table_2(data,data_aux,outfile):
    
    table_header = """
    \\begin{table} [!htbp]
    \\caption{caption}
    \\centering
    \\scalebox{1.0}{
    \\begin{tabular}{c c c c}
    \\hline
    \\\\
    Atom & CASSCF & CASPT2 & MR-CISD+Q\\\\ [0.5ex]
    %\\hline
    %    Atom & dz & fz & dz & fz & dz & fz\\\\ [0.5ex]
    \\hline
    \\\\ """

    line = '{:3}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f} \\\\ [1ex]'

    table_end = """
    \\hline
    \\end{tabular}
    }
    \\end{table}"""

    out = ''
    out += table_header
    for a, atom in enumerate(atoms):
        y = []
        for met in method:
            for aux in jkfit:
                if aux == 'dz':
                    y.append(data[2,a][met,'dz','fc'])               
                if aux == 'fz':
                    y.append(data_aux[2,a][met,'dz','fc'])               
        for i,num in enumerate(y):
            if num == 0:
                y[i] = np.nan
        #print(y)
        out += line.format(atom, y[1]-y[0],y[3]-y[2],y[4]-y[5])
    out += table_end

    open(outfile, 'a').write(out)
    
    return out
def get_table_final(data,data_aux,outfile):

    table_header = """
    \\begin{table} [!htbp]
    \\caption{caption}\label{table:SOS}
    \\centering \\scalebox{1.0}{ \\begin{tabular}{c c c c c c c} \\hline
    \\\\
     & \multicolumn{2}{c}{CASSCF} & \multicolumn{2}{c}{CASPT2} & \multicolumn{2}{c}{MR-CISD+Q}\\\\ [0.5ex]
    \\hline
        Atom & $\Delta$ & $\%\Delta$ & $\Delta$ & $\%\Delta$ & $\Delta$ & $\%\Delta$\\\\ [0.5ex]
    \\hline
    \\\\ """

    line = '{:3}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f}&{: > 5.5f} \\\\ [1ex]'
    table_end = """
    \\hline
    \\end{tabular}
    }
    \\end{table}"""

    out = ''
    out += table_header
    for a, atom in enumerate(atoms):
        y = []
        for met in method:
            for aux in jkfit:
                if aux == 'dz':
                    y.append(data[2,a][met,'dz','fc'])               
                if aux == 'fz':
                    y.append(data_aux[2,a][met,'dz','fc'])               
        for i,num in enumerate(y):
            if num == 0:
                y[i] = np.nan
   #     print(y)
        y_final = [(y[1]-y[0]),((y[1]-y[0])/y[0])*100,(y[3]-y[2]),((y[3]-y[2])/y[2])*100,(y[5]-y[4]),((y[5]-y[4])/y[4])*100]
    #    print(y_final)
        out += line.format(atom, y_final[0],y_final[1],y_final[2],y_final[3],y_final[4],y_final[5])
    out += table_end

    open(outfile, 'a').write(out)
    
    return out
if __name__=='__main__':
    data = get_energies.get_data()
    data_aux = get_energies.get_data_aux()
    print(data_aux[2,0]['zcasscf','dz','fc'])               
    open('table.tex', 'w').write('')
   # get_table(data,data_aux,'table.tex')
    #get_table_2(data,data_aux,'table.tex')
    get_table_final(data,data_aux,'table.tex')
    
