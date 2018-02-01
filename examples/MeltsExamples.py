#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 00:10:31 2018

@author: cbkeller
"""
from PyPerplex import melts

#%% # # # # # # # # # # # # pMelts equil. batch melting # # # # # # # # # # # # #
meltspath = '/usr/local/bin/run_alphamelts.command';
scratchdir = '/Users/cbkeller/Applications/perplex-stable';

# Conditions
H2O=0.15; 
P_range = [20000,20000]; 
T_range = [1700,800]
# Starting composition
elements = ['SiO2',  'TiO2','Al2O3','Fe2O3','Cr2O3',  'FeO',  'MnO',  'MgO',   'NiO',  'CoO',  'CaO',  'Na2O', 'K2O', 'P2O5','H2O',];
composition=[44.8030, 0.1991, 4.4305, 0.9778, 0.3823, 7.1350, 0.1344, 37.6345, 0.2489, 0.0129, 3.5345, 0.3584, 0.0289, 0.0209,  H2O,]; #mcdbse (McDonough Pyrolite)
# Batch string
batchstring='1\nsc.melts\n10\n1\n3\n1\nliquid\n1\n1.0\n0\n10\n0\n4\n0\n';
# Run simulation
melts.configure(meltspath, scratchdir, composition, elements, batchstring, T_range, P_range, dT=-10, dP=0, index=1, version='pMELTS',mode='isobaric',fo2path='FMQ')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

## Plot results
#plotelements={'SiO2','Al2O3','CaO','MgO','FeO','Na2O','K2O'};
#c=lines(length(plotelements));
#figure;
#for i=1:length(plotelements)
#    hold on; plot(melts.liquid_0.mass,melts.liquid_0.(plotelements{i}),'Color',c(i,:))
#end
#legend(plotelements)
#title([num2str(H2O) ' Percent  H2O,  ' num2str(Pi) '  bar'])
#xlabel('Percent melt')
#ylabel('Abudance (wt. %)')
#xlim([0 100])
