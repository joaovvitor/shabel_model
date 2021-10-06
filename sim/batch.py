from netpyne.batch import Batch
from netpyne import specs
import numpy as np

def changeIClamp():
    # params
    params = specs.ODict()
    params['clampAmplitude']=[0.05, 0.1, 0.2, 0.4, 0.6]
    params['stimDur']=[10, 100, 200, 500, 1000]
    initCfg = {}

    initCfg['addIClamp']=True
    
    initCfg[('savePlots')]=True # skips saving the figures for each simulation
    initCfg[('saveJson')]=True # skips saving the figures for each simulation
    initCfg[('hParams', 'celsius')] = 37
    
    # groupedParams
    groupedParams = [] 

    # batch
    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg_file.py', initCfg=initCfg, groupedParams=groupedParams)
    return b

def changeNetStims():
    '''
    # NetStim inputs:
    
    cfg.numStims            = 200
    cfg.netWeight           = 0.2
    cfg.startStimTime       = 1000
    cfg.interStimInterval   =0.25
    '''

    # params
    params = specs.ODict()
    params['netWeight']=[ 0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.15, 0.5]
    params['interStimInterval'] = [ 5, 2.5, 1, 0.5, 0.1]
    initCfg = {}
    
    initCfg['addNetStim']=True

    initCfg[('savePlots')]=True # skips saving the figures for each simulation
    initCfg[('saveJson')]=True # skips saving the figures for each simulation
    initCfg[('hParams', 'celsius')] = 37
    
    # groupedParams
    groupedParams = [] 

    # batch
    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg_file.py', initCfg=initCfg, groupedParams=groupedParams)
    return b

def changeCellParameters():
    '''
    # Line to modify the cellParams in netParams.py
    #  netParams.cellParams['CT5A_reduced']['secs']['soma']['mechs']['pas']['e']=cfg.changeBaseline
    '''
    # params
    params = specs.ODict()
    params['changeBaseline']=[ -90, -80, -70, -60, -50, -40]
    params['netWeight']=[ 0.1, 0.15]

    initCfg = {}
    
    initCfg[('savePlots')]=True # skips saving the figures for each simulation
    initCfg[('saveJson')]=True # skips saving the figures for each simulation
    initCfg[('hParams', 'celsius')] = 37
    
    # groupedParams
    groupedParams = [] 

    # batch
    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg_file.py', initCfg=initCfg, groupedParams=groupedParams)
    return b

def changeNetworkParameters():
    '''
    # Line to modify the cell number in netParams.py
    netParams.popParams['neuron_CT5A']      =   {'cellModel': 'HH_reduced', 'cellType': 'CT5A_reduced',     'yRange': layer['test_layer'],  'numCells':cfg.numcells}
    '''
    # params
    params = specs.ODict()
    params['numcells']=[ 1, 5, 10]
    
    initCfg = {}
    
    initCfg[('savePlots')]=True # skips saving the figures for each simulation
    initCfg[('saveJson')]=True # skips saving the figures for each simulation
    initCfg[('hParams', 'celsius')] = 37
    
    # groupedParams
    groupedParams = [] 

    # batch
    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg_file.py', initCfg=initCfg, groupedParams=groupedParams)
    return b

def changeGroupedParameters():
    # params
    params = specs.ODict()
    # params['']=[ , ]
    
    initCfg = {}
    
    initCfg[('savePlots')]=True # skips saving the figures for each simulation
    initCfg[('saveJson')]=True # skips saving the figures for each simulation
    initCfg[('hParams', 'celsius')] = 37
    
    # groupedParams
    groupedParams = [] 

    # batch
    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg_file.py', initCfg=initCfg, groupedParams=groupedParams)
    return b

def changeManyParameters():
    # params
    params = specs.ODict()
    # params['']=[ , ]
    
    initCfg = {}
    
    initCfg[('savePlots')]=True # skips saving the figures for each simulation
    initCfg[('saveJson')]=True # skips saving the figures for each simulation
    initCfg[('hParams', 'celsius')] = 37
    
    # groupedParams
    groupedParams = [] 

    # batch
    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg_file.py', initCfg=initCfg, groupedParams=groupedParams)
    return b



# ----------------------------------------------------------------------------------------------
# Run configurations
# ----------------------------------------------------------------------------------------------
def setRunCfg(b, type='mpi'):
    if type=='mpi_jv':
        b.runCfg = {'type': 'mpi_bulletin', 
                    'script': init_script, 
                    'skip': True} # skip sims that already exist
    else:
        b.runCfg = {'type': 'mpi', 
                    'script': 'init.py', 
                    'skip': True} # skip sims that already exist

# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------


# --- Folder Structure 
# simDataFolder   = '../data'  # local
simDataFolder   = '/content/batch_sim_tutorial/data'   # google colab
simLabel        = 'CT5A_cell'
simDate         = '2021_05_21'
simCode         = 'tune_001'
#   simDataFolder/simLabel/simDate/simType/simType_simCode

# --- Simulation Profiles
# b = changeIClamp();             simType = 'IClamp'
# b = changeNetStims();           simType = 'NetStims'
b = changeCellParameters();     simType = 'CellMod'
# b = changeNetworkParameters();  simType = 'NetMod'
# b = changeGroupedParameters();  simType = 'GroupMod'
# b = changeManyParameters();     simType = 'ParamExpl'

b.dataFolder    = simDataFolder
b.date          = simDate

mpi_type = 'mpi_jv' 
init_script 	= 'init.py'

b.batchLabel    = simCode
b.saveFolder    = b.dataFolder + '/' + simType+'_' +  b.batchLabel

b.method        = 'grid'
setRunCfg(b, mpi_type)
b.run() # run batch