#! /usr/bin/python3
"""
cfg.py 

High-level specifications for thalamus model using NetPyNE

Contributors: joao.moreira@downstate.edu, salvadordura@gmail.com
"""

from netpyne import specs
import pickle

cfg = specs.SimConfig()

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

cfg.simType='batch_tutorial'

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.startStimTime = 0 # TEMPORARY - IMPROVE THIS CODE

cfg.duration = 2*1e3			## Duration of the sim, in ms -- value from M1 cfg.py 
cfg.dt = 0.025                  ## Internal Integration Time Step -- value from M1 cfg.py 
cfg.verbose = True              ## Show detailed messages
cfg.hParams = {'celsius': 34, 'v_init': -70}  
cfg.createNEURONObj = True
cfg.createPyStruct = True  
cfg.printRunTime = 0.1

cfg.connRandomSecFromList = False  # set to false for reproducibility 
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.oneSynPerNetcon = False
cfg.includeParamsLabel = False
cfg.printPopAvgRates = [0, cfg.duration]

cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.checkErrors = 0 #### 0 == False?

#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
cfg.allpops = [
                'CoCell_pop',
                ]

# cfg.recordCells = [(pop,0) for pop in cfg.allpops]

cfg.recordTraces = {
                    'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'},
                    # 'i_soma':{'sec':'soma','loc':0.5,'var':'i_membrane_'},
                    # 'i_pas': {'sec':'soma', 'loc':0.5, 'mech':'pas', 'var':'i'},
                    # 'i_h': {'sec':'soma', 'loc':0.5, 'mech':'ih', 'var':'i'},
                    # 'i_nax': {'sec':'soma', 'loc':0.5, 'mech':'nax', 'var':'ina'},
                    # 'i_cadad': {'sec':'soma', 'loc':0.5, 'mech':'cadad', 'var':'cai'},
                    # 'i_kl': {'sec':'soma', 'loc':0.5, 'mech':'kl', 'var':'i'},                    
                    }  ## Dict with traces to record -- taken from M1 cfg.py 
cfg.recordStim = False			
cfg.recordTime = False  		
cfg.recordStep = cfg.dt      

#cfg.recordLFP = [[-15, 500, 100]] #[[200, y, 200] for y in range(0, 2000, 400)]+[[200, 2500, 200], [200,2700,200]]

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel            = 'CoCell_'+cfg.simType
cfg.saveFolder          = '../data/CoCell'
cfg.savePickle          = False
cfg.saveJson            = False
cfg.saveDataInclude     = ['simData', 'simConfig', 'netParams']#, 'net']
cfg.backupCfgFile       = None #['cfg.py', 'backupcfg/'] 
cfg.gatherOnlySimData   = False
cfg.saveCellSecs        = True # needs to be true if you want to access the membrane current (sim.net.cells[0].secs['soma'](0.5).i_membrane)
cfg.saveCellConns       = True

cfg.use_fast_imem       = True # RECORD MEMBRANE CURRENT

#------------------------------------------------------------------------------
# Analysis and plotting 
#----------------------------------------------------------------------------- 
cfg.savePlots=True
if cfg.savePlots:
    cfg.analysis['plotTraces'] = {  
                                    # 'include': [0,10,19,20,30,39], 
                                    # 'include': [(pop, 0) for pop in cfg.allpops], 
                                    'include': [(pop, x) for x in range(0,10,1) for pop in cfg.allpops], 
                                    # 'include': [(pop, x) for x in range(0,101,10) for pop in cfg.allpops], 
                                    # 'timeRange': [2900,4250],
                                    # 'timeRange': [0,cfg.duration],
                                    'ylim': [-85, 60],
                                    'oneFigPer': 'cell', 
                                    # 'oneFigPer': 'trace', 
                                    'overlay': False, 
                                    'saveFig': True, 
                                    'showFig': True, 
                                    'figSize': (40,16)}

    # cfg.analysis['plot2Dnet']   = { 'saveFig': True, 'figSize': (20,15)}   # Plot 2D net cells and connections

    # cfg.analysis['plotRaster'] = {'saveFig':True, 'orderInverse': True, 'popRates' : True, 'figSize': (40,30)}#, 'orderBy': 'y'}#, 'dpi':2000}

    # cfg.analysis['plotConn']  = {'saveFig': True}#,'logPlot': True}        # plot connectivity matrix

    # cfg.analysis['plot2Dfiring']={'saveFig': True}

    cfg.analysis['plotShape'] = {'saveFig':True}

#------------------------------------------------------------------------------
# Cells
#------------------------------------------------------------------------------

# Use this space to specify cell modifications
cfg.saveCellParams=False
cfg.changeBaseline = -70 # default
cfg.numcells = 1

#------------------------------------------------------------------------------
# Synapses
#------------------------------------------------------------------------------

# Use this space to specify synaptic modifications

#------------------------------------------------------------------------------
# Network 
#------------------------------------------------------------------------------
cfg.singleCellPops = 0 # Create pops with 1 single cell (to debug)
cfg.singlePop = 0
cfg.weightNorm = 1      # ADDED AS TRUE BECAUSE IN CFG.PY IT ALWAYS EXECUTES THIS LINE IN NETPARAMS.PY
cfg.weightNormThreshold = 4.0  # weight normalization factor threshold
cfg.connectNetwork = True

cfg.scale = 1.0
cfg.sizeY = 1350.0  # CHECK SIZES - 2020-11-11
cfg.sizeX = 300.0   # CHECK SIZES - 2020-11-11
cfg.sizeZ = 300.0   # CHECK SIZES - 2020-11-11
cfg.scaleDensity = 1

#------------------------------------------------------------------------------
#
# INPUTS CONFIGURATION
#
#------------------------------------------------------------------------------
'''
#------------------------------------------------------------------------------
# Current inputs 
#------------------------------------------------------------------------------
cfg.addIClamp=False
if cfg.addIClamp:
    cfg.startStimTime = 500
    cfg.clampAmplitude=0.1
    cfg.stimDur=500
    
    cfg.IClamp0 = { 'pop': 'CoCell_pop', 'sec': 'soma', 'loc': 0.5, 'start': 400, 'dur': 100, 'amp': cfg.clampAmplitude}

cfg.addPreIClamp = False
if cfg.addPreIClamp:
    cfg.startStimTime = 0
    cfg.stimDur_pre = None
    cfg.clampAmplitude_pre = -0.1

    cfg.PreIClamp0 = { 'pop': 'CoCell_pop', 'sec': 'soma', 'loc': 0.5, 'start': 400, 'dur': 150, 'amp': cfg.clampAmplitude_pre}
'''
#------------------------------------------------------------------------------
# NetStim inputs 
#------------------------------------------------------------------------------
cfg.addNetStim=True
if cfg.addNetStim:
    
    cfg.numStims    = 200
    cfg.netWeight   = 0.02
    cfg.startStimTime = 250
    cfg.interStimInterval=1000/50

    cfg.NetStim1    = { 'pop':              'CoCell_pop', 
                        'ynorm':            [0,1], 
                        'sec':              'soma', 
                        'loc':              0.5, 
                        'synMech':          ['AMPA','GABAA'], 
                        'synMechWeightFactor': [0.5,0.5],
                        'start':            cfg.startStimTime, 
                        'interval':         cfg.interStimInterval, 
                        'noise':            1, 
                        'number':           cfg.numStims, 
                        'weight':           cfg.netWeight, 
                        'delay':            0}
'''
#------------------------------------------------------------------------------
# Targeted NetStim inputs 
#------------------------------------------------------------------------------
cfg.addTargetedNetStim=False
if cfg.addTargetedNetStim:
    
    cfg.startStimTime=None
    cfg.stimPop = None
    cfg.netWeight           = 1
    cfg.numStims            = 1
    cfg.interStimInterval   = 100

    cfg.TargetedNetStim00= { 
                        'pop':              'neuron_CT5A', 
                        'ynorm':            [0,1], 
                        'sec':              'soma', 
                        'loc':              0.5, 
                        'synMech':          ['AMPA'], 
                        'synMechWeightFactor': [1.0],
                        'start':            2000, 
                        'interval':         cfg.interStimInterval, 
                        'noise':            0, 
                        'number':           cfg.numStims, 
                        'weight':           cfg.netWeight, 
                        'delay':            0,
                        'targetCells':      [0]
                        }

#------------------------------------------------------------------------------
# GroupNetStim inputs
#------------------------------------------------------------------------------
cfg.addGroupNetStim = False
if cfg.addGroupNetStim:
    cfg.groupWeight = 0.1
    cfg.groupRate = 1000/cfg.interStimInterval

    cfg.GroupNetStimW1  = { 'nstype':       'pop', 
                            'numStims':     200, 
                            'pop':          'neuron_CT5A', 
                            'ynorm':        [0,1], 
                            'cellRule':     'CT5A_reduced', 
                            'secList':      'soma', 
                            'allSegs':      True, \
                            # 'synMech': ['AMPA'], 
                            'synMech':      ['AMPA','NMDA'], 
                            'start':        500, 
                            'interval':     1000/cfg.groupRate, 
                            'noise':        0.6, 
                            'number':       1, 
                            'weight':       cfg.groupWeight , 
                            'delay':        0}
'''