# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:36:25 2020

@author: metalcorebear
"""

import random
import networkx as nx
import numpy as np


#Random output generator
def coin_flip(ptrue):
    test = random.uniform(0.0,1.0)
    if ptrue == 0:
        out = False
    elif test < ptrue:
        out = True
    else:
        out = False
    return out


#####################################################################
#                                                                   #
#               Initial Build                                       #
#                                                                   #
#####################################################################



#Instantiate social network
#Chaos parameter allows for variability in following social distancing recommendations.
def build_network(interactions, population, chaos = 0.001):
    G = nx.Graph()
    G.add_nodes_from(range(population))
    nodes_list = list(G.nodes())
    edge_set = set()
    top_row = 0
    for node_1 in nodes_list:
        top_row += 1
        for node_2 in range(top_row):
            if (G.degree(node_2) < interactions) and (G.degree(node_1) < interactions):
                edge = (node_1, node_2)
                if ((edge[0],edge[1])) and ((edge[1],edge[0])) not in edge_set:
                    if not coin_flip(chaos):
                        G.add_edge(*edge)
                        edge_set.add(edge)
            else:
                if coin_flip(chaos):
                    edge = (node_1, node_2)
                    if ((edge[0],edge[1])) and ((edge[1],edge[0])) not in edge_set:
                        G.add_edge(*edge)
                        edge_set.add(edge)
    return G


##########################################################################################
#                                                                                        #
#                    Infection                                                           #
#                                                                                        #
#                                                                                        #
#########################################################################################

class Infection:

    def __init__(self, model, ptrans = 0.25, reinfection_rate = 0.00, I0 =0.10, severe =0.18,
                 progression_period = 3, progression_sd = 2, death_rate = 0.0193, recovery_days = 21,
                 recovery_sd = 7):
        self.model = model
        self.ptrans = ptrans
        self.reinfection_rate = reinfection_rate
        self.I0 = I0
        self.severe = severe
        self.progression_period = progression_period
        self.progression_sd = progression_sd
        self.death_rate = death_rate
        self.recovery_days = recovery_days
        self.recovery_sd = recovery_sd
        self.dead_agents = []


    def initial_infection(self):
        infected = coin_flip(self.I0)
        if infected == False:
            susceptible = True
            severe = False
        else:
            susceptible = False
            severe = coin_flip(self.severe)

        return infected, susceptible, severe


    # Determine if infection is transmitted
    def infect(self, agent_1, agent_2):
        was_infected = agent_2.was_infected
        if (agent_2.infected == False) and (agent_2.susceptible == True):
            if agent_1.infected == True:
                if agent_2.was_infected == False:
                    agent_2.infected = coin_flip(self.ptrans)
                    if agent_2.infected == True:
                        infected_bool = True
                        agent_2.severe = coin_flip(self.severe)
                    else:
                        infected_bool = False
                        agent_2.severe = False
                else:
                    #agent_2.infected = coin_flip(reinfection_rate)
                    agent_2.infected = coin_flip(self.ptrans)
                    if agent_2.infected == True:
                        infected_bool = True
                        agent_2.severe = coin_flip(self.severe)
                    else:
                        infected_bool = False
                        agent_2.severe = False
            else:
                agent_2.infected = agent_2.infected
                infected_bool = False
        else:
            infected_bool = False
        return infected_bool, was_infected


    def interact(self, agent):

        neighbors = self.model.grid.get_neighbors(agent.pos)

        if len(neighbors)== 0:
            print (agent.unique_id + " is lonely")
        else:
            for neighbor in neighbors:
                if neighbor in self.dead_agents:
                    pass
                else:
                    neighbor_obj = self.model.schedule._agents[neighbor]
                    infected_bool, was_infected = self.infect(agent, neighbor_obj)
                    if infected_bool == True:
                        neighbor_obj.susceptible = False
                        neighbor_obj.day = 0
                        agent.induced_infections += 1
                        agent.infected_others = True
                        if was_infected == True:
                            agent.recovered = False


            if agent.infected == True:
                agent.susceptible = False
                progression_threshold = int(np.random.normal(self.progression_period, self.progression_sd))
                if agent.day >= progression_threshold:
                    if agent.severe == True:
                        agent.alive = coin_flip((1 - self.death_rate))
                        #Agent Dies sequence
                        if agent.alive == False:
                            agent.susceptible = False
                            agent.severe = False
                            agent.was_infected = True
                            self.dead_agents.append(agent.unique_id)
                            self.model.schedule.remove(agent)

                if agent.alive == True:
                    recovery_threshold = int(np.random.normal(self.recovery_days, self.recovery_sd))
                    if agent.day >= recovery_threshold:
                        agent.infected = False
                        agent.severe = False
                        if coin_flip(self.reinfection_rate):
                            agent.susceptible = True
                        else:
                            agent.susceptible = False
                        agent.was_infected = True
                        agent.recovered = True
                        agent.day = 0


