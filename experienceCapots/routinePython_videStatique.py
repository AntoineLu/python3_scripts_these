# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:33:38 2018

@author: Antoine Luboz

"""
# Se placer dans ce directory
#cd C:\Users\luboz.IPN\Documents\Projets\QualificationFour\ExperienceCapots
#%% Import des packages
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
#from FonctionsPython.extractionCsv import extractionCsv

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
#from matplotlib2tikz import save as tikz_save
import matplotlib as mpl
mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         #r"\usepackage{cmbright}",
         ]
}
mpl.rcParams.update(pgf_with_pdflatex)
        
from matplotlib.ticker import Locator
from scipy.optimize import curve_fit

class MinorSymLogLocator(Locator):
    """
    Dynamically find minor tick positions based on the positions of
    major ticks for a symlog scaling.
    """
    def __init__(self, linthresh):
        """
        Ticks will be placed between the major ticks.
        The placement is linear for x between -linthresh and linthresh,
        otherwise its logarithmically
        """
        self.linthresh = linthresh

    def __call__(self):
        'Return the locations of the ticks'
        majorlocs = self.axis.get_majorticklocs()

        # iterate through minor locs
        minorlocs = []

        # handle the lowest part
        for i in range(1, len(majorlocs)):
            majorstep = majorlocs[i] - majorlocs[i-1]
            if abs(majorlocs[i-1] + majorstep/2) < self.linthresh:
                ndivs = 10
            else:
                ndivs = 9
            minorstep = majorstep / ndivs
            locs = np.arange(majorlocs[i-1], majorlocs[i], minorstep)[1:]
            minorlocs.extend(locs)

        return self.raise_if_exceeds(np.array(minorlocs))

    def tick_values(self, vmin, vmax):
        raise NotImplementedError('Cannot get tick locations for a '
                                  '%s type.' % type(self))
        
#classe des choix de graphes à tracer
class Plots_videStatique:
    """"Classe permettant de choisir quel graphes tracer.
    - sans_capots, logique, defaut = True
    - P_LV, logique, defaut = True
    - P_HV, logique, defaut = True
    - Subplots, logique, defaut = True"""
    
    def __init__(self,sans_capots, capots_10mm, capots_1mm):
        self.sans_capots = True
        self.capots_10mm = True
        self.capots_1mm = True

from uncertainties import ufloat#incertitudes
        
with open('Graphes/resultats_statique.txt','w') as file:
    file.write('---------------------------------------\nPARAMÈTRES DE FIT LORS DU VIDE STATIQUE')

#%% Parmètres de taille et constantes
largeurPlot = 6.68; #largeur en inch
ratioPlot = 1.5;
hauteurPlot = largeurPlot/ratioPlot;
volumeFour = np.array([4500,20])#en litre
print(f'V_f = {ufloat(volumeFour[0],volumeFour[1]):+.2uS} L')

#on défnit d'abord la fonction linéaire
def linfunc(x,a,b):
    return(a*x+b)

#%% Choix des graphes à générer (je crée cette classe pour m'entrainer aux classes)        
choix = Plots_videStatique(True,True,True)

#%% Extraction des datas
videStatique_sansCapots = pd.read_csv('Data/videStatique_sansCapots.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
videStatique_10mm = pd.read_csv('Data/videStatique_10mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)
videStatique_1mm = pd.read_csv('Data/videStatique_1mm.csv',skiprows=1, infer_datetime_format = True, error_bad_lines=False)

#%% Suppression des colonnes inutiles et renommage
del videStatique_sansCapots["Date et heure"] ; del videStatique_sansCapots["Commentaires"]
del videStatique_10mm["Date et heure"] ; del videStatique_10mm["Commentaires"]
del videStatique_1mm["Date et heure"] ; del videStatique_1mm["Commentaires"]
videStatique_1mm.drop(videStatique_1mm.index[1],inplace=True) ; #videStatique_1mm.drop(videStatique_1mm.index[7], inplace=True)#pour supprimer des lignes

#%% Ajout de l'erreur de chaque jauge
videStatique_sansCapots["erreur P_cav (mbar)"] = 0.4*videStatique_sansCapots["P_cav (mbar)"] ; videStatique_sansCapots["erreur P_HV"] = 0.15*videStatique_sansCapots["P_HV (mbar)"]
videStatique_10mm["erreur P_cav (mbar)"] = 0.4*videStatique_10mm["P_cav (mbar)"] ; videStatique_10mm["erreur P_HV"] = 0.15*videStatique_10mm["P_HV (mbar)"]
videStatique_1mm["erreur P_cav (mbar)"] = 0.4*videStatique_1mm["P_cav (mbar)"] ; videStatique_1mm["erreur P_HV"] = 0.15*videStatique_1mm["P_HV (mbar)"]

# Tracé des courbes
#%% P sans capots en fonction du temps en vide statique
if choix.sans_capots:
    func_x = np.linspace(8,45,22)

    popt_sansCapots_pCav, pcov_sansCapots_pCav = curve_fit(linfunc, videStatique_sansCapots.iloc[1:7,0], videStatique_sansCapots.iloc[1:7,1])#.iloc[range ou num row, range ou num colonnes], range: #:#, selection: [#, #, #] ici, les 6 premières valeurs de la colonne 0
    popt_sansCapots_pHv, pcov_sansCapots_pHv = curve_fit(linfunc, videStatique_sansCapots.iloc[1:7,0], videStatique_sansCapots.iloc[1:7,2])
    popt_sansCapots_pRga, pcov_sansCapots_pRga = curve_fit(linfunc, videStatique_sansCapots.iloc[1:7,0], videStatique_sansCapots.iloc[1:7,3])

    plt.figure(num='videStatique_sansCapots_fit', figsize = (largeurPlot, hauteurPlot))
    plt.plot(videStatique_sansCapots['Temps (min)'],videStatique_sansCapots['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    plt.plot(videStatique_sansCapots['Temps (min)'],videStatique_sansCapots['P_HV (mbar)'],'b*', label= '$P_{HV}$')
    plt.plot(videStatique_sansCapots['Temps (min)'],videStatique_sansCapots['P_RGA (mbar)'],'k^', label= '$P_{RGA}$')
    
    plt.plot(func_x,linfunc(func_x, *popt_sansCapots_pCav),'r--', label = 'lin(1:7)' )
    plt.plot(func_x,linfunc(func_x, *popt_sansCapots_pHv),'b--', label = 'lin(1:7)' )
    plt.plot(func_x,linfunc(func_x, *popt_sansCapots_pRga),'k--', label = 'lin(1:7)' )
        
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.errorbar(videStatique_sansCapots['Temps (min)'],videStatique_sansCapots['P_cav (mbar)'], yerr = videStatique_sansCapots['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    plt.errorbar(videStatique_sansCapots['Temps (min)'],videStatique_sansCapots['P_HV (mbar)'], yerr = videStatique_sansCapots['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')
    #plt.errorbar(videStatique_sansCapots['Temps (min)'],videStatique_sansCapots['P_RGA (mbar)'], yerr = videStatique_sansCapots['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{RGA}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log', nonposy = 'mask')
    plt.ylabel(r'$P$ (mbar)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    #plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.title("Sans capots")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "videStatique_sansCapots_fit"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
    print(f'Équation de la courbe P_cav :\n y = ax + b avec a = {ufloat(popt_sansCapots_pCav[0],np.sqrt(np.diag(pcov_sansCapots_pCav))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pCav[1],np.sqrt(np.diag(pcov_sansCapots_pCav))[1]):+.2uS}')
    print(f'Équation de la courbe P_HV :\n y = ax + b avec a = {ufloat(popt_sansCapots_pHv[0],np.sqrt(np.diag(pcov_sansCapots_pHv))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pHv[1],np.sqrt(np.diag(pcov_sansCapots_pHv))[1]):+.2uS}')
    print(f'Équation de la courbe P_RGA :\n y = ax + b avec a = {ufloat(popt_sansCapots_pRga[0],np.sqrt(np.diag(pcov_sansCapots_pRga))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pRga[1],np.sqrt(np.diag(pcov_sansCapots_pRga))[1]):+.2uS}')
    #Dire dans le CR, on néglige le premier point car il y a une forte augmentation de la pression dues aux fuites d'Ar lors de l'opération des vannes.
    print(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA : \n {ufloat(popt_sansCapots_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pCav))[0]*volumeFour[0])**2 + (popt_sansCapots_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_sansCapots_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pHv))[0]*volumeFour[0])**2 + (popt_sansCapots_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_sansCapots_pRga[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pRga))[0]*volumeFour[0])**2 + (popt_sansCapots_pRga[0]*volumeFour[1])**2)/60 ):+.2uS}')#^2 s'écrit **2 en python
    
    with open('Graphes/resultats_statique.txt','a') as file:
        file.write(f'\n\n{name}:')
        file.write(f'\n Équation de la courbe P_cav:\n y = ax + b avec a = {ufloat(popt_sansCapots_pCav[0],np.sqrt(np.diag(pcov_sansCapots_pCav))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pCav[1],np.sqrt(np.diag(pcov_sansCapots_pCav))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_HV:\n y = ax + b avec a = {ufloat(popt_sansCapots_pHv[0],np.sqrt(np.diag(pcov_sansCapots_pHv))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pHv[1],np.sqrt(np.diag(pcov_sansCapots_pHv))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_RGA:\n y = ax + b avec a = {ufloat(popt_sansCapots_pRga[0],np.sqrt(np.diag(pcov_sansCapots_pRga))[0]):+.2uS} et b = {ufloat(popt_sansCapots_pRga[1],np.sqrt(np.diag(pcov_sansCapots_pRga))[1]):+.2uS}')
        file.write(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA:\n {ufloat(popt_sansCapots_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pCav))[0]*volumeFour[0])**2 + (popt_sansCapots_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_sansCapots_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pHv))[0]*volumeFour[0])**2 + (popt_sansCapots_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_sansCapots_pRga[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_sansCapots_pRga))[0]*volumeFour[0])**2 + (popt_sansCapots_pRga[0]*volumeFour[1])**2)/60 ):+.2uS}')
        file.write('\nMatrice de covariance de la courbe P_cav:')
        file.write(f'\n{pcov_sansCapots_pCav}')
        file.write('\n Matrice de covariance de la courbe P_HV:')
        file.write(f'\n{pcov_sansCapots_pHv}')
        file.write('\n Matrice de covariance de la courbe P_RGA:')
        file.write(f'\n{pcov_sansCapots_pRga}')
#%% P capots 10mm en fonction du temps en vide statique
if choix.capots_10mm:
    func_x = np.linspace(0.1,35,22)

    popt_10mm_pCav, pcov_10mm_pCav = curve_fit(linfunc, videStatique_10mm.iloc[1:9,0], videStatique_10mm.iloc[1:9,1])#.iloc[range ou num row, range ou num colonnes], range: #:#, selection: [#, #, #]
    popt_10mm_pHv, pcov_10mm_pHv = curve_fit(linfunc, videStatique_10mm.iloc[1:9,0], videStatique_10mm.iloc[1:9,2])
    popt_10mm_pRga, pcov_10mm_pRga = curve_fit(linfunc, videStatique_10mm.iloc[1:9,0], videStatique_10mm.iloc[1:9,3])

    plt.figure(num='videStatique_10mm_fit', figsize = (largeurPlot, hauteurPlot))
    plt.plot(videStatique_10mm['Temps (min)'],videStatique_10mm['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    plt.plot(videStatique_10mm['Temps (min)'],videStatique_10mm['P_HV (mbar)'],'b*', label= '$P_{HV}$')
    plt.plot(videStatique_10mm['Temps (min)'],videStatique_10mm['P_RGA (mbar)'],'k^', label= '$P_{RGA}$')
    
    plt.plot(func_x,linfunc(func_x, *popt_10mm_pCav),'r--', label = 'lin(1:9)' )
    plt.plot(func_x,linfunc(func_x, *popt_10mm_pHv),'b--', label = 'lin(1:9)' )
    plt.plot(func_x,linfunc(func_x, *popt_10mm_pRga),'k--', label = 'lin(1:9)' )
        
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.errorbar(videStatique_10mm['Temps (min)'],videStatique_10mm['P_cav (mbar)'], yerr = videStatique_10mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    plt.errorbar(videStatique_10mm['Temps (min)'],videStatique_10mm['P_HV (mbar)'], yerr = videStatique_10mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')
    #plt.errorbar(videStatique_10mm['Temps (min)'],videStatique_10mm['P_RGA (mbar)'], yerr = videStatique_10mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{RGA}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log', nonposy = 'mask')
    plt.ylabel(r'$P$ (mbar)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    #plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.title(r"Capots \`{a} 10 mm")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "videStatique_10mm_fit"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
    print('Équation de la courbe P_cav :\n y = ax + b avec a = %.2E +- %.2E' %(popt_10mm_pCav[0],np.sqrt(np.diag(pcov_10mm_pCav))[0]), 'et b = %.2E +- %.2E' %(popt_10mm_pCav[1],np.sqrt(np.diag(pcov_10mm_pCav))[1]) )
    print('Équation de la courbe P_HV :\n y = ax + b avec a = %.2E +- %.2E' %(popt_10mm_pHv[0],np.sqrt(np.diag(pcov_10mm_pHv))[0]), 'et b = %.2E +- %.2E' %(popt_10mm_pHv[1],np.sqrt(np.diag(pcov_10mm_pHv))[1]) )
    print('Équation de la courbe P_RGA :\n y = ax + b avec a = %.2E +- %.2E' %(popt_10mm_pRga[0],np.sqrt(np.diag(pcov_10mm_pRga))[0]), 'et b = %.2E +- %.2E' %(popt_10mm_pRga[1],np.sqrt(np.diag(pcov_10mm_pRga))[1]) )
    #Dire dans le CR, on néglige le premier point car il y a une forte augmentation de la pression dues aux fuites d'Ar lors de l'opération des vannes.
    print(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA:\n {ufloat(popt_10mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pCav))[0]*volumeFour[0])**2 + (popt_10mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_10mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pHv))[0]*volumeFour[0])**2 + (popt_10mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_10mm_pRga[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pRga))[0]*volumeFour[0])**2 + (popt_10mm_pRga[0]*volumeFour[1])**2)/60 ):+.2uS}')
    
    with open('Graphes/resultats_statique.txt','a') as file:
        file.write(f'\n\n{name}:')
        file.write(f'\n Équation de la courbe P_cav:\n y = ax + b avec a = {ufloat(popt_10mm_pCav[0],np.sqrt(np.diag(pcov_10mm_pCav))[0]):+.2uS} et b = {ufloat(popt_10mm_pCav[1],np.sqrt(np.diag(pcov_10mm_pCav))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_HV:\n y = ax + b avec a = {ufloat(popt_10mm_pHv[0],np.sqrt(np.diag(pcov_10mm_pHv))[0]):+.2uS} et b = {ufloat(popt_10mm_pHv[1],np.sqrt(np.diag(pcov_10mm_pHv))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_RGA:\n y = ax + b avec a = {ufloat(popt_10mm_pRga[0],np.sqrt(np.diag(pcov_10mm_pRga))[0]):+.2uS} et b = {ufloat(popt_10mm_pRga[1],np.sqrt(np.diag(pcov_10mm_pRga))[1]):+.2uS}')
        file.write(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA:\n {ufloat(popt_10mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pCav))[0]*volumeFour[0])**2 + (popt_10mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_10mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pHv))[0]*volumeFour[0])**2 + (popt_10mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_10mm_pRga[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_10mm_pRga))[0]*volumeFour[0])**2 + (popt_10mm_pRga[0]*volumeFour[1])**2)/60 ):+.2uS}')
        file.write('\nMatrice de covariance de la courbe P_cav:')
        file.write(f'\n{pcov_10mm_pCav}')
        file.write('\n Matrice de covariance de la courbe P_HV:')
        file.write(f'\n{pcov_10mm_pHv}')
        file.write('\n Matrice de covariance de la courbe P_RGA:')
        file.write(f'\n{pcov_10mm_pRga}')
#%% P capots 1mm en fonction du temps en vide statique
if choix.capots_1mm:
    func_x = np.linspace(1,28,22)

    popt_1mm_pCav, pcov_1mm_pCav = curve_fit(linfunc, videStatique_1mm.iloc[1:6,0], videStatique_1mm.iloc[1:6,1])#.iloc[range ou num row, range ou num colonnes], range: #:#, selection: [#, #, #] ici, les 6 premières valeurs de la colonne 0
    popt_1mm_pHv, pcov_1mm_pHv = curve_fit(linfunc, videStatique_1mm.iloc[1:6,0], videStatique_1mm.iloc[1:6,2])
    popt_1mm_pRga, pcov_1mm_pRga = curve_fit(linfunc, videStatique_1mm.iloc[1:6,0], videStatique_1mm.iloc[1:6,3])

    plt.figure(num='videStatique_1mm_fit', figsize = (largeurPlot, hauteurPlot))
    plt.plot(videStatique_1mm['Temps (min)'],videStatique_1mm['P_cav (mbar)'],'r.', label= '$P_{cav}$')
    plt.plot(videStatique_1mm['Temps (min)'],videStatique_1mm['P_HV (mbar)'],'b*', label= '$P_{HV}$')
    plt.plot(videStatique_1mm['Temps (min)'],videStatique_1mm['P_RGA (mbar)'],'k^', label= '$P_{RGA}$')
    
    plt.plot(func_x,linfunc(func_x, *popt_1mm_pCav),'r--', label = 'lin(1:6)' )
    plt.plot(func_x,linfunc(func_x, *popt_1mm_pHv),'b--', label = 'lin(1:6)' )
    plt.plot(func_x,linfunc(func_x, *popt_1mm_pRga),'k--', label = 'lin(1:6)' )
        
    plt.legend()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    
    plt.errorbar(videStatique_1mm['Temps (min)'],videStatique_1mm['P_cav (mbar)'], yerr = videStatique_1mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{cav}$')
    plt.errorbar(videStatique_1mm['Temps (min)'],videStatique_1mm['P_HV (mbar)'], yerr = videStatique_1mm['erreur P_HV'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{HV}$')
    #plt.errorbar(videStatique_1mm['Temps (min)'],videStatique_1mm['P_RGA (mbar)'], yerr = videStatique_1mm['erreur P_cav (mbar)'], fmt='none', ecolor = 'k', elinewidth = 1, capsize = 1, label= '$P_{RGA}$')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.yscale('log', nonposy = 'mask')
    plt.ylabel(r'$P$ (mbar)')
    plt.xscale('linear')#symlog displays a linear interval at 0 neighborhood
    plt.xlabel('Temps (min)')
    #plt.axes().yaxis.set_tick_params(which='minor', right = 'off')
    #plt.tick_params(axis='y', which='minor')
    #plt.xlim(); plt.ylim()
    #plt.minorticks_on()
    plt.grid(b = True, which = 'major', axis = 'both')
    plt.title(r"Capots \`{a} 1 mm")
    plt.tight_layout()#pour séparer un peu les plots
    
    #export en png et pgf pour latex.
    name = "videStatique_1mm_fit"
    plt.savefig(('Graphes/'+name+'.png'), format = 'png', transparent=True, dpi = 300)
    plt.savefig(('Graphes/'+name+'.pgf'), format = 'pgf')
    plt.savefig(('Graphes/'+name+'.pdf'), format = 'pdf', transparent=True)
    plt.savefig(('Graphes/'+name+'.svg'), format = 'svg', transparent=True)
    plt.show()
    
    print('Équation de la courbe P_cav :\n y = ax + b avec a = %.2E +- %.2E' %(popt_1mm_pCav[0],np.sqrt(np.diag(pcov_1mm_pCav))[0]), 'et b = %.2E +- %.2E' %(popt_1mm_pCav[1],np.sqrt(np.diag(pcov_1mm_pCav))[1]) )
    print('Équation de la courbe P_HV :\n y = ax + b avec a = %.2E +- %.2E' %(popt_1mm_pHv[0],np.sqrt(np.diag(pcov_1mm_pHv))[0]), 'et b = %.2E +- %.2E' %(popt_1mm_pHv[1],np.sqrt(np.diag(pcov_1mm_pHv))[1]) )
    print('Équation de la courbe P_RGA :\n y = ax + b avec a = %.2E +- %.2E' %(popt_1mm_pRga[0],np.sqrt(np.diag(pcov_1mm_pRga))[0]), 'et b = %.2E +- %.2E' %(popt_1mm_pRga[1],np.sqrt(np.diag(pcov_1mm_pRga))[1]) )
    #Dire dans le CR, on néglige le premier point car il y a une forte augmentation de la pression dues aux fuites d'Ar lors de l'opération des vannes.
    print(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA:\n {ufloat(popt_1mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pCav))[0]*volumeFour[0])**2 + (popt_1mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_1mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pHv))[0]*volumeFour[0])**2 + (popt_1mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_1mm_pRga[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pRga))[0]*volumeFour[0])**2 + (popt_1mm_pRga[0]*volumeFour[1])**2)/60 ):+.2uS}')
    
    with open('Graphes/resultats_statique.txt','a') as file:
        file.write(f'\n\n{name}:')
        file.write(f'\n Équation de la courbe P_cav:\n y = ax + b avec a = {ufloat(popt_1mm_pCav[0],np.sqrt(np.diag(pcov_1mm_pCav))[0]):+.2uS} et b = {ufloat(popt_1mm_pCav[1],np.sqrt(np.diag(pcov_1mm_pCav))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_HV:\n y = ax + b avec a = {ufloat(popt_1mm_pHv[0],np.sqrt(np.diag(pcov_1mm_pHv))[0]):+.2uS} et b = {ufloat(popt_1mm_pHv[1],np.sqrt(np.diag(pcov_1mm_pHv))[1]):+.2uS}')
        file.write(f'\n Équation de la courbe P_RGA:\n y = ax + b avec a = {ufloat(popt_1mm_pRga[0],np.sqrt(np.diag(pcov_1mm_pRga))[0]):+.2uS} et b = {ufloat(popt_1mm_pRga[1],np.sqrt(np.diag(pcov_1mm_pRga))[1]):+.2uS}')
        file.write(f'\nTaux de fuite (mbar×L/s) donné par la jauge cavité, HV et RGA:\n {ufloat(popt_1mm_pCav[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pCav))[0]*volumeFour[0])**2 + (popt_1mm_pCav[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_1mm_pHv[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pHv))[0]*volumeFour[0])**2 + (popt_1mm_pHv[0]*volumeFour[1])**2)/60 ):+.2uS}, {ufloat(popt_1mm_pRga[0]*volumeFour[0]/60,np.sqrt( (np.sqrt(np.diag(pcov_1mm_pRga))[0]*volumeFour[0])**2 + (popt_1mm_pRga[0]*volumeFour[1])**2)/60 ):+.2uS}')
        file.write('\nMatrice de covariance de la courbe P_cav:')
        file.write(f'\n{pcov_1mm_pCav}')
        file.write('\n Matrice de covariance de la courbe P_HV:')
        file.write(f'\n{pcov_1mm_pHv}')
        file.write('\n Matrice de covariance de la courbe P_RGA:')
        file.write(f'\n{pcov_1mm_pRga}')