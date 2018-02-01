# Import some useful packages
import os # os.system lets us access the command line
import re # Regular expressions, for cleaning up column names
import pandas as pd # Pandas, for importing PerpleX text file output as data frames

############################ Function definitions ###############################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Set up a PerpleX calculation for a single bulk composition along a specified 
# geothermal gradient and pressure (depth) range. P specified in bar and T_surf
# in Kelvin, with geothermal gradient in units of Kelvin/bar
def configure_geotherm(perplexdir, scratchdir, composition, elements = ['SIO2','TIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O','H2O'], index = 1, P_range = [280,28000], T_surf = 273.15, geotherm = 0.1, dataset = 'hp02ver.dat', solution_phases = 'O(HP)\nOpx(HP)\nOmph(GHP)\nGt(HP)\noAmph(DP)\ncAmph(DP)\nT\nB\nChl(HP)\nBio(TCC)\nMica(CF)\nCtd(HP)\nIlHm(A)\nSp(HP)\nSapp(HP)\nSt(HP)\nfeldspar_B\nDo(HP)\nF\n', excludes = 'ts\nparg\ngl\nged\nfanth\ng\n'):
    build = perplexdir + 'build'; # path to PerpleX build
    vertex = perplexdir + 'vertex'; # path to PerpleX vertex

    #Configure working directory
    prefix = scratchdir + 'out_%i/' %(index);
    os.system('rm -rf %s; mkdir -p %s' %(prefix, prefix));
    
    # Place required data files
    os.system('cp %s%s %s' %(perplexdir, dataset, prefix));
    os.system('cp %sperplex_option.dat %s' %(perplexdir, prefix));
    os.system('cp %ssolution_model.dat %s' %(perplexdir, prefix));

    # Create build batch file
    fp=open(prefix + 'build.bat','w');
    # Name, components, and basic options. Holland and Powell (1998) 'CORK' fluid equation state.
    elementstring = '';
    for e in elements:
        elementstring = elementstring + e.upper() + '\n'
    fp.write('%i\n%s\nperplex_option.dat\nn\nn\nn\nn\n%s\n5\n' %(index, dataset, elementstring));
    # Pressure gradient details
    fp.write('3\nn\ny\n2\n1\n%g\n%g\n%g\n%g\ny\n' %(T_surf, geotherm, P_range[0],P_range[1]));
    # Whole-rock composition
    for i in range(len(composition)):
        fp.write('%g ' %(composition[i]));
    # Solution model
    fp.write('\nn\ny\nn\n' + excludes + '\ny\nsolution_model.dat\n' + solution_phases + '\nGeothermal');    
    fp.close();
    
    # build PerpleX problem definition
    os.system('cd %s; %s < build.bat > /dev/null' %(prefix, build));
    
    # Run PerpleX vertex calculations
    os.system('cd %s; echo %i | %s > /dev/null' %(prefix, index, vertex));
    
    return;

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Set up a PerpleX calculation for a single bulk composition along a specified 
# isobaric temperature gradient. P specified in bar and T_range in Kelvin
def configure_isobaric(perplexdir, scratchdir, composition, elements = ['SIO2','TIO2','AL2O3','FEO','MGO','CAO','NA2O','K2O','H2O'], index = 1, P = 10000, T_range = [500+273.15, 1500+273.15], dataset = 'hp11ver.dat', solution_phases = 'O(HP)\nOpx(HP)\nOmph(GHP)\nGt(HP)\noAmph(DP)\ncAmph(DP)\nT\nB\nChl(HP)\nBio(TCC)\nMica(CF)\nCtd(HP)\nIlHm(A)\nSp(HP)\nSapp(HP)\nSt(HP)\nfeldspar_B\nDo(HP)\nF\n', excludes = 'ts\nparg\ngl\nged\nfanth\ng\n'):
    build = perplexdir + 'build'; # path to PerpleX build
    vertex = perplexdir + 'vertex'; # path to PerpleX vertex

    #Configure working directory
    prefix = scratchdir + 'out_%i/' %(index);
    os.system('rm -rf %s; mkdir -p %s' %(prefix, prefix));
    
    # Place required data files
    os.system('cp %s%s %s' %(perplexdir, dataset, prefix));
    os.system('cp %sperplex_option.dat %s' %(perplexdir, prefix));
    os.system('cp %ssolution_model.dat %s' %(perplexdir, prefix));

    # Create build batch file
    fp=open(prefix + 'build.bat','w');
    # Name, components, and basic options. Holland and Powell (1998) 'CORK' fluid equation state.
    elementstring = '';
    for e in elements:
        elementstring = elementstring + e.upper() + '\n'
    fp.write('%i\n%s\nperplex_option.dat\nn\nn\nn\nn\n%s\n5\n' %(index, dataset, elementstring));
    # Pressure gradient details
    fp.write('3\nn\nn\n2\n%g\n%g\n%g\ny\n' %(T_range[0],T_range[1],P));
    # Whole-rock composition
    for i in range(len(composition)):
        fp.write('%g ' %(composition[i]));
    # Solution model
    fp.write('\nn\ny\nn\n' + excludes + '\ny\nsolution_model.dat\n' + solution_phases + '\nIsobaric');    
    fp.close();
    
    # build PerpleX problem definition
    os.system('cd %s; %s < build.bat > /dev/null' %(prefix, build));
    
    # Run PerpleX vertex calculations
    os.system('cd %s; echo %i | %s > /dev/null' %(prefix, index, vertex));
    
    return;

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Query perplex results at a single pressure on a geotherm. Results are returned
# as string read from perplex text file output  
def query_geotherm(perplexdir, scratchdir, index, P):
    werami = perplexdir + 'werami'; # path to PerpleX werami
    prefix = scratchdir + 'out_%i/' %(index); # path to data files
    
    # Sanitize P inputs to avoid PerpleX escape sequence
    if P == 999:
        P = 999.001;
    
    # Create werami batch file
    fp=open(prefix + 'werami.bat','w');
    fp.write('%i\n1\n%g\n999\n0\n' %(index,P))
    fp.close();
    
    # Make sure there isn't already an output
    os.system('rm -f %s%i_1.txt' %(prefix, index));
    
    # Extract Perplex results with werami
    os.system('cd %s; %s < werami.bat > /dev/null' %(prefix, werami));
    
    # Read results and return them if possible
    try:
        fp = open(prefix + '%i_1.txt' %(index),'r');
        data = fp.read(); 
        fp.close();
    except:
        data = '';
    return data;

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Query perplex seismic results along a geotherm
def query_geotherm_seismic(perplexdir, scratchdir, index = 1, P_range = [284.2, 28420], npoints = 100):
    werami = perplexdir + 'werami'; # path to PerpleX werami
    prefix = scratchdir + 'out_%i/' %(index); # path to data files
    n_header_lines = 8;

    # Create werami batch file
    fp=open(prefix + 'werami.bat','w');
    fp.write('%i\n3\n1\n%g\n%g\n%i\n2\nn\nn\n13\nn\nn\n15\nn\nn\n0\n0\n' %(index, P_range[0], P_range[1], npoints));
    fp.close();
    
    # Make sure there isn't already an output
    os.system('rm -f %s%i_1.tab' %(prefix, index));
    
    # Extract Perplex results with werami
    os.system('cd %s; %s < werami.bat > /dev/null' %(prefix, werami));
    
    # Read results and return them if possible
    try:
        data = pd.read_csv(prefix + '%i_1.tab' %(index), delim_whitespace=True, header=n_header_lines)
    except:
        data = 0;
    return data;

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Query perplex results at a single temperature on an isobar. Results are 
# returned as string read from perplex text file output
def query_isobar(perplexdir, scratchdir, index, T):
    werami = perplexdir + 'werami'; # path to PerpleX werami
    prefix = scratchdir + 'out_%i/' %(index); # path to data files
    
    # Sanitize T inputs to avoid PerpleX escape sequence
    if T == 999:
        T = 999.001;
    
    # Create werami batch file
    fp=open(prefix + 'werami.bat','w');
    fp.write('%i\n1\n%g\n999\n0\n' %(index,T))
    fp.close();
    
    # Make sure there isn't already an output
    os.system('rm -f %s%i_1.txt' %(prefix, index));
    
    # Extract Perplex results with werami
    os.system('cd %s; %s < werami.bat > /dev/null' %(prefix, werami));
    
    # Read results and return them if possible
    try:
        fp = open(prefix + '%i_1.txt' %(index),'r');
        data = fp.read(); 
        fp.close();
    except:
        data = '';
    return data;

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Query perplex results for a specified phase along an entire isobar. Results
# are returned as a pandas DataFrame
def query_isobar_phase(perplexdir, scratchdir, index, T_range, npoints, phase = 'melt(G)', include_fluid = 'y', clean_units = True):
    werami = perplexdir + 'werami'; # path to PerpleX werami
    prefix = scratchdir + 'out_%i/' %(index); # path to data files
    n_header_lines = 8;

    # Create werami batch file
    fp=open(prefix + 'werami.bat','w');
    fp.write('%i\n3\n1\n%g\n%g\n%i\n36\n2\n%s\n%s\n0\n' %(index, T_range[0], T_range[1], npoints, phase, include_fluid))
    fp.close();
    
    # Make sure there isn't already an output
    os.system('rm -f %s%i_1.tab' %(prefix, index));
    
    # Extract Perplex results with werami
    os.system('cd %s; %s < werami.bat > /dev/null' %(prefix, werami));
    
    # Read results and return them if possible
    try:
        data = pd.read_csv(prefix + '%i_1.tab' %(index), delim_whitespace=True, header=n_header_lines)
        if clean_units:
            data.columns = [cn.replace(',%','_pct') for cn in data.columns] # substutue _pct for ,% in column names
            data.columns =  [re.sub(',.*','',cn) for cn in data.columns] # Remove units from column names
            data.columns =  [re.sub('[{}]','',cn) for cn in data.columns] # Remove unnecessary {} from isochemical seismic derivatives
    except:
#        data = '';
        data = 0;
    return data;


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Query modal mineralogy along a given isobar. Results are returned as a pandas
# DataFrame.
def query_isobar_modes(perplexdir, scratchdir, index, T_range, npoints, include_fluid = 'y'):
    werami = perplexdir + 'werami'; # path to PerpleX werami
    prefix = scratchdir + 'out_%i/' %(index); # path to data files
    n_header_lines = 8;

    # Create werami batch file
    fp=open(prefix + 'werami.bat','w');
    fp.write('%i\n3\n1\n%g\n%g\n%i\n25\nn\n%s\n0\n' %(index, T_range[0], T_range[1], npoints, include_fluid))
    fp.close();
    
    # Make sure there isn't already an output
    os.system('rm -f %s%i_1.tab' %(prefix, index));
    
    # Extract Perplex results with werami
    os.system('cd %s; %s < werami.bat > /dev/null' %(prefix, werami));
    
    # Read results and return them if possible
    try:
        data = pd.read_csv(prefix + '%i_1.tab' %(index), delim_whitespace=True, header=n_header_lines)
    except:
        data = 0;
    return data;

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Query calculated system properties along an entire isobar. Results are returned
# as a pandas dataframe. Set include_fluid = 'n' to get solid+melt only
def query_isobar_system(perplexdir, scratchdir, index, T_range, npoints, include_fluid = 'y', clean_units = True):
    werami = perplexdir + 'werami'; # path to PerpleX werami
    prefix = scratchdir + 'out_%i/' %(index); # path to data files
    n_header_lines = 8;
    
    # Create werami batch file
    fp=open(prefix + 'werami.bat','w');
    fp.write('%i\n3\n1\n%g\n%g\n%i\n36\n1\n%s\n0\n' %(index, T_range[0], T_range[1], npoints, include_fluid))
    fp.close();
    
    # Make sure there isn't already an output
    os.system('rm -f %s%i_1.tab' %(prefix, index));
    
    # Extract Perplex results with werami
    os.system('cd %s; %s < werami.bat > /dev/null' %(prefix, werami));
    
    # Read results and return them if possible
    try:
        data = pd.read_csv(prefix + '%i_1.tab' %(index), delim_whitespace=True, header=n_header_lines)
        if clean_units:
            data.columns = [cn.replace(',%','_pct') for cn in data.columns] # substutue _pct for ,% in column names
            data.columns =  [re.sub(',.*','',cn) for cn in data.columns] # Remove units from column names
            data.columns =  [re.sub('[{}]','',cn) for cn in data.columns] # Remove unnecessary {} from isochemical seismic derivatives
    except:
        data = 0;
    return data;
        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #