# WAVE_for_Jupiter

WAVE is a distributed scheduler for DAG type
task graph that outputs a mapping of tasks to real compute nodes.
It is a module used in [Jupiter](https://github.com/ANRGUSC/Jupiter).
We have two versions of WAVE: `random_WAVE` and `greedy_WAVE`

Note: We can not use WAVE as an independent tool

## Random WAVE
When assigning tasks to nodes, this version of WAVE does random assignment.
The algorithm will random choose a node in the set of all validate nodes.

## Greedy WAVE
When assigning tasks to nodes, this version of WAVE will first get network 
parameters from [profilers](https://github.com/ANRGUSC/DRUPE) as a delay factor.
The delay factor contains network delay, target node's CPU usage and memory usage.
The WAVE running in each of the node will maintain a sorted list of all its neighbor's delay 
information. Then it will pick up the node who has the lowest delay and assign tasks 
to it.

