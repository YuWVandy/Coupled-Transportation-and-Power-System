# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:52:10 2020

@author: wany105
""" 
from graph import Graph
from PowerNetwork import Power
from TransportationNetwork import Transportation
from Powerflowmodel import PowerFlowModel
from Trafficflowmodel import TrafficFlowModel
import Interdependency as interlink
import Tdata as td
import Pdata as pd
from System import system
from Hurricane import Hurricane
import Hdata as Hcd
import numpy as np
from matplotlib import pyplot as plt

def H_perform_plot(performance, hurricane):
    """Plot the performance curve for the power network under different sceneria
    performance: a list of performance under each hurricane sceneria
    hurricane: a list of hurricane
    """
    fig = plt.figure(figsize = (15, 10))
    for i in range(len(performance)):
        temp1 = performance[i]
        temp2 = hurricane[i]
        plt.plot(np.arange(0, len(temp1), 1), temp1, color = temp2.c, label = temp2.name)
        plt.xlabel('Time Step')
        plt.xticks(np.arange(0, len(temp1), 30))
        plt.ylabel('Performance')
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1, frameon = 0)
        plt.grid(True)
        
def Failure_Simulation(Num):
    """Perform Hurricane simulation on the whole system
    """
    #Define selected hurricanes
    Hurricanes = list()
    #Hcd.Hnum = 1
    TXpower.single_perform = np.empty([Hcd.Hnum, Num], dtype = object)
    length = np.zeros([Hcd.Hnum, Num]) #adjust the length of different performance list
    TX_TP.fail_history = np.empty(Hcd.Hnum, dtype = object)
    for i in range(Hcd.Hnum):
        TX_TP.fail_history[i] = []
        
    #Monte Carlo Simulation to calculate the performance
    for i in range(Hcd.Hnum):
        Hurricanes.append(Hurricane(Hcd.Hurricane_name[i], TXpower, Hcd.Latitude[i], Hcd.Longitude[i], Hcd.color[i]))
        Hurricanes[-1].verticexy(Hcd.Data[i], filelocation = Hcd.Data_Location, Type = 'local')
        Hurricanes[-1].trajectory_plot(townlat = 29.3013, townlon = -94.7977)
        Hurricanes[-1].Failprob(mu = 304, sigma = 45.6, a = 0.5, b = 1)
#        if(i == 0): #Since fail probability is nearly the same among all hurricane sceneria, we need to add some noise
        Hurricanes[-1].failprob -= 0.3
        
        for j in range(Num):
            TX_TP.fail_simu(Hurricanes[-1])
            TX_TP.Cascading_failure(pd.up_bound, pd.low_bound)
            TX_TP.fail_history[i].append(TX_TP.failsequence[-1]) ##Track down the final stable state for later use to calculate the conditional probability
            TXpower.single_perform[i, j] = TXpower.fperformance
            length[i, j] = len(TXpower.fperformance)
        
    return length
            
def Power_Performance(length, Num):
    """Quantify the performance of the power network
    """
    max_len = np.max(length)
    TXpower.performance = np.zeros([Hcd.Hnum, int(max_len)])
    for i in range(Hcd.Hnum):
        for j in range(Num):
            ##Unify the length of each array so that we can add them
            while(1):
                if(len(TXpower.single_perform[i, j]) == max_len):
                    break
                TXpower.single_perform[i, j].append(TXpower.single_perform[i, j][-1])
                
            TXpower.performance[i] = TXpower.performance[i] + np.array(TXpower.single_perform[i, j])
        
        TXpower.performance[i] = TXpower.performance[i]/Num
    
    

    

    
    

#Define the traffic network
TXtraffic = Transportation(graph_dict = td.Tadjl, color = td.color, name = td.name, lat = td.lat, lon = td.lon, nodenum = td.nodenum, edgenum = td.edgenum, \
                           O = td.O, D = td.D, nodefile = td.nodefile, edgefile = td.edgefile, Type = td.Type)
#Define the power network
TXpower = Power(graph_dict = pd.Padjl, color = pd.color, name = pd.name, lat = pd.lat, lon = pd.lon, nodenum = pd.nodenum, edgenum = pd.edgenum, \
                nodefile = pd.nodefile, edgefile = pd.edgefile, Type = pd.Type)


##Define the interdependency
TX_TPInter1 = interlink.PTinter1(TXpower, TXtraffic, name = 'TX_PowerSignal', color = 'orange')
TX_TPInter1.distadj()
DepenNum = [5]*TX_TPInter1.network2.Nnum
TX_TPInter1.dependadj(DepenNum)

##Define the power flow
TXPflow = PowerFlowModel(TXpower)
TXPflow.load([100]*TX_TPInter1.network2.Nnum, TX_TPInter1)
TXPflow.optimizationprob(cost = 1)
TXPflow.solve()


##Transportation flow
TXTflow = TrafficFlowModel(td.Tadjl, td.origins, td.destinations, td.demand, td.free_time, td.capacity, td.function, \
                       td.InterType, td.SigFun, td.Cycle, td.Green, td.t_service, td.hd, TXtraffic)

TXTflow.solve(td.accuracy, td.detail, td.precision)

TX_TP = system(name = 'TX_TP', networks = [TXpower, TXtraffic], inters = [TX_TPInter1])
TX_TP.Systemplot3d()
TX_TP.local_global_adj_flow()
TX_TPInter1.system = TX_TP

#Peform the hurricane simulation
Num = 1000
Length = Failure_Simulation(Num)
Power_Performance(Length, Num)

#Plot the power network performance under each hurricane sceneria
H_perform_plot(TXpower.performance, Hurricanes)

#Calculate the conditional failure probability
TX_TPInter1.Conditional_prob(0, Num)
TX_TPInter1.heatmap_conditional_prob()



    
    

