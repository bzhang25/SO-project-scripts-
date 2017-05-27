import sys 
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import get_energies
import scipy

#defining graphing colors
red = '#e41a1c'
blue = '#132bb2'
green = '#58b71d'
purple = '#984ea3'
orange = '#ff9d00'
yellow = '#f2ea0e'

sos_list = [[15.287, 16.41671, 8.713, 158.265, 404.141],
            [112.061,77.112,15.61,396.055,882.35],
            [826.19,557.1341,322.2,1989.497,3685.24],
            [2212.598,1691.806,1341.893,4706.5,7603.15]]

atom_label = [['Boron','Carbon','Nitrogen','Oxygen','Fluorine'],
               ['Aluminium','Silicon','Phosphorus','Sulfur','Chlorine'],
               ['Gallium','Germanium','Arsenic','Selenium','Bromine'],
               ['Indium','Tin','Antimony','Tellurium','Iodine']]

atoms = [['B','Al','Ga','In'],['C','Si','Ge','Sn'],['N','P','As','Sb'],['O','S','Se','Te'],['F','Cl','Br','I']]

idx = pd.IndexSlice
Labels = [['Period 2','Period 3','Period 4', 'Period 5'],['Boron Group','Carbon Group','Pnictogens','Chalcogens','Halogens'],['CASSCF','CASPT2','MR-CISD+Q'],['DZ','TZ','QZ','5Z'],['all electron','No Frozen Core']]
variable = [[2,3,4,5],[0,1,2,3,4],['zcasscf','caspt2','mrci'],['dz','tz','qz','fz'],['fc','nfc']]
yc = []
y=[]

#plots panels by period, shows contracted vs. uncontracted
def by_contraction(abserr,abserrc, period,atomlab,fc):

    var= ['dz','tz','qz']

    for var1 in variable[1]: 
        for var3 in variable[2]: 
            if period ==2:
                y.append(make_y(abserr, period,var1,var3,variable[3],fc,'basisset'))
                yc.append(make_y(abserrc, period,var1,var3,variable[3],fc,'basisset'))
            else: 
                y.append(make_y(abserr, period,var1,var3,var,fc,'basisset'))
                yc.append(make_y(abserrc, period,var1,var3,var,fc,'basisset'))
     
    fig,((ax0,ax1,ax2),(ax3,ax4,ax5)) = plt.subplots(2,3,sharex=True,sharey=False)
    
    fig.delaxes(ax5)
    ticks = ['DZ','TZ','QZ'] 
    x = np.arange(len(ticks))
    if period ==2:
        x = np.arange(len(variable[3]))
        ticks = Labels[3]
    plt.xticks(x, ticks)
    plt.setp(ax0.get_xticklabels(),visible=True)
    plt.setp(ax1.get_xticklabels(),visible=True)
    plt.setp(ax2.get_xticklabels(),visible=True)
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

    ax2.plot(x,y[6],'-o',label ='',color=red)
    ax2.plot(x,y[7],'-o',label ='',color=green)
    ax2.plot(x,y[8],'-o',label ='',color=blue)

    ax2.plot(x,yc[6], ':o',label ='',color=red)
    ax2.plot(x,yc[7],':o',label ='',color=green)
    ax2.plot(x,yc[8],':o',label ='',color=blue)

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
        ax2.set_ylim(ymin=0)
        ax3.set_ylim(ymax=0,ymin=-25)
        ax4.set_ylim(ymax=0,ymin=-50)

#    ax.set_xlabel('Basis Set',fontsize=15)
    l4, = ax0.plot(x,np.ones(len(ticks))*100,'k-',label ='uncontracted')
    l5,=ax0.plot(x,np.ones(len(ticks))*100,'k:',label='contracted')
    
    hor = [1.5,1,1] 
    place = [[-2.7,-2.7,0.5,-23,-45],[-25,-13,-5.3,-60,-85],[-225,-140,-115,-500,-700]]
    ax0.text(hor[atomlab],place[atomlab][0],'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][0]))
    ax1.text(hor[atomlab],place[atomlab][1],'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][1]))
    ax2.text(hor[atomlab],place[atomlab][2],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][2]))
    ax3.text(hor[atomlab],place[atomlab][3],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][3]))
    ax4.text(hor[atomlab],place[atomlab][4],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][4]))

    ax0.set_title(atom_label[atomlab][0])
    ax1.set_title(atom_label[atomlab][1])
    ax2.set_title(atom_label[atomlab][2])
    ax3.set_title(atom_label[atomlab][3])
    ax4.set_title(atom_label[atomlab][4])
    #plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=5)
    plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'lower right',frameon=False,bbox_to_anchor = (2.07,0.2),ncol=1)
    title = 'Absolute Splitting Error at Various Basis Sets' 
    fig.text(0.07,0.5,'Absolute Splitting Error (cm$^{-1}$)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
    #plt.suptitle(title ,fontsize=20)
    plt.show()

def by_basisset(abserr, percerr,period,atomlab):

    var= ['dz','tz','qz']
    if period==5:
        var= ['tz','qz']
    for var1 in variable[1]: 
        for var2 in variable[2]: 
            #    print(var1,var2,var3)
             y.append(make_y(abserr, period,var1,var2,var,'fc','basisset'))

    fig,((ax0,ax1,ax2),(ax3,ax4,ax5)) = plt.subplots(2,3,sharex=True,sharey=False)
    
    fig.delaxes(ax5)
    ticks = ['DZ','TZ','QZ'] 
    if period ==5:
        ticks = ['TZ','QZ'] 
    x = np.arange(len(ticks))

    plt.xticks(x, ticks)
    plt.setp(ax0.get_xticklabels(),visible=True)
    plt.setp(ax1.get_xticklabels(),visible=True)
    plt.setp(ax2.get_xticklabels(),visible=True)

    l1,=ax0.plot(x,y[0],'-o',label =Labels[2][0], color=red)
    l2,=ax0.plot(x,y[1],'-o',label =Labels[2][1], color=green)
    l3,=ax0.plot(x,y[2],'-o',label =Labels[2][2], color=blue)

    ax1.plot(x,y[3],'-o',label ='',color=red)
    ax1.plot(x,y[4],'-o',label ='',color=green)
    ax1.plot(x,y[5],'-o',label ='',color=blue)

    ax2.plot(x,y[6],'-o',label ='',color=red)
    ax2.plot(x,y[7],'-o',label ='',color=green)
    ax2.plot(x,y[8],'-o',label ='',color=blue)

    ax3.plot(x,y[9],'-o',label ='',color=red)
    ax3.plot(x,y[10],'-o',label ='',color=green)
    ax3.plot(x,y[11],'-o',label ='',color=blue)

    ax4.plot(x,y[12],'-o',label ='',color=red)
    ax4.plot(x,y[13],'-o',label ='',color=green)
    ax4.plot(x,y[14],'-o',label ='',color=blue)

    if period==3:
        ax0.set_ylim(ymax=0)
        ax1.set_ylim(ymax=0)
        ax2.set_ylim(ymax=0)
#        ax3.set_ylim(ymax=0,ymin=-18)
#        ax4.set_ylim(ymax=0,ymin=-40)
#    ax.set_xlabel('Basis Set',fontsize=15)
#    plt.text(1.7,-3.0,'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_exp[per][atomnum]))
    #l4, = ax0.plot(x,np.ones(4),'k-',label ='all electron')
    #l5,=ax0.plot(x,np.ones(4),'k--',label='frozen core')

    hor = [1.6,1,1,0.5] 
    place = [[-2.7,-2.7,0.5,-16,-35],[-12,-6,-4,-40,-10],[-130,-67,-80,-225,-125],[-130,-67,-80,-225,-125]]
    ax0.text(hor[atomlab],place[atomlab][0],'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][0]))
    ax1.text(hor[atomlab],place[atomlab][1],'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][1]))
    ax2.text(hor[atomlab],place[atomlab][2],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][2]))
    ax3.text(hor[atomlab],place[atomlab][3],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][3]))
    ax4.text(hor[atomlab],place[atomlab][4],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][4]))

    ax0.set_title(atom_label[atomlab][0])
    ax1.set_title(atom_label[atomlab][1])
    ax2.set_title(atom_label[atomlab][2])
    ax3.set_title(atom_label[atomlab][3])
    ax4.set_title(atom_label[atomlab][4])
    #plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=5)
    #title = 'Absolute Splitting Error at Various Basis Sets' 
    plt.legend(handles=[l1,l2,l3],loc = 'lower right',frameon=False,bbox_to_anchor = (2.07,0.2),ncol=1)
    fig.text(0.07,0.5,'Absolute Splitting Error (cm$^{-1}$)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
    #plt.suptitle(title ,fontsize=20)
    plt.show()

#plots panels by period, shows frozen core vs. no frozen core only for period 2
def by_basisset_per2(abserr, percerr,period,atomlab):

    for var1 in variable[1]: 
        for var2 in variable[4]:
            for var3 in variable[2]: 
                print(var1,var2,var3)
                y.append(make_y(abserr, period,var1,var3,variable[3],var2,'basisset'))

    fig,((ax0,ax1,ax2),(ax3,ax4,ax5)) = plt.subplots(2,3,sharex=True,sharey=False)
    
    fig.delaxes(ax5)

    x = np.arange(len(variable[3]))
    ticks = Labels[3]
    plt.xticks(x, ticks)

    plt.setp(ax0.get_xticklabels(),visible=True)
    plt.setp(ax1.get_xticklabels(),visible=True)
    plt.setp(ax2.get_xticklabels(),visible=True)

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

    ax2.plot(x,y[12],'-o',label ='',color=red)
    ax2.plot(x,y[13],'--o',label ='',color=green)
    ax2.plot(x,y[14],'--o',label ='',color=blue)
    ax2.plot(x,y[16],'-o',label ='',color=green)
    ax2.plot(x,y[17],'-o',label ='',color=blue)

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

    ax0.set_ylim(ymax=0,ymin=-3)
    ax1.set_ylim(ymax=0,ymin=-3)
    ax2.set_ylim(ymin=0)
    ax3.set_ylim(ymax=0,ymin=-18)
    ax4.set_ylim(ymax=0,ymin=-40)
#    ax.set_xlabel('Basis Set',fontsize=15)
#    plt.text(1.7,-3.0,'Exp. Splitting: {:>6.1f} cm$^{{-1}}$'.format(sos_exp[per][atomnum]))
    l4, = ax0.plot(x,np.ones(4),'k-',label ='all electron')
    l5,=ax0.plot(x,np.ones(4),'k--',label='frozen core')

    hor = [1.6,1,1] 
    place = [[-2.7,-2.7,0.5,-16,-35],[-25,-13,0,-60,-85],[-225,-140,0,-500,-750]]
    ax0.text(hor[atomlab],place[atomlab][0],'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][0]))
    ax1.text(hor[atomlab],place[atomlab][1],'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][1]))
    ax2.text(hor[atomlab],place[atomlab][2],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][2]))
    ax3.text(hor[atomlab],place[atomlab][3],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][3]))
    ax4.text(hor[atomlab],place[atomlab][4],'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][4]))

    ax0.set_title(atom_label[atomlab][0])
    ax1.set_title(atom_label[atomlab][1])
    ax2.set_title(atom_label[atomlab][2])
    ax3.set_title(atom_label[atomlab][3])
    ax4.set_title(atom_label[atomlab][4])
    #plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.1,-0.1),ncol=5)
    #title = 'Absolute Splitting Error at Various Basis Sets' 
    plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'lower right',frameon=False,bbox_to_anchor = (2.07,0.2),ncol=1)
    fig.text(0.07,0.5,'Absolute Splitting Error (cm$^{-1}$)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
    #plt.suptitle(title ,fontsize=20)
    plt.show()

#plots a comparison of all atoms split by groups for a particular method
def by_method(percerr,meth,m):

    fig,((ax1,ax2,axN),(ax3,ax4,ax5)) = plt.subplots(2,3,sharex=False,sharey=False)
    
    fig.delaxes(ax5)
    lis = ['dz','tz','qz']
    for l in lis: 
        for var in variable[1]: 
            y.append(make_y(percerr, variable[0],var,meth,l,'fc','period'))

    x = np.arange(len(variable[0]))
    ax1.set_xticks(x)
    ax2.set_xticks(x)
    ax3.set_xticks(x)
    ax4.set_xticks(x)
    axN.set_xticks(x)
    ax1.set_xticklabels(atoms[0])
    ax2.set_xticklabels(atoms[1])
    ax3.set_xticklabels(atoms[3])
    ax4.set_xticklabels(atoms[4])
    axN.set_xticklabels(atoms[2])

    ax1.plot(x,y[0],':o',label =Labels[3][0],color=red)
    ax2.plot(x,y[1],':o',label =Labels[3][0],color=orange)
    axN.plot(x,y[2],':o',label =Labels[3][0],color=purple)
    ax3.plot(x,y[3],':o',label =Labels[3][0],color=green)
    ax4.plot(x,y[4],':o',label =Labels[3][0],color=blue)
    ax1.plot(x,y[5],'--o',label =Labels[3][1],color=red)
    ax2.plot(x,y[6],'--o',label =Labels[3][1],color=orange)
    axN.plot(x,y[7],'--o',label =Labels[3][0],color=purple)
    ax3.plot(x,y[8],'--o',label =Labels[3][1],color=green)
    ax4.plot(x,y[9],'--o',label =Labels[3][1],color=blue)
    ax1.plot(x,y[10],'-o' ,label =Labels[3][2],color=red)
    ax2.plot(x,y[11],'-o' ,label =Labels[3][2],color=orange)
    axN.plot(x,y[12],'-o',label =Labels[3][0],color=purple)
    ax3.plot(x,y[13],'-o',label =Labels[3][2],color=green)
    ax4.plot(x,y[14],'-o',label =Labels[3][2],color=blue)

    l,=ax1.plot(x,np.ones(4)*20,'k-',label ='cc-pVQZ')
    l2,=ax1.plot(x,np.ones(4)*20,'k--',label ='cc-pVTZ')
    l3,= ax1.plot(x,np.ones(4)*20,'k:',label ='cc-pVDZ')
    ax1.set_title(Labels[1][0])
    ax2.set_title(Labels[1][1])
    ax3.set_title(Labels[1][3])
    ax4.set_title(Labels[1][4])
    axN.set_title(Labels[1][2])

    ax1.set_ylim(ymax=5,ymin=-20)
    ax2.set_ylim(ymax=5,ymin=-20)
    ax3.set_ylim(ymax=5,ymin=-20)
    ax4.set_ylim(ymax=5,ymin=-20)

    if meth == 'zcasscf': 
        axN.set_ylim(ymax=32,ymin=-6)
        axN.set_yticks(scipy.arange(-5,32,5))
    if meth == 'caspt2':
        axN.set_yticks(scipy.arange(-30,16,5))

    plt.setp(ax2.get_yticklabels(),visible=False)
    plt.setp(ax4.get_yticklabels(),visible=False)

    plt.legend(handles=[l3,l2,l],loc = 'lower right',frameon=False,bbox_to_anchor = (2.07,0.2),ncol=1)
    title = 'Relative Splitting Error at {}'.format(m)
    fig.text(0.07,0.5,'Relative Splitting Error (%)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
    #plt.suptitle(title ,fontsize=20)
    plt.show()

def contraction_compare(perc,percc):

    var = [[2,3,4],[0,1,2,3,4],['zcasscf','caspt2','mrci'],['dz','tz','qz'],['fc','nfc']]

    for var1 in var[0]: 
        for var2 in var[2]: 
            y.append(make_y(perc, var1,4,var2,var[3],'fc','basisset'))
            yc.append(make_y(percc, var1,4,var2,var[3],'fc','basisset'))
     
    fig,((axF,axCl,axBr)) = plt.subplots(1,3,sharex=True,sharey=True)
    
    ticks = ['DZ','TZ','QZ'] 
    x = np.arange(len(ticks))

#    plt.xticks(x, ticks)
#    plt.setp(ax0.get_xticklabels(),visible=True)
#    plt.setp(ax1.get_xticklabels(),visible=True)
#    plt.setp(ax2.get_xticklabels(),visible=True)

    l1,=axF.plot(x,y[0],'-o',label=Labels[2][0],color=red)
    l2,=axF.plot(x,y[1],'-o',label =Labels[2][1],color=green)
    l3,=axF.plot(x,y[2],'-o',label =Labels[2][2], color=blue)
    axF.plot(x,yc[0],':o',label ='',color=red)
    axF.plot(x,yc[1],':o',label ='',color=green)
    axF.plot(x,yc[2],':o',label ='', color=blue)    

    axCl.plot(x,y[3],'-o',label ='',color=red)
    axCl.plot(x,y[4],'-o',label ='',color=green)
    axCl.plot(x,y[5],'-o',label ='',color=blue)

    axCl.plot(x,yc[3], ':o',label ='',color=red)
    axCl.plot(x,yc[4],':o',label ='',color=green)
    axCl.plot(x,yc[5],':o',label ='',color=blue)

    axBr.plot(x,y[6],'-o',label ='',color=red)
    axBr.plot(x,y[7],'-o',label ='',color=green)
    axBr.plot(x,y[8],'-o',label ='',color=blue)

    axBr.plot(x,yc[6], ':o',label ='',color=red)
    axBr.plot(x,yc[7],':o',label ='',color=green)
    axBr.plot(x,yc[8],':o',label ='',color=blue)

    axF.set_ylim(ymax=5)
    axCl.set_ylim(ymax=5)
    axBr.set_ylim(ymax=5)

    l4, = axF.plot(x,np.ones(len(ticks))*100,'k-',label ='uncontracted')
    l5,=axF.plot(x,np.ones(len(ticks))*100,'k:',label='contracted')
    
    #axF.text( 1,1,'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][0]))
    #axCl.text(1,1,'Exp.: {:>5.1f} cm$^{{-1}}$'.format(sos_list[atomlab][1]))
    #axBr.text(1,1,'Exp.: {:>6.1f} cm$^{{-1}}$'.format(sos_list[atomlab][2]))

    axF.set_title(atom_label[0][4])
    axCl.set_title(atom_label[1][4])
    axBr.set_title(atom_label[2][4])
    plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'upper center',frameon=False,bbox_to_anchor=(-0.69,-0.07),ncol=5)
    #plt.legend(handles=[l1,l2,l3,l4,l5],loc = 'lower right',frameon=False,bbox_to_anchor = (2.07,0.2),ncol=1)
    fig.text(0.07,0.5,'Relative Splitting Error (%)',ha='center',va='center',rotation = 'vertical',fontsize = 15)
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
        return y

if __name__=='__main__':
    data = get_energies.get_data()
    datac = get_energies.get_data_contracted()
    abso, perc = get_energies.get_error(data)
    absoc,percc = get_energies.get_error_contracted(datac)
    #by_method(perc,'caspt2','CASPT2')
    #by_method(perc,'mrci','MRCI')
    #by_method(perc,'zcasscf','CASSCF')

    #contraction_compare(perc,percc)

    #by_contraction(abso,absoc,2,0,'fc')
    by_contraction(abso,absoc,2,0,'nfc')
    #by_contraction(abso,absoc,3,1,'fc')
    #by_contraction(abso,absoc,4,2,'fc')

    #by_basisset_per2(abso,perc,2,0)
    #by_basisset(abso,perc,3,1)
    #by_basisset(abso,perc,4,2)
    #by_basisset(abso,perc,5,3)
