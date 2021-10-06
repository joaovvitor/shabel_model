#! /usr/bin/python3
# Optional: change the Above line to your Python3 path 
# - type < which python3 > in the command line and replace the address < /usr/bin/python3 > by what your prompt returns

"""
init.py

Starting script to run NetPyNE-based model.

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: joao.moreira@downstate.edu, salvadordura@gmail.com
"""


# snippet of code to import matplotlib and dynamically switch backend to "MacOSX" for plotting
import sys
from    matplotlib  import  pyplot  as plt
# print("Matplotlib backend (default): %s" %plt.get_backend())
# modules = []
# for module in sys.modules:
#     if module.startswith('matplotlib'):
#         modules.append(module)
# for module in modules:
#     sys.modules.pop(module)
# import matplotlib
# matplotlib.use("MacOSX")
# from    matplotlib  import  pyplot  as plt
# print("Matplotlib backend (dynamic): %s" %plt.get_backend())

import matplotlib; matplotlib.use('agg')  # to avoid graphics error in servers
from netpyne import sim
import sys

cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg_file.py', netParamsDefault='netParams.py')
#sim.create(netParams, cfg)
#sim.gatherData()

sys.stderr.write('#------------------------------------------------# \n')
sys.stderr.write('#     Simulation Type:        %s \n' %cfg.simType)
sys.stderr.write('#------------------------------------------------# \n')

sim.create(netParams, cfg)
sim.net.defineCellShapes()
sim.simulate()
sim.analyze()

# sim.createSimulateAnalyze(netParams, cfg)

import matplotlib.pyplot as plt
plt.show()