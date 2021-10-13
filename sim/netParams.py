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
netParams.scale = cfg.scale # Scale factor for number of cells
netParams.sizeX = cfg.sizeX # x-dimension (horizontal length) size in um
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = cfg.sizeZ # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume

#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
netParams.scaleConnWeight = 1.0 # Connection weight scale factor (default if no model specified)
netParams.scaleConnWeightModels = {'HH_simple': 1.0, 'HH_reduced': 1.0, 'HH_full': 1.0} #scale conn weight factor for each cell model
netParams.scaleConnWeightNetStims = 1.0 #0.5  # scale conn weight factor for NetStims
netParams.defaultThreshold = 0.0 # spike threshold, 10 mV is NetCon default, lower it for all cells

### reevaluate these values
netParams.defaultDelay = 2.0 # default conn delay (ms) # DEFAULT
netParams.propVelocity = 500.0 # propagation velocity (um/ms)
netParams.probLambda = 100.0  # length constant (lambda) for connection probability decay (um)

### maybe add the edge effect parameter to compensate for the error form distance dependant conn
# netParams.correctBorder = {‘threshold’: [200, 40, 200]}

netParams.defineCellShapes = True # JV 2021-02-23 - Added to fix the lack of the pt3d term in the cells, which make it unable to record i_membrane_

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------

layer = {'test_layer': [0, 0.1]}  # normalized layer boundaries  

# Import model from HOC file

# cellRule=netParams.importCellParams(label='CoCell_HOC', fileName='../cells/corelease_netpyne.hoc', cellName='CoCell_Cell')
cellRule=netParams.importCellParams(label='CoCell_HOC', fileName='../cells/corelease_netpyne_just_cell.hoc', cellName='CoCell_Cell')
netParams.cellParams['CoCell_HOC']['conds']={}

netParams.saveCellParamsRule(label='CoCell_HOC', fileName='../cells/CoCell_HOC_cellParams.json')

#------------------------------------------------------------------------------
# Population parameters
#------------------------------------------------------------------------------

netParams.popParams['CoCell_pop']      =   {'cellType': 'CoCell_HOC',     'yRange': layer['test_layer'],  'numCells':1}

## CORTICAL NEURONS (from prev model)
# netParams.popParams['neuron_CT5A']      =   {'cellModel': 'HH_reduced', 'cellType': 'CT5A_reduced',     'yRange': layer['test_layer'],  'numCells':cfg.numcells}
# netParams.cellParams['CT5A_reduced']['secs']['soma']['mechs']['pas']['e']=cfg.changeBaseline

# sets the number of cells in each pop to 1 for testing
if cfg.singleCellPops:
    for popName,pop in netParams.popParams.items():
        if cfg.singlePop:
            if cfg.singlePop == popName:
                pop['numCells'] = 1
            else:
                pop['numCells'] = 0
        else:
            pop['numCells'] = 1

#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
# excitatory synapses
netParams.synMechParams['NMDA']             = {'mod': 'MyExp2SynNMDABB',    'tau1NMDA': 15, 'tau2NMDA': 150,                'e': 0}
netParams.synMechParams['AMPA']             = {'mod': 'MyExp2SynBB',        'tau1': 0.05,   'tau2': 5.3,                    'e': 0}
# inhibitory synapses
netParams.synMechParams['GABAB']            = {'mod': 'MyExp2SynBB',        'tau1': 3.5,    'tau2': 260.9,                  'e': -93} 
netParams.synMechParams['GABAA']            = {'mod': 'MyExp2SynBB',        'tau1': 0.07,   'tau2': 18.2,                   'e': -80}
netParams.synMechParams['GABAASlow']        = {'mod': 'MyExp2SynBB',        'tau1': 2,      'tau2': 100,                    'e': -80}
netParams.synMechParams['GABAASlowSlow']    = {'mod': 'MyExp2SynBB',        'tau1': 200,    'tau2': 400,                    'e': -80}

ESynMech    = ['AMPA', 'NMDA']
SOMESynMech = ['GABAASlow','GABAB']
SOMISynMech = ['GABAASlow']
PVSynMech   = ['GABAA']
NGFSynMech  = ['GABAA', 'GABAB']

# #------------------------------------------------------------------------------
# # Background Stimulation parameters
# #------------------------------------------------------------------------------

# netParams.stimSourceParams['Input_1'] = {'type': 'NetStim', 'rate': 10, 'start': 2000, 'noise': 1, 'number': 20}
# netParams.stimTargetParams['Input_1->TC'] = {'source': 'Input_1', 'sec':'soma', 'loc': 0.5, 'weight': '20+normal(0.2,0.05)', 'conds': {'pop': 'CT5A_S1','xnorm':[0,0.2]}, 'synMech':['AMPA']}

#------------------------------------------------------------------------------
# NetStim inputs - FROM CFG.PY
#------------------------------------------------------------------------------
if cfg.addNetStim:
    for key in [k for k in dir(cfg) if k.startswith('NetStim')]:
        params = getattr(cfg, key, None)
        [pop, sec, loc, synMech, synMechWeightFactor, start, interval, noise, number, weight, delay] = \
        [params[s] for s in ['pop', 'sec', 'loc', 'synMech', 'synMechWeightFactor', 'start', 'interval', 'noise', 'number', 'weight', 'delay']] 

        #cfg.analysis['plotTraces']['include'] = [(pop,0)]

        if synMech == ESynMech:
            wfrac = cfg.synWeightFractionEE
        elif synMech == SOMESynMech:
            wfrac = cfg.synWeightFractionSOME
        else:
            wfrac = [1.0]

        # add stim source
        netParams.stimSourceParams[key] = { 'type':     'NetStim', 
                                            'start':    cfg.startStimTime       if cfg.startStimTime is not None        else start, 
                                            'interval': cfg.interStimInterval   if cfg.interStimInterval is not None    else interval, 
                                            'noise':    noise, 
                                            'number':   cfg.numStims            if cfg.numStims is not None             else number}

        # netParams.stimSourceParams[key] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

        # connect stim source to target
        # for i, syn in enumerate(synMech):
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
    print('\n\n\nAdding NetStims to multiple sections\n\n\n')
    for key in [k for k in dir(cfg) if k.startswith('ManySecs')]:
        params = getattr(cfg, key, None)
        [pop, secList, loc, synMech, synMechWeightFactor, start, interval, noise, number, weight, delay] = \
        [params[s] for s in ['pop', 'secList', 'loc', 'synMech', 'synMechWeightFactor', 'start', 'interval', 'noise', 'number', 'weight', 'delay']] 

        #cfg.analysis['plotTraces']['include'] = [(pop,0)]

        if synMech == ESynMech:
            wfrac = cfg.synWeightFractionEE
        elif synMech == SOMESynMech:
            wfrac = cfg.synWeightFractionSOME
        else:
            wfrac = [1.0]

        # add stim source
        netParams.stimSourceParams[key] = { 'type':     'NetStim', 
                                            'start':    cfg.startStimTime       if cfg.startStimTime is not None        else start, 
                                            'interval': cfg.interStimInterval   if cfg.interStimInterval is not None    else interval, 
                                            'noise':    noise, 
                                            'number':   cfg.numStims            if cfg.numStims is not None             else number}

        # netParams.stimSourceParams[key] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

        # connect stim source to target
        # for i, syn in enumerate(synMech):
        # print(pop)
        # print(secList)
        for sec in secList:
            print(sec+'\n\n')
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


'''
#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
    for key in [k for k in dir(cfg) if k.startswith('IClamp')]:
        params = getattr(cfg, key, None)
        [pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

        # cfg.analysis['plotTraces']['include'].append((pop,0))  # record that pop

        # add stim source
        # netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
        netParams.stimSourceParams[key] = { 'type': 'IClamp', 
                                            'delay': start, 
                                            'dur': cfg.stimDur if cfg.stimDur is not None else dur, 
                                            'amp': cfg.clampAmplitude if cfg.clampAmplitude is not None else amp}
        
        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': sec, 
            'loc': loc}

if cfg.addPreIClamp:
    for key in [k for k in dir(cfg) if k.startswith('PreIClamp')]:
        params = getattr(cfg, key, None)
        [pop,sec,loc,start,dur,amp] = [params[s] for s in ['pop','sec','loc','start','dur','amp']]

        # cfg.analysis['plotTraces']['include'].append((pop,0))  # record that pop

        # add stim source
        # netParams.stimSourceParams[key] = {'type': 'IClamp', 'delay': start, 'dur': dur, 'amp': amp}
        netParams.stimSourceParams[key] = { 'type': 'IClamp', 
                                            'delay': start, 
                                            'dur': cfg.stimDur_pre if cfg.stimDur_pre is not None else dur, 
                                            'amp': cfg.clampAmplitude_pre if cfg.clampAmplitude_pre is not None else amp}
        
        # connect stim source to target
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': pop},
            'sec': sec, 
            'loc': loc}

#------------------------------------------------------------------------------
# Targeted NetStim inputs - FROM CFG.PY
#------------------------------------------------------------------------------
# The difference of this one to the "NetStim" is that this one allows you to target specific cells within a pop

if cfg.addTargetedNetStim:
    for key in [k for k in dir(cfg) if k.startswith('TargetedNetStim')]:
        params = getattr(cfg, key, None)
        [pop, sec, loc, synMech, synMechWeightFactor, start, interval, noise, number, weight, delay, targetCells] = \
        [params[s] for s in ['pop', 'sec', 'loc', 'synMech', 'synMechWeightFactor', 'start', 'interval', 'noise', 'number', 'weight', 'delay', 'targetCells']] 

        #cfg.analysis['plotTraces']['include'] = [(pop,0)]

        if synMech == ESynMech:
            wfrac = cfg.synWeightFractionEE
        elif synMech == SOMESynMech:
            wfrac = cfg.synWeightFractionSOME
        else:
            wfrac = [1.0]

        # add stim source
        netParams.stimSourceParams[key] = { 'type':     'NetStim', 
                                            'start':    cfg.startStimTime       if cfg.startStimTime is not None        else start, 
                                            'interval': cfg.interStimInterval   if cfg.interStimInterval is not None    else interval, 
                                            'noise':    noise, 
                                            'number':   cfg.numStims            if cfg.numStims is not None             else number}

        # netParams.stimSourceParams[key] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

        # connect stim source to target
        # for i, syn in enumerate(synMech):
        netParams.stimTargetParams[key+'_'+pop] =  {
            'source': key, 
            'conds': {'pop': cfg.stimPop if cfg.stimPop is not None else pop, 'cellList': targetCells},
            'sec': sec, 
            'loc': loc,
            'synMech': cfg.synMech if cfg.synMech is not None else synMech,
            # 'weight': weight,
            'weight': cfg.netWeight if cfg.netWeight is not None else weight,
            'synMechWeightFactor': synMechWeightFactor,
            'delay': delay}

#------------------------------------------------------------------------------
# GroupNetStim inputs - FROM CFG_CELL.PY
#------------------------------------------------------------------------------
if cfg.addGroupNetStim:
    # Group of NetStims
    for key in [k for k in dir(cfg) if k.startswith('GroupNetStim')]:
        params = getattr(cfg, key, None)
        nstype, numStims, pop, ynorm, cellRule, secList, allSegs, synMech, start, interval, noise, number, weight, delay = [params[s] for s in ['nstype', 'numStims', 'pop', 'ynorm', 'cellRule', 'secList', 'allSegs', 'synMech', 'start', 'interval', 'noise', 'number', 'weight', 'delay']]

        # cfg.analysis['plotTraces']['include'].append((pop,0))

        # print(str(netParams.cellParams[cellRule]))
        if not isinstance(secList, list):
            secList = list(netParams.cellParams[cellRule]['secLists'][secList])

        istim = 0
        segs = []

        if synMech == ESynMech:
            wfrac = cfg.synWeightFractionEE
        elif synMech == SOMESynMech:
            wfrac = cfg.synWeightFractionSOME
        else:
            wfrac = [1.0]

        if nstype == 'stim':  # implement as a stim - [jv] not being used
            while istim < numStims:
                for secName,sec in netParams.cellParams[cellRule]['secs'].items():
                    if secName in secList:
                        if allSegs:
                            nseg = sec['geom']['nseg']
                            for iseg in range(nseg):
                                segs.append([secName, (iseg+1)*(1.0/(nseg+1))])
                                istim += 1
                                if istim >= numStims: break
                        else:
                            segs.append([secName, 0.5])
                            istim += 1
                        
                        if istim >= numStims: break

            for istim, seg in enumerate(segs):

                # add stim source
                netParams.stimSourceParams[key+'_'+str(istim)] = {'type': 'NetStim', 'start': start, 'interval': interval, 'noise': noise, 'number': number}

                # connect stim source to target
                for i, syn in enumerate(synMech):
                    netParams.stimTargetParams[key+'_'+pop+'_'+syn+'_'+str(istim)] =  {
                        'source': key+'_'+str(istim), 
                        'conds': {'pop': pop, 'ynorm': ynorm},
                        'sec': seg[0], 
                        'loc': seg[1],
                        'synMech': syn,
                        'weight': weight*wfrac[i],
                        'delay': delay}

        elif nstype == 'pop':  # implement as a pop
            netParams.popParams[key] = {	'cellModel':'NetStim', 
                                            'numCells': numStims, 
                                            'rate': 	cfg.groupRate       if cfg.groupRate is not None        else 1000/interval,
                                            'noise': 	noise, 
                                            'start': 	start, 
                                            # 'start': 	cfg.startStimTime   if cfg.startStimTime is not None    else start, 
                                            'number':   number}
                                            # 'number': 	cfg.numGroupStims  if cfg.numGroupStims is not None  else number}
            
            netParams.connParams[key] = { 
                        'preConds': 	{'pop': key}, 
                        'postConds': 	{'pop': pop, 'ynorm': ynorm},
                        'synMech': 		synMech,
                        'weight': 		cfg.groupWeight if cfg.groupWeight is not None else weight, 
                        'synMechWeightFactor': wfrac,
                        'delay': 		delay,
                        'synsPerConn': 	1,
                        'sec': 			secList}
            
            netParams.subConnParams[key] = {
                        'preConds': 	{'pop': key}, 
                        'postConds': 	{'pop': pop, 'ynorm': ynorm},  
                        'sec': 			secList, 
                        'groupSynMechs': ESynMech, # removed to use only AMPA and see if it affects spatial summation, and not a combination of [AMPA, NMDA] 2020_05_28
                        'density': 		'uniform'} 

'''

'''
version control:

'''
