import sys 
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import get_energies

#defining graphing colors
red = '#e41a1c'
blue = '#132bb2'
green = '#58b71d'
purple = '#984ea3'
orange = '#ff9d00'
yellow = '#f2ea0e'

sos_list = [[15.287, 16.41671, 19224.464, 158.265, 404.141],
            [112.061,77.112,11361.02,396.055,882.35],
            [826.19,557.1341,10592.666,1989.497,3685.24],
            [2212.598,1691.806,8512.125,4706.5,7603.15]]

atom_label = [['Boron','Carbon','Nitrogen','Oxygen','Fluorine'],
               ['Aluminium','Silicon','Phosphorus','Sulfur','Chlorine'],
               ['Gallium','Germanium','Arsenic','Selenium','Bromine'],
               ['Indium','Tin','Antimony','Tellurium','Iodine']]

idx = pd.IndexSlice
Labels = [['Period 2','Period 3','Period 4', 'Period 5'],['Boron Group','Carbon Group','Pnictogens','Chalcogens','Halogens'],['CASSCF','CASPT2','MR-CISD+Q'],['DZ','TZ','QZ','5Z'],['all electron','No Frozen Core']]
variable = [[2],[0,1,2,3,4],['zcasscf','caspt2','mrci'],['dz','tz','qz','fz'],['fc','nfc']]
yc = []
y=[]
#plot_graph plots individual plots for each atom
def plot_graph(abserr, abserrc,percerr,percerrc,per,atomnum,atom):
    fig,ax = plt.subplots()
    for var0 in variable[4]:
        for var in variable[2]: 
            y.append(make_y(abserr, per,atomnum,var,variable[3],var0,'basisset'))
            #yc.append(make_y(abserrc, per,atomnum,var,variable[3],var0,'basisset'))
    x = np.arange(len(variable[3]))
    ticks = Labels[3]

    plt.xticks(x, ticks)
    ax.plot(x,y[0],'-o',label=Labels[2][0],color=red)
    ax.plot(x,y[1],'--o',label ='',color=green)
    ax.plot(x,y[2],'--o',label ='',color=blue)
    ax.plot(x,y[4],'-o',label =Labels[2][1],color=green)
    ax.plot(x,y[5],'-o',label =Labels[2][2], color=blue)
    #ax.plot(x,yc[0],'-mo',label=Labels[2][0]+ ' contracted')
    #ax.plot(x,yc[1],'--co',label ='')
    #ax.plot(x,yc[2],':yo',label =Labels[2][2]+ ' contracted')
    #ax.plot(x,yc[4],'-co',label =Labels[2][1]+ ' contracted')
    #ax.plot(x,yc[5],':yo',label ='')
    ax.plot(x,np.ones(4),'k-',label ='all electron')
    ax.plot(x,np.ones(4),'k--',label='frozen core')
    legend = ax.legend(loc = 'upper left',frameon=False)
    #plt.ylim(ymax=0)
    #if atomnum ==0:
    #    plt.ylim(ymax=0,ymin=-3.5)
    #elif atomnum ==1:
    #    plt.ylim(ymax=0,ymin=-3.5)
    #lif atomnum ==3:
     #   plt.ylim(ymax=0,ymin=-20)
    #lif atomnum ==4:
     #   plt.ylim(ymax=0,ymin=-50)
    ax.set_xlabel('Basis Set',fontsize=15)
    ax.text(2,-2.5,'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_exp[0][0]))
    ax.set_ylabel('Absolute Splitting Error (cm$^{-1}$)',fontsize=15)
    ax.set_title(atom,fontsize=20)
    plt.show()

#plots panels by period, shows contracted vs. uncontracted
def plot_graph_0(abserr,abserrc, period,atomlab,fc):

    var= ['dz','tz','qz']

    for var1 in variable[1]: 
        for var3 in variable[2]: 
            if period ==2:
                y.append(make_y(abserr, period,var1,var3,variable[3],fc,'basisset'))
                yc.append(make_y(abserrc, period,var1,var3,variable[3],fc,'basisset'))
            else: 
                y.append(make_y(abserr, period,var1,var3,var,fc,'basisset'))
                yc.append(make_y(abserrc, period,var1,var3,var,fc,'basisset'))
     
    fig,((ax0,ax1),(ax3,ax4)) = plt.subplots(2,2,sharex=True,sharey=False)
    
    ticks = ['DZ','TZ','QZ'] 
    x = np.arange(len(ticks))
    if period ==2:
        x = np.arange(len(variable[3]))
        ticks = Labels[3]
    plt.xticks(x, ticks)

    l1,=ax0.plot(x,y[0],'-o',label=Labels[2][0],color=red)
    l2,=ax0.plot(x,y[1],'-o',label =Labels[2][1],color=green)
    l3,=ax0.plot(x,y[2],'-o',label =Labels[2][2], color=blue)
    ax0.plot(x,yc[0],':o',label ='',color=red)
    ax0.plot(x,yc[1],':o',label ='',color=green)
    ax0.plot(x,yc[2],':o',label ='', color=blue)    

    ax1.plot(x,y[3],'-o',label ='',color=red)
    ax1.plot(x,y[4],'-o',label ='',color=green)
    ax1.plot(x,y[5],'-o',label ='',color=blue)

    ax1.plot(x,yc[3], ':o',label ='',color=red)
    ax1.plot(x,yc[4],':o',label ='',color=green)
    ax1.plot(x,yc[5],':o',label ='',color=blue)

    #ax2.plot(x,y[6],'-o',label ='',color=red)
    #ax2.plot(x,y[7],'-o',label ='',color=green)
    #ax2.plot(x,y[8],'-o',label ='',color=blue)

    #ax2.plot(x,yc[6], ':o',label ='',color=red)
    #ax2.plot(x,yc[7],':o',label ='',color=green)
    #ax2.plot(x,yc[8],':o',label ='',color=blue)

    ax3.plot(x,y[9],'-o',label ='',color=red)
    ax3.plot(x,y[10],'-o',label ='',color=green)
    ax3.plot(x,y[11],'-o',label ='',color=blue)

    ax3.plot(x,yc[9],':o',label ='',color=red)
    ax3.plot(x,yc[10],':o',label ='',color=green)
    ax3.plot(x,yc[11],':o',label ='',color=blue)

    ax4.plot(x,y[12],'-o',label ='',color=red)
    ax4.plot(x,y[13],'-o',label ='',color=green)
    ax4.plot(x,y[14],'-o',label ='',color=blue)

    ax4.plot(x,yc[12],':o',label ='',color=red)
    ax4.plot(x,yc[13],':o',label ='',color=green)
    ax4.plot(x,yc[14],':o',label ='',color=blue)

    ax0.set_ylim(ymax=0)
    ax1.set_ylim(ymax=0)
    if period ==2:
        ax0.set_ylim(ymax=0,ymin=-3.1)
        ax1.set_ylim(ymax=0,ymin=-3.1)
        ax3.set_ylim(ymax=0,ymin=-25)
        ax4.set_ylim(ymax=0,ymin=-50)

#    ax.set_xlabel('Basis Set',fontsize=15)
    l4, = ax0.plot(x,np.ones(len(ticks))*100,'k-',label ='uncontracted')
    l5,=ax0.plot(x,np.ones(len(ticks))*100,'k:',label='contracted')
    
    hor = [1.5,1,1] 
    place = [[-2.7,-2.7,0,-23,-45],[-25,-13,0,-60,-85],[-225,-140,0,-500,-750]]
    ax0.text(hor[atomlab],place[atomlab][0],'Exp. Splitting: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][0]))
    ax1.text(hor[atomlab],place[atomlab][1],'Exp. Splitting: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][1]))
#    ax2.text(hor[atomlab],place[atomlab][2],'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][2]))
    ax3.text(hor[atomlab],place[atomlab][3],'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][3]))
    ax4.text(hor[atomlab],place[atomlab][4],'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][4]))

    ax0.set_title(atom_label[atomlab][0])
    ax1.set_title(atom_label[atomlab][1])
  #  ax2.set_title(atom_label[atomlab][2])
    ax3.set_title(atom_label[atomlab][3])
    ax4.set_title(atom_label[atomlab][4])
    #plt.legend(handles=[l1,l4,l2,l5,l3],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=3)
    plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=5)
    title = 'Absolute Splitting Error at Various Basis Sets' 
    fig.text(0.07,0.5,'Absolute Splitting Error (cm$^{-1}$)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
    #plt.suptitle(title ,fontsize=20)
    plt.show()

#plots panels by period, shows frozen core vs. no frozen core
def plot_graph_1(abserr, percerr,period,atomlab):
    Labels = [['Period 2','Period 3','Period 4', 'Period 5'],['Boron Group','Carbon Group','Pnictogens','Chalcogens','Halogens'],['CASSCF','CASPT2','MR-CISD+Q'],['DZ','TZ','QZ','5Z'],['all electron','No Frozen Core']]
    variable = [[2],[0,1,2,3,4],['zcasscf','caspt2','mrci'],['dz','tz','qz','fz'],['fc','nfc']]
    for var1 in variable[1]: 
        for var2 in variable[4]:
            for var3 in variable[2]: 
                print(var1,var2,var3)
                y.append(make_y(abserr, period,var1,var3,variable[3],var2,'basisset'))

    fig,((ax0,ax1),(ax3,ax4)) = plt.subplots(2,2,sharex=True,sharey=False)

    x = np.arange(len(variable[3]))
    ticks = Labels[3]
    plt.xticks(x, ticks)

    l1,=ax0.plot(x,y[0],'-o',label=Labels[2][0],color=red)
    ax0.plot(x,y[1],'--o',label ='',color=green)
    ax0.plot(x,y[2],'--o',label ='',color=blue)
    l2,=ax0.plot(x,y[4],'-o',label =Labels[2][1],color=green)
    l3,=ax0.plot(x,y[5],'-o',label =Labels[2][2], color=blue)

    ax1.plot(x,y[6],'-o',label ='',color=red)
    ax1.plot(x,y[7],'--o',label ='',color=green)
    ax1.plot(x,y[8],'--o',label ='',color=blue)
    ax1.plot(x,y[10],'-o',label ='',color=green)
    ax1.plot(x,y[11],'-o',label ='',color=blue)

    #ax2.plot(x,y[12],'-o',label ='',color=red)
    #ax2.plot(x,y[13],'--o',label ='',color=blue)
    #ax2.plot(x,y[14],'--o',label ='',color=green)
    #ax2.plot(x,y[16],'-o',label ='',color=blue)
    #ax2.plot(x,y[17],'-o',label ='',color=green)

    ax3.plot(x,y[18],'-o',label ='',color=red)
    ax3.plot(x,y[19],'--o',label ='',color=green)
    ax3.plot(x,y[20],'--o',label ='',color=blue)
    ax3.plot(x,y[22],'-o',label ='' ,color=green)
    ax3.plot(x,y[23],'-o',label ='' ,color=blue)

    ax4.plot(x,y[24],'-o',label ='',color=red)
    ax4.plot(x,y[25],'--o',label ='',color=green)
    ax4.plot(x,y[26],'--o',label ='',color=blue)
    ax4.plot(x,y[28],'-o',label ='' ,color=green)
    ax4.plot(x,y[29],'-o',label ='' ,color=blue)

    if period ==2:
        ax0.set_ylim(ymax=0,ymin=-3)
        ax1.set_ylim(ymax=0,ymin=-3)
        ax3.set_ylim(ymax=0,ymin=-18)
        ax4.set_ylim(ymax=0,ymin=-40)
#    ax.set_xlabel('Basis Set',fontsize=15)
#    plt.text(1.7,-3.0,'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_exp[per][atomnum]))
    l4, = ax0.plot(x,np.ones(4),'k-',label ='all electron')
    l5,=ax0.plot(x,np.ones(4),'k--',label='frozen core')


    ax0.text(1.5,-2.7,'Exp. Splitting: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][0]))
    ax1.text(1.5,-2.7,'Exp. Splitting: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][1]))
    #ax2.text(1.3,-2.5,'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][2]))
    ax3.text(1.5, -16,'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][3]))
    ax4.text(1.5, -35,'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][4]))

    ax0.set_title(atom_label[atomlab][0])
    ax1.set_title(atom_label[atomlab][1])
   # ax2.set_title(atom_label[atomlab][2])
    ax3.set_title(atom_label[atomlab][3])
    ax4.set_title(atom_label[atomlab][4])
    #plt.legend(handles=[l1,l4,l2,l5,l3],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=3)
    plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=5)
    #title = 'Absolute Splitting Error at Various Basis Sets' 
    fig.text(0.07,0.5,'Absolute Splitting Error (cm$^{-1}$)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
    #plt.suptitle(title ,fontsize=20)
    plt.show()

#plots individual atom graphs for period 3-5
def plot_graph_1_1(abserr,percerr,atomnum,atom):
    Labels = [['Period 2','Period 3','Period 4', 'Period 5'],['Boron Group','Carbon Group','Pnictogens','Chalcogens','Halogens'],['CASSCF','CASPT2','MR-CISD+Q'],['cc-pVDZ','cc-pVTZ','cc-pVQZ'],['all electron','No Frozen Core']]
    variable = [[2,3,4,5],[0,1,3,4],['zcasscf','caspt2','mrci'],['dz','tz','qz'],['fc','nfc']]
    fig,ax = plt.subplots()
    for var in variable[2]: 
        y.append(make_y(abserr, 3,atomnum,var,variable[3],'fc','basisset'))
    x = np.arange(len(variable[3]))
    ticks = Labels[3]
   # print(y[0])

    print(y[1])
    plt.xticks(x, ticks)
    ax.plot(x,y[0],'-ro',label=Labels[2][0])
    ax.plot(x,y[1],'-go',label =Labels[2][1])
    ax.plot(x,y[2],'-bo',label =Labels[2][2])
    legend = ax.legend(loc = 'upper left',frameon=False)
    
    ax.set_xlabel('Basis Set',fontsize=15)
    ax.set_ylabel('Absolute Splitting Error (cm$^{-1}$)',fontsize=15)
    ax.set_title(atom,fontsize=20)
    
#    l,=ax1.plot(x,dum,'k-',label ='cc-pVQZ')
#    l2,=ax1.plot(x,dum,'k--',label ='cc-pVTZ')
#    l3,= ax1.plot(x,dum,'k:',label ='cc-pVDZ')
#    ax1.set_title(Labels[1][0])
#    ax2.set_title(Labels[1][1])
#    ax3.set_title(Labels[1][3])
#    ax4.set_title(Labels[1][4])
#    plt.legend(handles=[l3,l2,l],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=3)

#    title = 'Relative Splitting Error at {}'.format(m)
#    fig.text(0.07,0.5,'Relative Splitting Error (%)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
#    plt.suptitle(title ,fontsize=20)
    plt.show()

#plots a comparison of all atoms split by groups for a particular method
def plot_graph_2(data,abserr, percerr,meth,m):
    Labels = [['Period 2','Period 3','Period 4', 'Period 5'],['Boron Group','Carbon Group','Pnictogens','Chalcogens','Halogens'],['CASSCF','CASPT2','MR-CISD+Q'],['cc-pVDZ','cc-pVTZ','cc-pVQZ','cc-pV5Z'],['all electron','No Frozen Core']]
    atoms = [['B','Al','Ga','In'],['C','Si','Ge','Sn'],['N','P','As','Sb'],['O','S','Se','Te'],['F','Cl','Br','I']]
    variable = [[2,3,4,5],[0,1,3,4],['zcasscf','caspt2','mrci'],['dz','tz','qz','fz'],['fc','nfc']]
    fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,sharex=False,sharey=True)
    
    lis = ['dz','tz','qz']
    dum=[-20,-20,-20,-20]
    for l in lis: 
        for var in variable[1]: 
            y.append(make_y(percerr, variable[0],var,meth,l,'fc','period'))
    print(y)
    x = np.arange(len(variable[0]))
    ax1.set_xticks(x)
    ax2.set_xticks(x)
    ax3.set_xticks(x)
    ax4.set_xticks(x)
    ax1.set_xticklabels(atoms[0])
    ax2.set_xticklabels(atoms[1])
    ax3.set_xticklabels(atoms[3])
    ax4.set_xticklabels(atoms[4])

    ax1.plot(x,y[0],':o',label =Labels[3][0],color=red)
    ax2.plot(x,y[1],':o',label =Labels[3][0],color=orange)
    ax3.plot(x,y[2],':o',label =Labels[3][0],color=green)
    ax4.plot(x,y[3],':o',label =Labels[3][0],color=blue)
    ax1.plot(x,y[4],'--o',label =Labels[3][1],color=red)
    ax2.plot(x,y[5],'--o',label =Labels[3][1],color=orange)
    ax3.plot(x,y[6],'--o',label =Labels[3][1],color=green)
    ax4.plot(x,y[7],'--o',label =Labels[3][1],color=blue)
    ax1.plot(x,y[8],'-o' ,label =Labels[3][2],color=red)
    ax2.plot(x,y[9],'-o' ,label =Labels[3][2],color=orange)
    ax3.plot(x,y[10],'-o',label =Labels[3][2],color=green)
    ax4.plot(x,y[11],'-o',label =Labels[3][2],color=blue)

    l,=ax1.plot(x,dum,'k-',label ='cc-pVQZ')
    l2,=ax1.plot(x,dum,'k--',label ='cc-pVTZ')
    l3,= ax1.plot(x,dum,'k:',label ='cc-pVDZ')
    ax1.set_title(Labels[1][0])
    ax2.set_title(Labels[1][1])
    ax3.set_title(Labels[1][3])
    ax4.set_title(Labels[1][4])
    plt.legend(handles=[l3,l2,l],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=3)

    title = 'Relative Splitting Error at {}'.format(m)
    fig.text(0.07,0.5,'Relative Splitting Error (%)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
    plt.suptitle(title ,fontsize=20)
    plt.show()

def make_y(matrix,period,group,method,basisset,frozencore,var):
    y = []

    if var == 'period': 
        for per in period:
            y.append(matrix[per,group][method,basisset,frozencore])
        return y
    if var == 'group': 
        for grp in group:
            y.append(matrix[period,grp][method,basisset,frozencore])
        return y
    if var == 'method': 
        for met in method:
            y.append(matrix[period,group][met,basisset,frozencore])
        return y
    if var == 'basisset': 
        for basis in basisset:
            y.append(matrix[period,group][method,basis,frozencore])
 #       print(y)
        return y


data = get_energies.get_data()
datac = get_energies.get_data_contracted()
abso, perc = get_energies.get_error(data)

absoc,percc = get_energies.get_error_contracted(datac)
#plot_graph_2(data,abso, perc,'caspt2','CASPT2')
#plot_graph_2(data,abso, perc,'zcasscf','CASSCF')
plot_graph_0(abso,absoc,4,2,'fc')
#plot_graph_1(abso,perc,3,1)

#plot_graph_1_1(abso,perc,0,'Aluminium')
#plot_graph_1_1(abso,perc,1,'Silicon')
#plot_graph_1_1(abso,perc,3,'Sulfur')
#plot_graph_1_1(abso,perc,4,'Chlorine')


#plot_graph_1_1(abso,perc,0,'Gallium')
#plot_graph_1_1(abso,perc,1,'Germanium')
#plot_graph_1_1(abso,perc,3,'Selenium')
#plot_graph_1_1(abso,perc,4,'Bromine')
