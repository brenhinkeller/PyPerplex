#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 18:42:55 2018
    Run the same isobaric Perplex calculation with different solution models 
    to compare results
@author: cbkeller
"""
#################################################################################
# # # # # # # # # # # # # Import some useful packages # # # # # # # # # # # # # #

# Import perplex interface
from PyPerplex import perplex

# Matplotlib options for vector plotting
from matplotlib import rcParams
rcParams['pdf.fonttype'] = 42
rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt

# For text processing and data handling
import pandas as pd
pd.set_option('display.max_columns',None) # Show me all the columns...
import numpy as np

# For evaluating calculation speed
import time;

# # # # # # # # # # # # #  Directories to configure # # # # # # # # # # # # # # #
    
# Absolute paths to perplex resources
perplexdir = '/Users/cbkeller/Applications/perplex-stable/'; # Location of executables and solution models to use
scratchdir = '/Users/cbkeller/Applications/perplex-stable/scratch1/'; # Location of directory to store output files

# # # # # # # # # # # # # # # Initial composition # # # # # # # # # # # # # # # #

## McDonough Pyrolite
#elements =    [ 'SIO2', 'TIO2', 'AL2O3',  'FEO',  'MNO',  'MGO',  'CAO', 'NA2O',  'K2O',  'H2O',  'CO2',];
#composition = [45.1242, 0.2005, 4.4623, 8.0723, 0.1354, 37.9043, 3.5598, 0.3610, 0.0291, 0.1511, 0.0440,]; 

# Kelemen (2014) primitive continental basalt. H2O and CO2 are guesses
elements =    [ 'SIO2', 'TIO2', 'AL2O3',  'FEO',  'MNO',  'MGO',  'CAO', 'NA2O',  'K2O',  'H2O',  'CO2',];
composition = [50.0956, 0.9564, 15.3224, 8.5103, 0.1659, 9.2520, 9.6912, 2.5472, 0.8588, 2.0000, 0.6000,]; 

## Average Archean basalt (EarthChem data)
#elements =    [ 'SIO2', 'TIO2', 'AL2O3',   'FEO',  'MNO',   'MGO',  'CAO', 'NA2O',  'K2O',  'H2O',  'CO2',];
#composition = [49.2054, 0.8401, 12.0551, 11.4018, 0.2198, 12.3997, 9.3113, 1.6549, 0.4630, 1.8935, 0.5555,]; 


# # # # # # # # # # # # # Some solution model options # # # # # # # # # # # # # #

# Emphasis on phases from Green (2016) -- developed for metabasites, includes what is probably the best (and most expensive) amphibole model. Use with hp11ver.dat
G_solution_phases = 'Augite(G)\nOpx(JH)\ncAmph(G)\noAmph(DP)\nO(JH)\nSp(JH)\nGrt(JH)\nfeldspar_B\nMica(W)\nBio(TCC)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W)\nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nNeph(FB)\n'; 
G_excludes ='ged\nfanth\ngl\n';

# Emphasis on phases from White (2014) -- developed for metapelites. Use with hp11ver.dat
W_solution_phases = 'Omph(HP)\nOpx(W)\ncAmph(DP)\noAmph(DP)\nO(JH)\nSp(JH)\nGt(W)\nfeldspar_B\nMica(W)\nBi(W)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W) \nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nPu(M)\n'; 
W_excludes = 'andr\nts\nparg\ngl\nged\nfanth\n';

# Emphasis on phases from Jennings and Holland (2015) -- developed for mantle melting. Use with hp11ver.dat
JH_solution_phases = 'Cpx(JH)\nOpx(JH)\ncAmph(DP)\noAmph(DP)\nO(JH)\nSp(JH)\nGrt(JH)\nfeldspar_B\nMica(W)\nBio(TCC)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W)\nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nNeph(FB)\n'; 
JH_excludes = 'ts\nparg\ngl\nged\nfanth\n';

# Emphasis on phases from Holland and Powell -- all phases can be used with hp02ver.dat.
HP_solution_phases = 'Omph(HP)\nOpx(HP)\nGlTrTsPg\nAnth\nO(HP)\nSp(HP)\nGt(HP)\nfeldspar_B\nMica(CF)\nBio(TCC)\nChl(HP)\nCtd(HP)\nSapp(HP)\nSt(HP)\nIlHm(A)\nDo(HP)\nT\nB\nF\n';
HP_excludes = '';

# # # # # # # # # # # # # melt(G) + G_solution_phases # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 1;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp11ver.dat', 'melt(G)\n' + G_solution_phases, G_excludes);
elapsed_G_isobaric = time.time() - t
print elapsed_G_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1200+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar -- results returned as pandas DataFrames
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)           # Get system data for all temperatures.  Set include_fluid = 'n' for solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')    # || melt data
 
# Add results to melt % vs temperature figure
plt.figure(0)
plt.clf()
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], melt[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('melt(G) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it from what we know about melt and system
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for e in elements:
    solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], solid[e]);
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(G) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_G.pdf",transparent=True)


# # # # # # # # # # # # # melt(G) + W_solution_phases # # # # # # # # # # # # # #

# Input parameters
P = 10000; # Pressure, bar
T_range = [500+273.15, 1500+273.15]; # Temperature, Kelvin
index = 2; # Calculation index - used only to determine name of working directory

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp11ver.dat', 'melt(G)\n' + W_solution_phases, W_excludes);
elapsed_G_W_isobaric = time.time() - t
print elapsed_G_W_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1200+273;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar -- results returned as pandas DataFrames
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)           # Get system data for all temperatures. Set include_fluid = 'n' for solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')    # || melt data

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], melt[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('melt(G) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G_W.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it from what we know about melt and system
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for e in elements:
    solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], solid[e]);
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(G) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_G_W.pdf",transparent=True)

# # # # # # # # # # # # # melt(G) + JH_solution_phases # # # # # # # # # # # # # 

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 3;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp11ver.dat', 'melt(G)\n' + JH_solution_phases, JH_excludes);
elapsed_G_JH_isobaric = time.time() - t
print elapsed_G_JH_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1200+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar -- results returned as pandas DataFrames
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints)           # Get system data for all temperatures.  Set include_fluid = 'n' for solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)')    # || melt data

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], melt[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('melt(G) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_G_JH.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it from what we know about melt and system
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for e in elements:
    solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], solid[e]);
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(G) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_G_JH.pdf",transparent=True)

# # # # # # # # # # # # pMELTS(G) + HP_solution_phases # # # # # # # # # # # # # 

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 4;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp02ver.dat', 'pMELTS(G)\n' + HP_solution_phases, HP_excludes);
elapsed_pMELTS_HP_isobaric = time.time() - t
print elapsed_pMELTS_HP_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1200+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar -- results returned as pandas DataFrames
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1];
npoints = T_range_inc[1]-T_range_inc[0]+1;
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints);          # Get system data for all temperatures.  Set include_fluid = 'n' for solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'pMELTS(G)'); # || melt data

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], melt[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('pMELTS(G) + HP_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_pMELTS_HP.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it from what we know about melt and system
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for e in elements:
    solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], solid[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('pMELTS(G) + HP_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_pMELTS_HP.pdf",transparent=True)


# # # # # # # # # # # # # melt(W) + W_solution_phases # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 5;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp11ver.dat', 'melt(W)\n' + W_solution_phases, W_excludes);
elapsed_W_isobaric = time.time() - t
print elapsed_W_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1200+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar -- results returned as pandas DataFrames
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1];
npoints = T_range_inc[1]-T_range_inc[0]+1;
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints);          # Get system data for all temperatures.  Set include_fluid = 'n' for solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(W)');   # || melt data

# Add results to melt % vs temperature figure
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], melt[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('melt(W) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_W.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it from what we know about melt and system
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for e in elements:
    solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], solid[e]);
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(W) + W_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_W.pdf",transparent=True)

# # # # # # # # # # # # # melt(W) + G_solution_phases # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 6;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp11ver.dat', 'melt(W)\n' + G_solution_phases, G_excludes);
elapsed_W_G_isobaric = time.time() - t
print elapsed_W_G_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1200+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar -- results returned as pandas DataFrames
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1];
npoints = T_range_inc[1]-T_range_inc[0]+1;
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints);          # Get system data for all temperatures.  Set include_fluid = 'n' for solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(W)');   # || melt data

# Plot melt % vs temperature
plt.figure(0)
plt.plot(melt['T(K)']-273.15, melt['wt_pct'])

# Plot melt composition as a function of melt percent
plt.figure(index)
plt.clf()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], melt[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('melt(W) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_W_G.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it from what we know about melt and system
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for e in elements:
    solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 
    
# Plot solid composition as a function of melt percent
plt.figure()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], solid[e]);
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(W) + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_W_G.pdf",transparent=True)

# # # # # # # # # # # # # melt(W) + JH_solution_phases # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];
index = 7;

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp11ver.dat', 'melt(W)\n' + JH_solution_phases, JH_excludes);
elapsed_W_JH_isobaric = time.time() - t
print elapsed_W_JH_isobaric

# Query the full isobar -- results returned as pandas dataframes
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1];
npoints = T_range_inc[1]-T_range_inc[0]+1;
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints);          # Get system data for all temperatures.  Set include_fluid = 'n' for solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(W)');   # || melt data

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
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], melt[e])
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in melt')
plt.title('melt(W) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("MeltingTest_W_JH.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it from what we know about melt and system
solid = pd.DataFrame();
solid['wt_pct'] = 100 - melt['wt_pct']
for e in elements:
    solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100) 

# Plot solid composition as a function of melt percent
plt.figure()
for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
    plt.plot(melt['wt_pct'], solid[e]);
plt.xlabel('Percent melt')
plt.ylabel('Wt. % in solid')
plt.title('melt(W) + JH_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidTest_W_JH.pdf",transparent=True)
