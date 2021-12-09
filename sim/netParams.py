#! /usr/bin/python3
"""
netParams.py 

High-level specifications for thalamus model using NetPyNE

Contributors: joao.moreira@downstate.edu, salvadordura@gmail.com
"""

from netpyne import specs
import pickle, json

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg_file import cfg


#------------------------------------------------------------------------------
# VERSION 
#------------------------------------------------------------------------------
netParams.version = 'cell_000'

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
# Do not worry about these parameters
netParams.defaultThreshold = 0.0 # spike threshold, 10 mV is NetCon default, lower it for all cells
netParams.defineCellShapes = True # JV 2021-02-23 - Added to fix the lack of the pt3d term in the cells, which make it unable to record i_membrane_

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
layer = {'cell_layer': [0, 0.1]}  # normalized layer boundaries  

# Import model from HOC file
# cellRule=netParams.importCellParams(label='CoCell_HOC', fileName='../cells/corelease_netpyne.hoc', cellName='CoCell_Cell')
cellRule=netParams.importCellParams(label='CoCell_HOC', fileName='../cells/corelease_netpyne_just_cell.hoc', cellName='CoCell_Cell')
netParams.cellParams['CoCell_HOC']['conds']={}

netParams.saveCellParamsRule(label='CoCell_HOC', fileName='../cells/CoCell_HOC_cellParams.json')

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------

netParams.popParams['CoCell_pop']      =   {'cellType': 'CoCell_HOC',     'yRange': layer['cell_layer'],  'numCells':1}

#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------

# excitatory synapses
netParams.synMechParams['AMPA']             = {'mod': 'MyExp2SynBB',        'tau1': 0.05,   'tau2': 5.3,                    'e': 0}
# inhibitory synapses
netParams.synMechParams['GABAA']            = {'mod': 'MyExp2SynBB',        'tau1': 0.07,   'tau2': 18.2,                   'e': -80}

#------------------------------------------------------------------------------
# NetStim inputs - FROM CFG.PY
#------------------------------------------------------------------------------
if cfg.addNetStim:
    for key in [k for k in dir(cfg) if k.startswith('NetStim')]:
        params = getattr(cfg, key, None)
        [pop, sec, loc, synMech, synMechWeightFactor, start, interval, noise, number, weight, delay] = \
        [params[s] for s in ['pop', 'sec', 'loc', 'synMech', 'synMechWeightFactor', 'start', 'interval', 'noise', 'number', 'weight', 'delay']] 

        # add stim source
        netParams.stimSourceParams[key] = { 'type':     'NetStim', 
                                            'start':    cfg.startStimTime       if cfg.startStimTime is not None        else start, 
                                            'interval': cfg.interStimInterval   if cfg.interStimInterval is not None    else interval, 
                                            'noise':    noise, 
                                            'number':   cfg.numStims            if cfg.numStims is not None             else number}

        # netParams.stimSourceParams[key] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': sec, 
            'loc': loc,
            'synMech': synMech,
            # 'weight': weight,
            'weight': cfg.netWeight if cfg.netWeight is not None else weight,
            'synMechWeightFactor': synMechWeightFactor,
            'delay': delay}


if cfg.addManySecs_NetStim:
    for key in [k for k in dir(cfg) if k.startswith('ManySecs')]:
        params = getattr(cfg, key, None)
        [pop, secList, loc, synMech, synMechWeightFactor, start, interval, noise, number, weight, delay] = \
        [params[s] for s in ['pop', 'secList', 'loc', 'synMech', 'synMechWeightFactor', 'start', 'interval', 'noise', 'number', 'weight', 'delay']] 

        # add stim source
        netParams.stimSourceParams[key] = { 'type':     'NetStim', 
                                            'start':    cfg.startStimTime       if cfg.startStimTime is not None        else start, 
                                            'interval': cfg.interStimInterval   if cfg.interStimInterval is not None    else interval, 
                                            'noise':    noise, 
                                            'number':   cfg.numStims            if cfg.numStims is not None             else number}

        # netParams.stimSourceParams[key] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

        # connect stim source to target
        for sec in secList:
            netParams.stimTargetParams[key+'_'+pop+'_'+sec] =  {
                'source': key, 
                'conds': {'pop': pop},
                'sec': sec, 
                'loc': loc,
                'synMech': cfg.synMech if cfg.synMech is not None else synMech,
                # 'weight': weight,
                'weight': cfg.netWeight if cfg.netWeight is not None else weight,
                'synMechWeightFactor': cfg.synMechWF if cfg.synMechWF is not None else synMechWeightFactor,
                'delay': delay}