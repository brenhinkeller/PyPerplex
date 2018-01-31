#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:16:38 2018
    A few PerpleX calculation examples using the PyPerplex interface
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
scratchdir = '/Users/cbkeller/Applications/perplex-stable/scratch/'; # Location of directory to store output files

# # # # # # # # # # # # # # # Initial composition # # # # # # # # # # # # # # # #

## McDonough Pyrolite
#elements =    [ 'SIO2', 'TIO2', 'AL2O3',  'FEO',  'MNO',  'MGO',  'CAO', 'NA2O',  'K2O',  'H2O',  'CO2',];
#composition = [45.1242, 0.2005, 4.4623, 8.0723, 0.1354, 37.9043, 3.5598, 0.3610, 0.0291, 0.1511, 0.0440,]; 

## Kelemen (2014) primitive continental basalt. H2O and CO2 are guesses
#elements =    [ 'SIO2', 'TIO2', 'AL2O3',  'FEO',  'MNO',  'MGO',  'CAO', 'NA2O',  'K2O',  'H2O',  'CO2',];
#composition = [50.0956, 0.9564, 15.3224, 8.5103, 0.1659, 9.2520, 9.6912, 2.5472, 0.8588, 2.0000, 0.6000,]; 

# Kelemen (2014) primitive continental basalt excluding Mn and Ti
elements =    [ 'SIO2', 'AL2O3',  'FEO',  'MGO',  'CAO', 'NA2O',  'K2O',  'H2O',  'CO2',];
composition = [50.0956, 15.3224, 8.5103, 9.2520, 9.6912, 2.5472, 0.8588, 2.0000, 0.6000,]; 

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

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 2000; # Pressure, bar
T_range = [500+273.15, 1500+273.15]; # Temperature range, Kelvin
index = 1; # Index determines the name of working directory
melt_model = 'melt(G)';

# Configure (run build and vertex)
t = time.time();
perplex.configure_isobaric(perplexdir, scratchdir, composition, elements, index, P, T_range, 'hp11ver.dat', melt_model + '\n' + G_solution_phases, G_excludes);
elapsed_isobaric = time.time() - t
print elapsed_isobaric

# Query all properties at a single temperature -- results retruned as text
T = 1450+273.15;
data_isobaric = perplex.query_isobar(perplexdir, scratchdir, index, T)
print data_isobaric

# Query the full isobar -- results returned as pandas DataFrames
T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1]
npoints = T_range_inc[1]-T_range_inc[0]+1
system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints);          # Get system data for all temperatures. Set include_fluid = 'n' to get solid+melt only
modes = perplex.query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints);            # || phase modes
melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,melt_model);  # || melt data
    

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
plt.savefig("MeltComposition.pdf",transparent=True)

# Create DataFrame to hold solid composition and fill it using what we know from system and melt 
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
plt.title(melt_model + ' + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("SolidComposition.pdf",transparent=True)

# Plot modes of all phases as a function of temperature
plt.figure()
for m in modes.columns[2:]:
    plt.plot(modes['T(K)']-273.15, modes[m]);
plt.xlabel('T (C)')
plt.ylabel('Weight percent')
plt.title(melt_model+ ' + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()
plt.savefig("PhaseModes.pdf",transparent=True)

# Plot modes of all phases as a function of melt percent
plt.figure()
for m in modes.columns[2:]:
    plt.plot(modes[melt_model], modes[m]);
plt.xlabel('Percent melt')
plt.ylabel('Weight percent')
plt.title(melt_model + ' + G_solution_phases, %i bar' %(P))
plt.legend(fontsize=10)
plt.show()

# # # # # # # # # # # # # Geothermal gradient example # # # # # # # # # # # # # #

# Input parameters
P_range = [280, 28000] # Pressure range to explore, bar (1-100 km)
T_surf = 273.15; # Temperature of surface (K)
geotherm = 0.1; # Geothermal gradient of 0.1 K/bar == about 28.4 K/km
index = 0; # Index determines the name of working directory
melt_model = 'melt(G)';

# Configure (run build and vertex)
t = time.time();
perplex.configure_geotherm(perplexdir, scratchdir, composition, elements, index, P_range, T_surf, geotherm, 'hp11ver.dat', melt_model + '\n' + G_solution_phases, G_excludes);
elapsed_G_geotherm = time.time() - t
print elapsed_G_geotherm

# Query seismic properties along the whole geotherm
geotherm_sesimic = perplex.query_geotherm_seismic(perplexdir, scratchdir, index, P_range, 100)

# Query all properties at a single pressure
P = 10000;
data_geotherm = perplex.query_geotherm(perplexdir, scratchdir, index, P)
print data_geotherm


##


