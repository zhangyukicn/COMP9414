# stripsProblem.py - STRIPS Representations of Actions
# AIFCA Python3 code Version 0.8.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Strips(object):
    def __init__(self, preconditions, effects, cost=1):
        """
        defines the STRIPS representation for an action:
        * preconditions is feature:value dictionary that must hold
        for the action to be carried out
        * effects is a feature:value map that this action makes
        true. The action changes the value of any feature specified
        here, and leaves other properties unchanged.
        * cost is the cost of the action
        """
        self.preconditions = preconditions
        self.effects = effects
        self.cost = cost

class STRIPS_domain(object):
    def __init__(self, feats_vals, strips_map):
        """Problem domain
        feats_vals is a feature:domain dictionary, 
                mapping each feature to its domain
        strips_map is an action:strips dictionary, 
                mapping each action to its Strips representation
        """
        self.actions = set(strips_map)  # set of all actions
        self.feats_vals = feats_vals
        self.strips_map = strips_map

class Planning_problem(object):
    def __init__(self, prob_domain, initial_state, goal):
        """
        a planning problem consists of
        * a planning domain
        * the initial state
        * a goal 
        """
        self.prob_domain = prob_domain
        self.initial_state = initial_state
        self.goal = goal

boolean = {True, False}
delivery_domain = STRIPS_domain(
    {'RLoc':{'cs', 'off', 'lab', 'mr'}, 'RHC':boolean, 'SWC':boolean,
     'MW':boolean, 'RHM':boolean},           #feaures:values dictionary
    {'mc_cs': Strips({'RLoc':'cs'}, {'RLoc':'off'}),   
     'mc_off': Strips({'RLoc':'off'}, {'RLoc':'lab'}),
     'mc_lab': Strips({'RLoc':'lab'}, {'RLoc':'mr'}),
     'mc_mr': Strips({'RLoc':'mr'}, {'RLoc':'cs'}),
     'mcc_cs': Strips({'RLoc':'cs'}, {'RLoc':'mr'}),   
     'mcc_off': Strips({'RLoc':'off'}, {'RLoc':'cs'}),
     'mcc_lab': Strips({'RLoc':'lab'}, {'RLoc':'off'}),
     'mcc_mr': Strips({'RLoc':'mr'}, {'RLoc':'lab'}),
     'puc': Strips({'RLoc':'cs', 'RHC':False}, {'RHC':True}),  
     'dc': Strips({'RLoc':'off', 'RHC':True}, {'RHC':False, 'SWC':False}),
     'pum': Strips({'RLoc':'mr','MW':True}, {'RHM':True,'MW':False}),
     'dm': Strips({'RLoc':'off', 'RHM':True}, {'RHM':False})
    } )

problem0 = Planning_problem(delivery_domain,
                            {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False, 
                             'RHM':False}, 
                            {'RLoc':'off'})
problem1 = Planning_problem(delivery_domain,
                            {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False, 
                             'RHM':False}, 
                            {'SWC':False})
problem2 = Planning_problem(delivery_domain,
                            {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False, 
                             'RHM':False}, 
                            {'SWC':False, 'MW':False, 'RHM':False})

### blocks world
def move(x,y,z):
    """string for the 'move' action"""
    return 'move_'+x+'_from_'+y+'_to_'+z
def on(x):
    """string for the 'on' feature"""
    return x+'_is_on'
def clear(x):
    """string for the 'clear' feature"""
    return 'clear_'+x
def create_blocks_world(blocks = {'a','b','c','d'}):
    blocks_and_table = blocks | {'table'}
    stmap =  {move(x,y,z):Strips({on(x):y, clear(x):True, clear(z):True}, 
                                 {on(x):z, clear(y):True, clear(z):False})
                    for x in blocks
                    for y in blocks_and_table
                    for z in blocks
                    if x!=y and y!=z and z!=x}
    stmap.update({move(x,y,'table'):Strips({on(x):y, clear(x):True}, 
                                 {on(x):'table', clear(y):True})
                    for x in blocks
                    for y in blocks
                    if x!=y})
    feats_vals = {on(x):blocks_and_table-{x} for x in blocks}
    feats_vals.update({clear(x):boolean for x in blocks_and_table})
    return STRIPS_domain(feats_vals, stmap)

blocks1dom = create_blocks_world({'a','b','c'})
blocks1 = Planning_problem(blocks1dom,
     {on('a'):'table', clear('a'):True,
      on('b'):'c',  clear('b'):True,
      on('c'):'table', clear('c'):False}, # initial state
     {on('a'):'b', on('c'):'a'})  #goal

blocks2dom = create_blocks_world({'a','b','c','d'})
tower4 = {clear('a'):True, on('a'):'b',
          clear('b'):False, on('b'):'c',
          clear('c'):False, on('c'):'d',
          clear('d'):False, on('d'):'table'}
blocks2 = Planning_problem(blocks2dom,
     tower4, # initial state
     {on('d'):'c',on('c'):'b',on('b'):'a'})  #goal

blocks3 = Planning_problem(blocks2dom,
     tower4, # initial state
     {on('d'):'a', on('a'):'b', on('b'):'c'})  #goal

