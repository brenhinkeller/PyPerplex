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
scratchdir = '/Users/cbkeller/Applications/perplex-stable/AntonelliKCa/'; # Location of directory to store output files

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
W_solution_phases = 'Cpx(JH)\nOpx(W)\ncAmph(DP)\noAmph(DP)\nO(JH)\nSp(JH)\nGt(W)\nfeldspar_B\nMica(W)\nBi(W)\nChl(W)\nCtd(W)\nCrd(W)\nSa(WP)\nSt(W)\nIlm(WPH)\nAtg(PN)\nT\nB\nF\nDo(HP)\nScap\nChum\nPu(M)\n'; 
W_excludes = 'andr\nts\nparg\ngl\nged\nfanth\n';

# # # # # # # # # # # # # # # # Isobaric example # # # # # # # # # # # # # # # #

# Input parameters
P = 10000; # bar
T_range = [500+273.15, 1500+273.15];

## Elements to use and starting composition
#elementstring = 'SIO2\nTIO2\nAL2O3\nFEO\nMNO\nMGO\nCAO\nNA2O\nK2O\nH2O\n';
#protoliths = pd.read_csv(scratchdir + 'GranuliteProtlithEstimates.csv', delim_whitespace=True);
#observed = pd.read_csv(scratchdir + 'ObservedCompositions.csv', delim_whitespace=True);
#elements = ['SIO2','TIO2','AL2O3','FEO','MNO','MGO','CAO','NA2O','K2O','H2O'];

# Exclude Mn and Ti since the melt model can't handle them
elementstring = 'SIO2\nAL2O3\nFEO\nMGO\nCAO\nNA2O\nK2O\nH2O\n'; # No Mn or Ti
protoliths = pd.read_csv(scratchdir + 'GranuliteProtlithEstimatesNoMnTi.csv', delim_whitespace=True);
observed = pd.read_csv(scratchdir + 'ObservedCompositionsNoMnTi.csv', delim_whitespace=True);
elements = ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O','H2O']

bestfits = pd.DataFrame();


# Cycle through a set of compositions read from file
for index in range(len(protoliths)):
    starting_composition = protoliths[index:index+1].values[0];
    observed_composition = observed[index:index+1];

    # Configure (run build and vertex)
    t = time.time();
    perplex.configure_isobaric(perplexdir, scratchdir, starting_composition, index, P, T_range, 'hp11ver.dat', 'melt(G)\n' + W_solution_phases, W_excludes, elementstring);
    elapsed_G_W_isobaric = time.time() - t
    print elapsed_G_W_isobaric
    
    # Query the full isobar
    T_range_inc = [np.floor(T_range[0])+1, np.ceil(T_range[1])-1];
    npoints = T_range_inc[1]-T_range_inc[0]+1;
    # Get melt data for all temperatures - - results returned as pandas data frame
    melt = perplex.query_isobar_phase(perplexdir,scratchdir,index,T_range_inc,npoints,'melt(G)');
    # Get system data for all temperatures - - results returned as pandas data frame
    system = perplex.query_isobar_system(perplexdir,scratchdir,index,T_range_inc,npoints);   
    
    
    # Create dataframe to hold solid composition
    solid = pd.DataFrame();
    solid['wt_pct'] = 100 - melt['wt_pct']
    solid['T(K)'] = melt['T(K)'];
    for e in elements:
        solid[e] = (system[e] - (melt[e] * melt['wt_pct']/100)) / (solid['wt_pct']/100);
 
    rsquared = np.zeros(len(melt));       
    for e in ['SIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O']:
        uncertainty = max([min([observed_composition[e].values[0]*0.05,0.5]),0.001])
        rsquared = rsquared + ((solid[e].values - observed_composition[e].values[0])/uncertainty)**2;

    rsquared[np.isnan(rsquared)] = 1E100; # Set NaNs to an arbirarily large value
    closest_match = np.argmin(rsquared);
    
#    print melt['wt_pct'].values[closest_match];
    print solid[closest_match:closest_match+1];
    
    # Plot solid composition as a function of melt percent
    plt.figure()
    plt.clf()
    plt.plot(melt['wt_pct'], solid['SIO2'])
    plt.plot(melt['wt_pct'], solid['AL2O3'])
    plt.plot(melt['wt_pct'], solid['MGO'])
    plt.plot(melt['wt_pct'], solid['FEO'])
    plt.plot(melt['wt_pct'], solid['CAO'])
    plt.plot(melt['wt_pct'], solid['K2O'])
    plt.plot(melt['wt_pct'], solid['NA2O'])
    plt.xlabel('Percent melt')
    plt.ylabel('Wt. % in solid')
    plt.legend(fontsize=10)
    plt.show()                  



