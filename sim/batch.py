from netpyne.batch import Batch
from netpyne import specs
import numpy as np

def changeWeight():
    # params
    params = specs.ODict()
    # params['synMech'] = [   ['AMPA'],
    #                         ['GABAA'],
    #                         ['AMPA','GABAA'],   
    #                         ['AMPA','GABAA'],
    #                         ['AMPA','GABAA'],
    #                         ]
    # params['synMechWF'] = [ [1],
    #                         [1],
    #                         [0.5,0.5],
    #                         [0.25,0.75],
    #                         [0.75,0.25],
    #                         ]
    
    params[('ManySecs_NetStim0','synMech')] = [             ['AMPA'],
                                                            ['GABAA'],
                                                            ['AMPA','GABAA'],   
                                                            ['AMPA','GABAA'],
                                                            ['AMPA','GABAA'],]
    params[('ManySecs_NetStim0','synMechWeightFactor')] = [ [1],
                                                            [1],
                                                            [0.5,0.5],
                                                            [0.25,0.75],
                                                            [0.75,0.25],
                                                            ]
    
    # params[('ManySecs_NetStim2','synMech')] = [['AMPA'],['GABAA']]
    # params[('ManySecs_NetStim2','synMechWeightFactor')] = [ [1],
    #                                                         [1]]
    # params['netWeight'] = [0.01, 0.05, 0.1]
    
    initCfg = {}

    initCfg['addManySecs_NetStim']=True
    
    initCfg[('savePlots')]=True     # FALSE: skips saving the figures for each simulation
    initCfg[('saveJson')]=True      # FALSE: skips saving the data file for each simulation
    
    # groupedParams
    # groupedParams = ['synMech','synMechWF'] 
    groupedParams = [   ('ManySecs_NetStim0','synMech'),('ManySecs_NetStim0','synMechWeightFactor')]
                        # [('ManySecs_NetStim2','synMech'),('ManySecs_NetStim2','synMechWeightFactor')]] 
    
    # batch
    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg_file.py', initCfg=initCfg, groupedParams=groupedParams)
    return b

# ----------------------------------------------------------------------------------------------
# Run configurations
# ----------------------------------------------------------------------------------------------
def setRunCfg(b):
    b.runCfg = {'type': 'mpi_bulletin', 
                        'script': 'init.py', 
                        'skip': True} # skip sims that already exist

# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------


# --- Folder Structure 
simDataFolder   = '../data'  # local
# simDataFolder   = '/content/batch_sim_tutorial/data'   # google colab
simLabel        = 'Sheibel_CoCell'
simDate         = '2021_10_13'
simCode         = 'tune_000'
#   simDataFolder/simLabel/simDate/simType/simType_simCode

# --- Simulation Profiles
b = changeWeight();             simType = 'ManySecs_NetStim'

b.dataFolder    = simDataFolder
b.date          = simDate

b.batchLabel    = simCode
b.saveFolder    = b.dataFolder + '/' + simType+'_' +  b.batchLabel

b.method        = 'grid'
setRunCfg(b)
b.run() # run batch

'''
mpiexec -n 6 nrniv -python -mpi batch.py

sudo git commit -a -m " "; sudo git push; sudo git pull
'''