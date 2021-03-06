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

# creates a NEURON object with all the matching  
cfg.createNEURONObj = True
cfg.createPyStruct = True  

# prints the progress of the simulation with the defined interval
cfg.printRunTime = 0.1

# do not worry about these
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
                    'V_spine0_0': {'sec':'spine0_0', 'loc':0.5, 'var':'v'},
                    'V_spine4_2': {'sec':'spine4_2', 'loc':0.5, 'var':'v'},
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

    cfg.analysis['plotRaster'] = {'saveFig':True}
    
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

cfg.otherSecsList=[ 'soma',
                    'ah', 
                    'is', 
                    'axon'
                ]

cfg.dendList=[
                'dend0_0', 
                'dend0_1', 
                'dend0_2', 
                'dend0_3', 
                'dend1_0', 
                'dend1_1', 
                'dend1_2', 
                'dend1_3', 
                'dend2_0', 
                'dend2_1', 
                'dend2_2', 
                'dend2_3', 
                'dend3_0', 
                'dend3_1', 
                'dend3_2', 
                'dend3_3', 
                'dend4_0', 
                'dend4_1', 
                'dend4_2', 
                'dend4_3'
            ]

cfg.neckList=[
                'neck0_0',
                'neck0_1',
                'neck0_2',
                'neck0_3',
                'neck1_0',
                'neck1_1', 
                'neck1_2', 
                'neck1_3', 
                'neck2_0', 
                'neck2_1', 
                'neck2_2', 
                'neck2_3', 
                'neck3_0', 
                'neck3_1', 
                'neck3_2', 
                'neck3_3', 
                'neck4_0', 
                'neck4_1', 
                'neck4_2', 
                'neck4_3'
            ]

cfg.spineList=[
                'spine0_0', 
                'spine0_1', 
                'spine0_2', 
                'spine0_3', 
                'spine1_0', 
                'spine1_1', 
                'spine1_2', 
                'spine1_3', 
                'spine2_0', 
                'spine2_1', 
                'spine2_2', 
                'spine2_3', 
                'spine3_0', 
                'spine3_1', 
                'spine3_2', 
                'spine3_3', 
                'spine4_0', 
                'spine4_1', 
                'spine4_2', 
                'spine4_3'
            ]

cfg.spineList2=[
                'spine0_0', 
                'spine0_1', 
                ]

#------------------------------------------------------------------------------
# Synapses
#------------------------------------------------------------------------------

# Use this space to specify synaptic modifications

#------------------------------------------------------------------------------
# Network 
#------------------------------------------------------------------------------
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

cfg.addNetStim=False
if cfg.addNetStim:
    
    cfg.numStims    = 200
    cfg.netWeight   = 0.5
    cfg.startStimTime = 250
    cfg.interStimInterval=1000/50

    cfg.NetStim0    = { 'pop':              'CoCell_pop', 
                        'ynorm':            [0,1], 
                        # 'sec':              'soma', 
                        'sec':              'soma', 
                        'loc':              0.5, 
                        'synMech':          ['AMPA'], 
                        'synMechWeightFactor': [1],
                        # 'synMech':          ['GABAA'], 
                        # 'synMechWeightFactor': [1],
                        # 'synMech':          ['AMPA','GABAA'], 
                        # 'synMechWeightFactor': [0.9,0.1],
                        'start':            cfg.startStimTime, 
                        'interval':         cfg.interStimInterval, 
                        'noise':            1, 
                        'number':           cfg.numStims, 
                        'weight':           cfg.netWeight, 
                        'delay':            0}

#------------------------------------------------------------------------------
# ManySecs_NetStim inputs - Modified to provide inputs to a list of sections within the same cell
# Pass a list of sections to 'secList' instead of a single section to 'sec'
#------------------------------------------------------------------------------

cfg.addManySecs_NetStim=True
if cfg.addManySecs_NetStim:

    cfg.synMech = None
    cfg.synMechWF = None

    # cfg.synMech = ['AMPA']
    # cfg.synMechWF = [1]
    # cfg.synMech = ['GABAA']
    # cfg.synMechWF = [1]
    # cfg.synMech = ['AMPA','GABAA']
    # cfg.synMechWF = [0.5,0.5]
    
    cfg.startStimTime = 250
    cfg.interStimInterval=1000/50
    
    cfg.numStims    = 200
    cfg.netWeight   = 0.01

    # for i in range(cfg.spineList):
    #     cfg.ManySecs_NetStim[i] = {}

    cfg.ManySecs_NetStim0   = { 'pop':              'CoCell_pop', 
                                'ynorm':            [0,1], 
                                # 'sec':              'soma', 
                                'secList':          cfg.spineList, 
                                'loc':              0.5, 
                                'synMech':          cfg.synMech, 
                                'synMechWeightFactor': cfg.synMechWF, 
                                # 'synMech':          ['GABAA'], 
                                # 'synMechWeightFactor': [1],
                                # 'synMech':          ['AMPA','GABAA'], 
                                # 'synMechWeightFactor': [0.5,0.5],
                                'start':            cfg.startStimTime, 
                                'interval':         cfg.interStimInterval, 
                                'noise':            1, 
                                'number':           cfg.numStims, 
                                'weight':           cfg.netWeight, 
                                'delay':            0}

    # cfg.ManySecs_NetStim2   = { 'pop':              'CoCell_pop', 
    #                             'ynorm':            [0,1], 
    #                             # 'sec':              'soma', 
    #                             'secList':          cfg.spineList2, 
    #                             'loc':              0.5, 
    #                             'synMech':          cfg.synMech, 
    #                             'synMechWeightFactor': cfg.synMechWF, 
    #                             # 'synMech':          ['GABAA'], 
    #                             # 'synMechWeightFactor': [1],
    #                             # 'synMech':          ['AMPA','GABAA'], 
    #                             # 'synMechWeightFactor': [0.5,0.5],
    #                             'start':            cfg.startStimTime, 
    #                             'interval':         cfg.interStimInterval, 
    #                             'noise':            1, 
    #                             'number':           cfg.numStims, 
    #                             'weight':           cfg.netWeight, 
    #                             'delay':            0}
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

'''
LOOK AT M1 FOR EXAMPLE OF CODE
popParams of netstims

connParams with synsperconn=numspines and sec=spine list 

can also be individual GABA and AMPA instead of together

FOLLOW NEURON INSTALLATION FOR WINDOWS
THEN TRY TO INSTALL NETPYNE AFTER NEURON IS SETUP (MUCH EASIER)

'''