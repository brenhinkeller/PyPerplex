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
pd.set_option('display.max_columns',None) # Show me all the columns...
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

## Composition   SIO2     TIO2    AL2O3    FEO     MNO     MGO     CAO     NA2O    K2O     H2O
#composition = [50.2841, 0.9600, 15.3801, 8.5423, 0.1665, 9.2868, 9.7277, 2.5568, 0.8000, 2.3000,]; # Kelemen primitive continental basalt
#elements = 'SIO2\nTIO2\nAL2O3\nFEO\nMNO\nMGO\nCAO\nNA2O\nK2O\nH2O\n';

## Composition   SIO2     TIO2    AL2O3    FEO      MNO      MGO     CAO     NA2O    K2O     H2O
#composition = [49.2388, 0.8619, 12.7914, 11.1946, 0.2050, 12.3062, 9.6917, 1.6871, 0.5019, 1.5214]; # Average Archean basalt
#elements = 'SIO2\nTIO2\nAL2O3\nFEO\nMNO\nMGO\nCAO\nNA2O\nK2O\nH2O\n';

# Composition   SIO2     TIO2    AL2O3    FEO     MNO     MGO     CAO     NA2O    K2O     H2O
composition = [64.8684, 0.6500, 15.0878, 4.9230, 0.1009, 3.2589, 4.1573, 3.8177, 2.1386, 0.9973,]; # Test composition for K/Ca
elements = 'SIO2\nTIO2\nAL2O3\nFEO\nMNO\nMGO\nCAO\nNA2O\nK2O\nH2O\n';


# # # # # # # # # # # # # Some solution model options # # # # # # # # # # # # # #

# Holland and Powell
HP_solution_phases = 'Omph(HP)\nOpx(HP)\nGlTrTsPg\nAnth\nO(HP)\nSp(HP)\nGt(HP)\nfeldspar_B\nMica(CF)\nBio(TCC)\nChl(HP)\nCtd(HP)\nSapp(HP)\nSt(HP)\nIlHm(A)\nDo(HP)\nT\nB\nF\n';
HP_excludes = '';

# Emphasis on phases from Jennings and Holland (2015)
JH_solution_phases = 'Cpx(JH)\nOpx(JH)\ncAmph(DP)\noAmph(DP)\nO(JH)\nSp(JH)\nGrt(JH)\nfeldspar_B\nMica(W)\nBio(TCC)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W)\nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nNeph(FB)\n'; 
JH_excludes = 'ts\nparg\ngl\nged\nfanth\n';

# Emphasis on phases from Green (2016)
G_solution_phases = 'Augite(G)\nOpx(JH)\ncAmph(G)\noAmph(DP)\nO(JH)\nSp(JH)\nGrt(JH)\nfeldspar_B\nMica(W)\nBio(TCC)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W)\nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nNeph(FB)\n'; 
G_excludes ='ged\nfanth\ngl\n';

# Emphasis on phases from White (2014)
W_solution_phases = 'Omph(HP)\nOpx(W)\ncAmph(DP)\noAmph(DP)\nO(JH)\nSp(JH)\nGt(W)\nfeldspar_B\nMica(W)\nBi(W)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W) \nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nPu(M)\n'; 
W_excludes = 'andr\nts\nparg\ngl\nged\nfanth\n';


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

# Query all properties at a single temperature -- results retruned as text
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data for all temperatures - - results returned as pandas data frame
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')
# Get system data for all temperatures - - results returned as pandas data frame
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    

# Add results to melt % vs temperature figure
plt.figure(0)
plt.clf()
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
plt.plot(melt['wt_pct'], melt['SIO2'])
plt.plot(melt['wt_pct'], melt['AL2O3'])
plt.plot(melt['wt_pct'], melt['MGO'])
plt.plot(melt['wt_pct'], melt['FEO'])
plt.plot(melt['wt_pct'], melt['CAO'])
plt.plot(melt['wt_pct'], melt['K2O'])
plt.plot(melt['wt_pct'], melt['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('melt(G) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G.pdf",transparent=True)

# Create dataframe to hold solid composition
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for element in ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O']:
    solid[element] = (system[element] - (melt[element] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
plt.plot(melt['wt_pct'], solid['SIO2'])
plt.plot(melt['wt_pct'], solid['AL2O3'])
plt.plot(melt['wt_pct'], solid['MGO'])
plt.plot(melt['wt_pct'], solid['FEO'])
plt.plot(melt['wt_pct'], solid['CAO'])
plt.plot(melt['wt_pct'], solid['K2O'])
plt.plot(melt['wt_pct'], solid['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(G) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_G.pdf",transparent=True)

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

# Query all properties at a single temperature -- results retruned as text
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data for all temperatures -- results returned as pandas data frame
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')
# Get system data for all temperatures - - results returned as pandas data frame
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
plt.plot(melt['wt_pct'], melt['SIO2'])
plt.plot(melt['wt_pct'], melt['AL2O3'])
plt.plot(melt['wt_pct'], melt['MGO'])
plt.plot(melt['wt_pct'], melt['FEO'])
plt.plot(melt['wt_pct'], melt['CAO'])
plt.plot(melt['wt_pct'], melt['K2O'])
plt.plot(melt['wt_pct'], melt['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(G) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G_W.pdf",transparent=True)

# Create dataframe to hold solid composition
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for element in ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O']:
    solid[element] = (system[element] - (melt[element] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
plt.plot(melt['wt_pct'], solid['SIO2'])
plt.plot(melt['wt_pct'], solid['AL2O3'])
plt.plot(melt['wt_pct'], solid['MGO'])
plt.plot(melt['wt_pct'], solid['FEO'])
plt.plot(melt['wt_pct'], solid['CAO'])
plt.plot(melt['wt_pct'], solid['K2O'])
plt.plot(melt['wt_pct'], solid['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(G) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_G_W.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 3;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp11ver.dat', 'melt(G)\n' + JH_solution_phases, JH_excludes, elements);
elapsed_G_JH_isobaric = time.time() - t
print elapsed_G_JH_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data for all temperatures -- results returned as pandas data frame
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')
# Get system data for all temperatures - - results returned as pandas data frame
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
plt.plot(melt['wt_pct'], melt['SIO2'])
plt.plot(melt['wt_pct'], melt['AL2O3'])
plt.plot(melt['wt_pct'], melt['MGO'])
plt.plot(melt['wt_pct'], melt['FEO'])
plt.plot(melt['wt_pct'], melt['CAO'])
plt.plot(melt['wt_pct'], melt['K2O'])
plt.plot(melt['wt_pct'], melt['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(G) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G_JH.pdf",transparent=True)

# Create dataframe to hold solid composition
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for element in ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O']:
    solid[element] = (system[element] - (melt[element] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
plt.plot(melt['wt_pct'], solid['SIO2'])
plt.plot(melt['wt_pct'], solid['AL2O3'])
plt.plot(melt['wt_pct'], solid['MGO'])
plt.plot(melt['wt_pct'], solid['FEO'])
plt.plot(melt['wt_pct'], solid['CAO'])
plt.plot(melt['wt_pct'], solid['K2O'])
plt.plot(melt['wt_pct'], solid['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(G) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_G_JH.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 4;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp02ver.dat', 'pMELTS(G)\n' + HP_solution_phases, HP_excludes, elements);
elapsed_pMELTS_HP_isobaric = time.time() - t
print elapsed_pMELTS_HP_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data for all temperatures -- results returned as pandas data frame
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'pMELTS(G)')
# Get system data for all temperatures - - results returned as pandas data frame
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
plt.plot(melt['wt_pct'], melt['SIO2'])
plt.plot(melt['wt_pct'], melt['AL2O3'])
plt.plot(melt['wt_pct'], melt['MGO'])
plt.plot(melt['wt_pct'], melt['FEO'])
plt.plot(melt['wt_pct'], melt['CAO'])
plt.plot(melt['wt_pct'], melt['K2O'])
plt.plot(melt['wt_pct'], melt['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('pMELTS(G) + HP_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_pMELTS_HP.pdf",transparent=True)

# Create dataframe to hold solid composition
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for element in ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O']:
    solid[element] = (system[element] - (melt[element] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
plt.plot(melt['wt_pct'], solid['SIO2'])
plt.plot(melt['wt_pct'], solid['AL2O3'])
plt.plot(melt['wt_pct'], solid['MGO'])
plt.plot(melt['wt_pct'], solid['FEO'])
plt.plot(melt['wt_pct'], solid['CAO'])
plt.plot(melt['wt_pct'], solid['K2O'])
plt.plot(melt['wt_pct'], solid['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('pMELTS(G) + HP_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_pMELTS_HP.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 5;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp11ver.dat', 'melt(W)\n' + W_solution_phases, W_excludes, elements);
elapsed_W_isobaric = time.time() - t
print elapsed_W_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data for all temperatures -- results returned as pandas data frame
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(W)')
# Get system data for all temperatures - - results returned as pandas data frame
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
plt.plot(melt['wt_pct'], melt['SIO2'])
plt.plot(melt['wt_pct'], melt['AL2O3'])
plt.plot(melt['wt_pct'], melt['MGO'])
plt.plot(melt['wt_pct'], melt['FEO'])
plt.plot(melt['wt_pct'], melt['CAO'])
plt.plot(melt['wt_pct'], melt['K2O'])
plt.plot(melt['wt_pct'], melt['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(W) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_W.pdf",transparent=True)

# Create dataframe to hold solid composition
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for element in ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O']:
    solid[element] = (system[element] - (melt[element] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
plt.plot(melt['wt_pct'], solid['SIO2'])
plt.plot(melt['wt_pct'], solid['AL2O3'])
plt.plot(melt['wt_pct'], solid['MGO'])
plt.plot(melt['wt_pct'], solid['FEO'])
plt.plot(melt['wt_pct'], solid['CAO'])
plt.plot(melt['wt_pct'], solid['K2O'])
plt.plot(melt['wt_pct'], solid['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(W) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_W.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 6;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp11ver.dat', 'melt(W)\n' + G_solution_phases, G_excludes, elements);
elapsed_W_G_isobaric = time.time() - t
print elapsed_W_G_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data for all temperatures -- results returned as pandas data frame
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(W)')
# Get system data for all temperatures - - results returned as pandas data frame
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    

# Plot melt % vs temperature
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
plt.plot(melt['wt_pct'], melt['SIO2'])
plt.plot(melt['wt_pct'], melt['AL2O3'])
plt.plot(melt['wt_pct'], melt['MGO'])
plt.plot(melt['wt_pct'], melt['FEO'])
plt.plot(melt['wt_pct'], melt['CAO'])
plt.plot(melt['wt_pct'], melt['K2O'])
plt.plot(melt['wt_pct'], melt['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(W) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_W_G.pdf",transparent=True)

# Create dataframe to hold solid composition
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for element in ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O']:
    solid[element] = (system[element] - (melt[element] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
plt.plot(melt['wt_pct'], solid['SIO2'])
plt.plot(melt['wt_pct'], solid['AL2O3'])
plt.plot(melt['wt_pct'], solid['MGO'])
plt.plot(melt['wt_pct'], solid['FEO'])
plt.plot(melt['wt_pct'], solid['CAO'])
plt.plot(melt['wt_pct'], solid['K2O'])
plt.plot(melt['wt_pct'], solid['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(W) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_W_G.pdf",transparent=True)

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 7;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, index, P, T_range, 'hp11ver.dat', 'melt(W)\n' + JH_solution_phases, JH_excludes, elements);
elapsed_W_JH_isobaric = time.time() - t
print elapsed_W_JH_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1400+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
# Get melt data for all temperatures -- results returned as pandas data frame
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(W)')
# Get system data for all temperatures - - results returned as pandas data frame
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)    

# Plot melt % vs temperature
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])
plt.xlabel('T (C)')
plt.ylabel('Percent melt')
plt.legend(fontsize=10)
plt.show()
plt.savefig("PercentMeltVsTemp.pdf",transparent=True)

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
plt.plot(melt['wt_pct'], melt['SIO2'])
plt.plot(melt['wt_pct'], melt['AL2O3'])
plt.plot(melt['wt_pct'], melt['MGO'])
plt.plot(melt['wt_pct'], melt['FEO'])
plt.plot(melt['wt_pct'], melt['CAO'])
plt.plot(melt['wt_pct'], melt['K2O'])
plt.plot(melt['wt_pct'], melt['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. %')
plt.title('melt(W) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_W_JH.pdf",transparent=True)

# Create dataframe to hold solid composition
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for element in ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O']:
    solid[element] = (system[element] - (melt[element] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
plt.plot(melt['wt_pct'], solid['SIO2'])
plt.plot(melt['wt_pct'], solid['AL2O3'])
plt.plot(melt['wt_pct'], solid['MGO'])
plt.plot(melt['wt_pct'], solid['FEO'])
plt.plot(melt['wt_pct'], solid['CAO'])
plt.plot(melt['wt_pct'], solid['K2O'])
plt.plot(melt['wt_pct'], solid['NA2O'])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(W) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_W_JH.pdf",transparent=True)

##
