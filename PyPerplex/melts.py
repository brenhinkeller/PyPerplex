#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 02:00:37 2018

@author: cbkeller
"""
#def configure_isobaric(perplexdir, scratchdir, composition, elements = ['SIO2','TIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O','H2O'], index = 1, P = 10000, T_range = [500+273.15, 1500+273.15], dataset = 'hp11ver.dat', solution_phases = 'O(HP)\nOpx(HP)\nOmph(GHP)\nGt(HP)\noAmph(DP)\ncAmph(DP)\nT\nB\nChl(HP)\nBio(TCC)\nMica(CF)\nCtd(HP)\nIlHm(A)\nSp(HP)\nSapp(HP)\nSt(HP)\nfeldspar_B\nDo(HP)\nF\n', excludes = 'ts\nparg\ngl\nged\nfanth\ng\n'):

# Import some useful packages
import os # os.system lets us access the command line
import numpy as np # For np.array
#import pandas as pd # Pandas, for importing PerpleX text file output as data frames

def configure(meltspath, scratchdir, composition, elements, batchstring, T_range, P_range, dT=-10, dP=0, index=1, version='pMELTS',mode='isobaric',fo2path='FMQ',fractionatesolids='!'):
    
    ############################ Default Settings ###############################
    ##MELTS or pMELTS
    #version='pMELTS';
    ##Mode (isothermal, isobaric, isentropic, isenthalpic, isochoric, geothermal or PTPath)
    #mode='isobaric';
    ## Set fO2 constraint, i.e. 'IW','COH','FMQ','NNO','HM','None' as a string
    #fo2path='FMQ';
    ## Fractionate all solids? ('!' for no, '' for yes)
    #fractionatesolids='!';
    # Mass retained during fractionation
    massin=0.001;
    # Ouptut temperatures in celcius? ('!' for no, '' for yes)
    celciusoutput='';
    # Save all output? ('!' for no, '' for yes)
    saveall='!';
    # Fractionate all water? ('!' for no, '' for yes)
    fractionatewater='!';
    # Fractionate individual phases (specify as strings in cell array, i.e. {'olivine','spinel'})
    fractionate=[];
    # Supress individual phases (specify as strings in cell array, i.e. {'leucite'})
    supress=[];
    # Coninuous (fractional) melting? ('!' for no, '' for yes)
    continuous='!';
    # Threshold above which melt is extracted (if fractionation is turned on)
    minf=0.005;
    # Do trace element calculations
    dotrace='!';
    # Treat water as a trace element
    dotraceh2o='!';
    # Initial trace compositionT
    tsc=[];
    # Initial trace elements
    telements=[];
    # Default global constraints
    Pmax=90000;
    Pmin=2;
    Tmax=3000;
    Tmin=450;
    # Simulation number (for folder, etc)
    
    ########################## end Default Settings ############################
    
    # Guess if intention is for calculation to end at Tf or Pf as a min or max
    if T_range[1]<T_range[0]:
        Tmin=T_range[1]
    if T_range[1]>T_range[0]:
        Tmax=T_range[1];
    if P_range[1]<P_range[0]:
        Pmin=P_range[1];
    if P_range[1]>P_range[0]:
        Pmax=P_range[1];
    
    # Normalize starting composition
    composition = np.array(composition)/sum(composition)*100; 
    
    # output prefixectory name
    prefix = scratchdir + 'out%i' %(index);
    os.system('rm -rf' + prefix); # Ensure directory is empty
    os.system('mkdir -p '+ prefix);
    
    # Make .melts file containing the starting composition you want to run
    # simulations on
    fp=open(prefix + '/sc.melts','w');
    for i in range(len(elements)):
        fp.write('Initial Composition: %s %.4f\n' %(elements[i],composition[i]));
    for i in range(len(telements)):
        fp.write('Initial Trace: %s %.4f\n' %(telements[i],tsc[i]));
        
    fp.write('Initial Temperature: %.2f\nInitial Pressure: %.2f\nlog fo2 Path: %s\n' %(T_range[0],P_range[0],fo2path));
    
    for i in range(len(fractionate)):
        fp.write('Fractionate: %s\n' %(fractionate[i]));
    for i in range(len(supress)):
        fp.write('Suppress: %s\n' %(supress[i])); 
    fp.close();
    
    
    # Make melts_env file to specify type of MELTS calculation
    fp=open(prefix + '/melts_env.txt','w');
    fp.write('! *************************************\n!  Python-generated environment file\n! *************************************\n\n' + \
        '! this variable chooses MELTS or pMELTS; for low-pressure use MELTS\n' + \
        'ALPHAMELTS_VERSION		%s\n\n' %(version) + \
        '! do not use this unless fO2 anomalies at the solidus are a problem\n' + \
        '!ALPHAMELTS_ALTERNATIVE_FO2	true\n\n' + \
        '! use this if you want to buffer fO2 for isentropic, isenthalpic or isochoric mode\n! e.g. if you are doing isenthalpic AFC\n' + \
        '!ALPHAMELTS_IMPOSE_FO2		true\n\n' + \
        '! use if you want assimilation and fractional crystallization (AFC)\n' + \
        '!ALPHAMELTS_ASSIMILATE		true\n\n' + \
        '! isothermal, isobaric, isentropic, isenthalpic, isochoric, geothermal or PTPath\n' + \
        'ALPHAMELTS_MODE			%s\n' %(mode) + \
        '!ALPHAMELTS_PTPATH_FILE		ptpath.txt\n\n' + \
        '! need to set DELTAP for polybaric paths; DELTAT for isobaric paths\nALPHAMELTS_DELTAP	%.0f\n' %(dP) + \
        'ALPHAMELTS_DELTAT	%.0f\n' %(dT) + \
        'ALPHAMELTS_MAXP		%.0f\n' %(Pmax) + \
        'ALPHAMELTS_MINP		%.0f\n' %(Pmin) + \
        'ALPHAMELTS_MAXT		%.0f\n' %(Tmax) + \
        'ALPHAMELTS_MINT		%.0f\n\n' %(Tmin) + \
        '! this one turns on fractional crystallization for all solids\n! use Fractionate: in the melts file instead for selective fractionation\n' + \
        '%sALPHAMELTS_FRACTIONATE_SOLIDS	true\n' %(fractionatesolids) + \
        '%sALPHAMELTS_MASSIN		%g\n\n' %(fractionatesolids,massin) + \
        '! free water is unlikely but can be extracted\n' + \
        '%sALPHAMELTS_FRACTIONATE_WATER	true\n' %(fractionatewater) + \
        '%sALPHAMELTS_MINW			0.005\n\n' %(fractionatewater) + \
        '! the next one gives an output file that is always updated, even for single calculations\n' + \
        '%sALPHAMELTS_SAVE_ALL		true\n' %(saveall)+ \
        '!ALPHAMELTS_SKIP_FAILURE		true\n\n' + \
        '! this option converts the output temperature to celcius, like the input\n' + \
        '%sALPHAMELTS_CELSIUS_OUTPUT	true\n\n' %(celciusoutput) + \
        '! the next two turn on and off fractional melting\n' + \
        '%sALPHAMELTS_CONTINUOUS_MELTING	true\n' %(continuous) + \
        '%sALPHAMELTS_MINF			%g\n' %(continuous,minf) + \
        '%sALPHAMELTS_INTEGRATE_FILE	integrate.txt\n\n' %(continuous) + \
        '! the next two options refer to the trace element engine\n' + \
        '%sALPHAMELTS_DO_TRACE		true\n' %(dotrace)+ \
        '%sALPHAMELTS_DO_TRACE_H2O		true\n' %(dotraceh2o));
    fp.close();
    
    # Make a batch file to run the above .melts file starting from the liquidus
    fp = open(prefix + '/batch.txt','w');
    fp.write(batchstring);
    fp.close();
    
    # Run the command
    # Edit the following line(s to make sure you have a correct path to the 'run_alphamelts.command' perl script
    os.system('cd ' + prefix  + '; ' + meltspath + ' -f melts_env.txt -b batch.txt');
        
#    # Import the results
#    if exist([prefix '/Phase_main_tbl.txt'],'file')
#        cells=importc([prefix '/Phase_main_tbl.txt'],' ');
#        emptycols=all(cellfun('isempty', cells),1);
#        cells=cells(:,~emptycols);
#        pos=[find(all(cellfun('isempty', cells),2)); size(cells,1)+1];
#        melts.minerals=cell(length(pos)-1,1);
#        for i=1:(length(pos)-1)
#            name=varname(cells(pos(i)+1,1));
#            melts.(name{1}).elements=varname(cells(pos(i)+2,~cellfun('isempty',cells(pos(i)+2,:))));
#            melts.(name{1}).data=str2double(cells(pos(i)+3:pos(i+1)-1,1:length(melts.(name{1}).elements)));
#            if elementout; melts.(name{1})=elementify(melts.(name{1})); end
#            melts.minerals(i)=name;
#        end
#    else
#        melts=[];
#    end
    return
    
