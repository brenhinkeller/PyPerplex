#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:16:38 2018
    A few PerpleX calculation examples using the PyPerplex interface
@author: cbkeller
"""
# Import perplex interface
from PyPerplex import perplex

# Matplotlib options for vector plotting
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Helvetica']
rcParams['pdf.fonttype'] = 42
rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt

# For text processing and data handling
import pandas as pd
import numpy as np

# For evaluating calculation speed
import time;

############################ Example calculations ###############################
    
# Absolute paths to perplex resources
perplexdir = '/Users/cbkeller/Applications/perplex-stable/'; # Location of executables and solution models to use
scratchdir = '/Users/cbkeller/Applications/perplex-stable/'; # Location of directory to store output files

# # # # # # # # # # # # # # # Initial composition # # # # # # # # # # # # # # # #

## Composition   SIO2     TIO2    AL2O3    FEO     MNO     MGO     CAO     NA2O    K2O     H2O
#composition = [45.1242, 0.2005, 4.4623, 8.0723, 0.1354, 37.9043, 3.5598, 0.3610, 0.0291, 0.1511,]; # McDonough Pyrolite
#elements = 'SIO2\nTIO2\nAL2O3\nFEO\nMNO\nMGO\nCAO\nNA2O\nK2O\nH2O\n';

# Composition   SIO2     TIO2    AL2O3    FEO     MNO     MGO     CAO     NA2O    K2O     H2O
composition = [50.2841, 0.9600, 15.3801, 8.5423, 0.1665, 9.2868, 9.7277, 2.5568, 0.1567, 2.9389,]; # Kelemen primitive continental basalt
elements = 'SIO2\nTIO2\nAL2O3\nFEO\nMNO\nMGO\nCAO\nNA2O\nK2O\nH2O\n';

# # # # # # # # # # # # # Some solution model options # # # # # # # # # # # # # #

# Holland and Powell
HP_solution_phases = 'O(HP)\nOpx(HP)\nOmph(HP)\nGt(HP)\nGlTrTsPg\nAnth\nT\nB\nChl(HP)\nBio(TCC)\nMica(CF)\nCtd(HP)\nIlHm(A)\nSp(HP)\nSapp(HP)\nSt(HP)\nfeldspar_B\nDo(HP)\nF\n';
HP_excludes = '';

# Emphasis on phases from Jennings and Holland (2015)
JH_solution_phases = 'Cpx(JH)\nOpx(JH)\nGlTrTsPg\nAnth\nO(JH)\nSp(JH)\nGrt(JH)\nfeldspar_B\nMica(W)\nBio(TCC)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W)\nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nNeph(FB)\n'; 
JH_excludes ='';

# Emphasis on phases from Green (2016)
G_solution_phases = 'Augite(G)\nOpx(JH)\ncAmph(G)\noAmph(DP)\nO(JH)\nSp(JH)\nGrt(JH)\nfeldspar_B\nMica(W)\nBio(TCC)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W)\nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nNeph(FB)\n'; 
G_excludes ='ged\nfanth\ngl\n';

# Emphasis on phases from White (2014)
W_solution_phases = 'Omph(HP)\nOpx(W)\ncAmph(DP)\noAmph(DP)\nO(JH)\nSp(JH)\nGt(W)\nfeldspar_B\nMica(W)\nBi(W)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W) \nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nPu(M)\n'; 
W_excludes ='andr\nts\nparg\ngl\nged\nfanth\n';


# # # # # # # # # # # # # Geothermal gradient example # # # # # # # # # # # # # #
#
## Input parameters
#P_range = [280, 28000] # Pressure range to explore, bar (1-100 km)
#T_surf = 273.15; # Temperature of surface (K)
#geotherm = 0.1; # Geothermal gradient of 0.1 K/bar, or about 28.4 K/km
#index = 0;
#
## Configure (run build and vertex)
#t = time.time();
#perplex.configure_geotherm(perplexdir, scratchdir, composition, index, P_range, T_surf, geotherm, 'hp11ver.dat', 'melt(G)' + G_solution_phases, G_excludes, elements);
#elapsed_G_geotherm = time.time() - t
#print elapsed_G_geotherm
#
#
## Query seismic properties along the whole geotherm
##geotherm_sesimic_table = query_perplex_geotherm_seismic(perplexdir, scratchdir, index, P_range, 100)
#
## Query all properties at a single pressure
#P = 10000;
#data_geotherm = perplex.query_geotherm(perplexdir, scratchdir, index, P)
#print data_geotherm

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 1;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp11ver.dat', 'melt(G)\n' + G_solution_phases, G_excludes, elements);
elapsed_G_isobaric = time.time() - t
print elapsed_G_isobaric

# Query all properties at a single temperature
T = 1599+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data
melt_data = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')
# Get system data
system_data = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    


plt.figure(0)
plt.clf()
plt.plot(melt_data['T(K)']-273.15, melt_data['wt,%'])

plt.figure(index)
plt.clf()
plt.plot(melt_data['wt,%'], melt_data['SIO2,wt%'])
plt.plot(melt_data['wt,%'], melt_data['AL2O3,wt%'])
plt.plot(melt_data['wt,%'], melt_data['MGO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['FEO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['CAO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['K2O,wt%'])
plt.plot(melt_data['wt,%'], melt_data['NA2O,wt%'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(G) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 2;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp11ver.dat', 'melt(G)\n' + W_solution_phases, W_excludes, elements);
elapsed_G_W_isobaric = time.time() - t
print elapsed_G_W_isobaric

# Query all properties at a single temperature
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
melt_data = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')

plt.figure(0)
plt.plot(melt_data['T(K)']-273.15, melt_data['wt,%'])

plt.figure(index)
plt.clf()
plt.plot(melt_data['wt,%'], melt_data['SIO2,wt%'])
plt.plot(melt_data['wt,%'], melt_data['AL2O3,wt%'])
plt.plot(melt_data['wt,%'], melt_data['MGO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['FEO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['CAO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['K2O,wt%'])
plt.plot(melt_data['wt,%'], melt_data['NA2O,wt%'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(G) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G_W.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 3;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp02ver.dat', 'pMELTS(G)\n' + HP_solution_phases, HP_excludes, elements);
elapsed_pMELTS_HP_isobaric = time.time() - t
print elapsed_pMELTS_HP_isobaric

# Query all properties at a single temperature
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
melt_data = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'pMELTS(G)')

plt.figure(0)
plt.plot(melt_data['T(K)']-273.15, melt_data['wt,%'])

plt.figure(index)
plt.clf()
plt.plot(melt_data['wt,%'], melt_data['SIO2,wt%'])
plt.plot(melt_data['wt,%'], melt_data['AL2O3,wt%'])
plt.plot(melt_data['wt,%'], melt_data['MGO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['FEO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['CAO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['K2O,wt%'])
plt.plot(melt_data['wt,%'], melt_data['NA2O,wt%'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('pMELTS(G) + HP_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_pMELTS_HP.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 4;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp11ver.dat', 'melt(W)\n' + W_solution_phases, W_excludes, elements);
elapsed_W_isobaric = time.time() - t
print elapsed_W_isobaric

# Query all properties at a single temperature
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
melt_data = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(W)')

plt.figure(0)
plt.plot(melt_data['T(K)']-273.15, melt_data['wt,%'])
plt.xlabel('T (C)')
plt.ylabel('Percent melt')
plt.legend(fontsize=10)
plt.show()
plt.savefig("PercentMeltVsTemp.pdf",transparent=True)

plt.figure(index)
plt.clf()
plt.plot(melt_data['wt,%'], melt_data['SIO2,wt%'])
plt.plot(melt_data['wt,%'], melt_data['AL2O3,wt%'])
plt.plot(melt_data['wt,%'], melt_data['MGO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['FEO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['CAO,wt%'])
plt.plot(melt_data['wt,%'], melt_data['K2O,wt%'])
plt.plot(melt_data['wt,%'], melt_data['NA2O,wt%'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(W) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_W.pdf",transparent=True)

##
