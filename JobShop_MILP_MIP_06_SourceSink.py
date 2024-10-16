# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:13:42 2024

@author: KARADGI
"""

from itertools import product
from mip import *
import matplotlib.pyplot as plt
import datetime as dt
import time

def GetUniqueFileName (prefix, m, n, a, ftype):
    timestamp = int (time.time())
    fileName = "{}_m{}_n{}_a{}_{}.{}".format (prefix, m, n, a, timestamp, ftype)
    return fileName

try:
    model = Model('Lineless', solver_name="CBC")
    # model = Model('Lineless') # Gurobi
    
    # # Processing time
    # P_j = [[0, 1, 3, 6, 7, 3, 6, 0],
    #         [0, 8, 5, 10, 10, 10, 4, 0],
    #         [0, 5, 4, 8, 9, 1, 7, 0],
    #         [0, 5, 5, 5, 3, 8, 9, 0],
    #         [0, 9, 3, 5, 4, 3, 1, 0],
    #         [0, 3, 3, 9, 10, 4, 1, 0]]
    
    P_j = [[0, 10, 8, 4, 0],
            [0, 8, 3, 5, 6, 0],
            [0, 4, 7, 3, 0]]
    
    nJobs = len(P_j)
    print ("Number of Job = {0}".format(nJobs))
    
    Jobs = range (0, nJobs+2, 1) #SuperJ
    Jobs_N = range (1, nJobs+1, 1) # N
    Jobs_K = range (0, nJobs+1, 1) # K
    Jobs_L = range (1, nJobs+2, 1) # L
    
    nMachines = 0
    for j in Jobs_N:
        tmpLen = len(P_j[j-1])-2
        if nMachines < tmpLen:
            nMachines = tmpLen
    print ("Number of Machines = {0}".format(nMachines))
    Machines = range(0, nMachines+2) #Considering SOURCE & SINK
    
    O_j = [ [0, 1, 2, 3, nMachines+1],
            [0, 2, 1, 4, 3, nMachines+1],
            [0, 1, 2, 4, nMachines+1]]
    
    # # Machine ID of above operations
    # O_j = [[0, 2, 0, 1, 3, 5, 4, nMachines+1],
    #         [0, 1, 2, 4, 5, 0, 3, nMachines+1],
    #         [0, 2, 3, 5, 0, 1, 4, nMachines+1],
    #         [0, 1, 0, 2, 3, 4, 5, nMachines+1],
    #         [0, 2, 1, 4, 5, 0, 3, nMachines+1],
    #         [0, 1, 3, 5, 0, 4, 2, nMachines+1]]
    
    nAMR = 2
    print ("Number of AMRs = {0}".format(nAMR))
    AMRs = range (0, nAMR)
    
    # AMR Velocity
    AMRVel = [3, 3]
    
    # Distance Loading Station, 1 ... m, Unloading Station
    MacDist = [[0, 6, 6, 11, 11, 10],
               [6, 0, 5, 10, 10, 9],
               [6, 5, 0, 10, 10, 9],
               [11, 10, 10, 0, 5, 6],
               [11, 10, 10, 5, 0, 6],
               [10, 9, 9, 6, 6, 0]]
    
    # Large Positive Number
    H = 1000000
    
    # »»»»»»»»»»»»»»»»»»»»»» set N «««««««««««««««««««««««
    #  AR: Consists of all possible combination if operation/machine and job
    # print ("set N")
    AR = {}
    tmpNCount = 0
    for j in Jobs_N:
        tmpCount = len(O_j[j-1])
        for i in range (1, tmpCount-1):
            # print ("({}, {})".format (O_j[j-1][i], j))
            
            tmpNValue = []
            tmpNValue.append(O_j[j-1][i])
            tmpNValue.append(j) #Considering SOURCE & SINK
            AR [tmpNCount] = tmpNValue
            tmpNCount += 1
    
    
    # »»»»»»»»»»»»»»»»»»»»»» set A «««««««««««««««««««««««
    # AJ: Consist of routing information of job j
    # Job perspective
    # print ("set A")
    AJ = {}
    tmpACount = 0
    for j in Jobs_N:
        tmpCount = len(O_j[j-1])
        for i in range (1, tmpCount-2):
            # print ("({}, {}) -> ({}, {})".format (O_j[j][i], j, O_j[j][i+1], j))
            
            tmpAValue = []
            tmpAValue.append(O_j[j-1][i])
            tmpAValue.append(j)
            tmpAValue.append(O_j[j-1][i+1])
            tmpAValue.append(j) #Considering SOURCE & SINK
            AJ [tmpACount] = tmpAValue
            tmpACount += 1
    
    
    # »»»»»»»»»»»»»»»»»»»»»» set B «««««««««««««««««««««««
    # AD: Consist of all possible Disjunctive Constraints
    # print ("set B")
    AD = {}
    tmpBCount = 0
    for i in range (1, nMachines+1):
        tmpB = {}
        tmpBCnt = 0
        for j in Jobs_N:
            tmpBList = []
            oo = O_j[j-1]
            # print ("({}, {}, {})".format (i, j, oo))
            if i in oo:
                # print ("({}, {})".format (i, j))
                tmpBList.append(i)
                tmpBList.append(j) #Considering SOURCE & SINK
                tmpB[tmpBCnt] = tmpBList
                tmpBCnt += 1
        
        tmpBItemCnt = len (tmpB)
        for ky1 in range (tmpBItemCnt-1):
            val1 = tmpB [ky1]
            # print ("{} -> {}".format (ky1, val1))
            for ky2 in range (ky1+1, tmpBItemCnt, 1):
                val2 = tmpB [ky2]
                # print ("{} -> {}".format (val1, val2))
                
                tmpBValue = []
                tmpBValue.append(val1[0])
                tmpBValue.append(val1[1])
                tmpBValue.append(val2[0])
                tmpBValue.append(val2[1])
                
                AD [tmpBCount] = tmpBValue
                tmpBCount += 1
    
    
    # »»»»»»»»»»»»»»»»»»»» PARAMETERS ««««««««««««««««««««
    # Makespan
    C_max = model.add_var(name="C_max")
    
    # Start time S_ij of job j on machine i
    C = [[model.add_var(name='C({},{})'.format(i, j)) 
          for j in Jobs] 
             for i in Machines]
    
    # »»»»»»»»»» DECISION VARIABLES - x_ijk ««««««««««
    # x_ijk = 1 if job j precedes job k on machine i; otherwise 0
    x = [[[model.add_var(var_type=BINARY, name='x({},{},{})'.format(i, j, k))
                   for k in Jobs] 
                      for j in Jobs] 
                         for i in Machines]
    
    # delta = 1 if AMR a is assigned to job j, otherwise 0
    delta = [[model.add_var(var_type=BINARY, name='delta({},{})'.format(a, j)) 
               for j in Jobs]
                 for a in AMRs]
    
    # gamma = 1 if directly or indirectly j precedes k, otherwise 0
    gamma = [[model.add_var(var_type=BINARY, name='gamma({},{})'.format(j, k)) 
               for k in Jobs]
                  for j in Jobs]
    
    
    # CONSTRAINT 02: Ensures no two operations start at the same time on a machine
    # print ("<<<< CONSTRAINT 02 >>>>")
    constraintCnt = 0
    for val in AD.values():
        i = val[0]      # I as per book
        l = val[1]      # L as per book
        j = val[3]      # K as per book
        iIndx1 = O_j[l-1].index (i)
        iIndx2 = O_j[j-1].index (i)
        # print ("{0} = ({1},{2}) [{3}] -> ({4},{5}) [{6}]".format(val, iIndx1, l-1, P_j[l-1][iIndx1], iIndx2, j-1, P_j[j-1][iIndx2]))
        # model += H * (1 - x[i][l][j]) + C[i][j] >= C[i][l] + P_j[j][iIndx]
        model += H * (1 - x[i][l][j]) + C[i][j] >= C[i][l] + P_j[j-1][iIndx2]
    
    
    # CONSTRAINT 03: Ensures no two operations start at the same time
    # print ("<<<< CONSTRAINT 03 >>>>")
    for val in AD.values():
        i = val[0]      # I as per book
        l = val[1]      # L as per book
        j = val[3]      # K as per book
        iIndx1 = O_j[l-1].index (i)
        iIndx2 = O_j[j-1].index (i)
        # print ("{0} = ({1},{2}) [{3}] -> ({4},{5}) [{6}]".format(val, iIndx1, l-1, P_j[l-1][iIndx1], iIndx2, j-1, P_j[j-1][iIndx2]))
        model += H * x[i][l][j] + C[i][l] >= C[i][j] + P_j[l-1][iIndx1]
	
	
	# CONSTRAINT 04: Ensure that processing is done as per the routing for each job
    # print ("<<<< CONSTRAINT 04 >>>>")
    for val in AJ.values():
        i1 = val[0]    # i as per book
        j = val[1]   # j as per book
        i1Indx = O_j[j-1].index (i1)
        i2 = val[2]    # k as per book
        i2Indx = O_j[j-1].index (i2)
        # print ("{3} = ({0},{1}) [{4}] -> ({2},{1}) [{5}]".format(i1, j, i2, val, P_j[j][i1Indx], P_j[j][i2Indx]))
        # model += C[i2][j] >= C[i1][j] + P_j[j-1][i2Indx] # Works fine without distance & velocity
        model += C[i2][j] >= C[i1][j] + P_j[j-1][i2Indx] + (xsum(delta[a][j]* int(MacDist[i1][i2]/AMRVel[a]) for a in AMRs))
    
    
    # CONTRAINTS 05, 06: Ensures that the last operation of job j and first operation 
    # of job k do not overlap in case if both jobs are assigned AMR a
    # print ("<<<< CONSTRAINT 05, 06 >>>>")
    for j in Jobs_N:
        for k in Jobs_N:
            if j != k:
                
                i_FrstJob = O_j[k-1][1]
                i_LastJob = O_j[j-1][-2]
                
                Pj_FrstJob = P_j[k-1][1]
                Pj_LastJob = P_j[j-1][-2]
                
                i_j = O_j[j-1].index (1)
                i_k = O_j[k-1].index (1)
                
                # print ("1st {}/{}/{}/{}, Lst {}/{}/{} ".format (j, i_FrstJob, Pj_FrstJob, k, i_LastJob, Pj_LastJob, MacDist[0][i]))
                
                for a in range (nAMR):
                    model += H * (1 - delta[a][j]) + H * (1 - delta[a][k]) + H * (1 - gamma [j][k]) + C[i_FrstJob][k] >= C[i_LastJob][j] + Pj_FrstJob + (xsum(delta[a][k]* int(MacDist[nMachines+1][0]/AMRVel[a]) for a in AMRs)) + (xsum(delta[a][i_k]* int(MacDist[0][i_k]/AMRVel[a]) for a in AMRs))
                    model += H * (1 - delta[a][j]) + H * (1 - delta[a][k]) + H * gamma [j][k] + C[i_LastJob][j] >= C[i_FrstJob][k] + Pj_LastJob + (xsum(delta[a][j]* int(MacDist[nMachines+1][0]/AMRVel[a]) for a in AMRs)) + (xsum(delta[a][i_j]* int(MacDist[0][i_j]/AMRVel[a]) for a in AMRs))
       
    
    # CONSTRAINT 07: Ensure AMR travel from source to 1st machine/operation
    # print ("<<<< CONSTRAINT 07 >>>>")
    for j in Jobs_N:        
        i = O_j[j-1].index (1)
        iIndx = O_j[j-1].index (i)
        # print ("{}: {} - {} / {} -> {}".format(j, 0, P_j[j-1][iIndx], MacDist[0][i], i))
        model += C[i][j] >= P_j[j-1][iIndx] + (xsum(delta[a][j]* int(MacDist[0][i]/AMRVel[a]) for a in AMRs))
     
    
    # CONSTRAINT 08: Ensure AMR travel from last machine/operation to sink
    # print ("<<<< CONSTRAINT 08 >>>>")
    for j in Jobs_N:        
        i = O_j[j-1][-2]
        # print ("{}: {} - {} -> {}".format(j, i, MacDist[i][nMachines+1], nMachines+1))
        model += C[nMachines+1][j] >= C[i][j] + (xsum(delta[a][j]* int(MacDist[i][nMachines+1]/AMRVel[a]) for a in AMRs))
    
    
    # CONSTRAINT 09: Ensures Precedence Constraints of jobs on same machine
    # print ("<<<< CONSTRAINT 09 >>>>")
    for val in AD.values():
        i = val[0]    # I as per book
        j = val[1]    # J as per book
        k = val[3]    # L as per book
        # print (val)
        model += x[i][j][k] + x[i][k][j] <= 1
    
    
    # CONSTRAINTS 10: Ensures that either job j precedes job k or job k precedes job j
    # print ("<<<< CONSTRAINT 10 >>>>")
    for j in Jobs_N:
        for k in Jobs_N:
            if j != k:
                model += gamma[j][k] + gamma[k][j] == 1
    
    
    # CONSTRAINT 11: Ensures starting time is greater than zero
    # print ("<<<< CONSTRAINT 11 >>>>")
    for val in AR.values():
        i = val[0]
        j = val[1]
        iIndx = O_j[j-1].index (i)
        # print (val)
        model += C[i][j] >= P_j[j-1][iIndx]
        
    
    # CONSTRAINT 12: Ensure the computation of Cmax, which will be the 
    # completion time of processing of last operation + travel time to
    # unloading station
    # print ("<<<< CONSTRAINT 12 >>>>")  
    for j in Jobs_N:        
        i = O_j[j-1][-2]
        model += C_max >= C[nMachines+1][j]
    
    
    # CONSTRAINT 13: Ensures that an AMR a is assigned to a job j 
    # print ("<<<< CONSTRAINT 13 >>>>")
    for j in Jobs_N:
        # print (j)
        model.add_constr (xsum(delta[a][j] for a in AMRs) == 1)
    
    
    # CONSTRAINT 14: Ensure that job 0 is assigned to a valid machine
    # print ("<<<< CONSTRAINT 14 >>>>")
    for i in Machines:
        model += (xsum(x[i][0][k] for k in Jobs_N) == 1)
        
    
    # CONSTRAINT 15: Ensure that there is no precedence between same job
    # print ("<<<< CONSTRAINT 15 >>>>")
    for j in Jobs_N:
        model += gamma[j][j] == 0
    
    
    # CONSTRAINT 16, 16: Ensure that no AMR is assigned to dummy jobs o and n+1
    # print ("<<<< CONSTRAINT 16, 17 >>>>")
    # for a in AMRs:
    #     model += delta[a][0] == 0
    #     model += delta[a][nJobs+1] == 0
    
    
    # CONSTRAINT 18, 19: Ensure that there is no precedence relationship between dummy jobs
    # print ("<<<< CONSTRAINT 18, 19 >>>>")
    # model += gamma [0][nJobs+1] == 0
    # model += gamma [nJobs+1][0] == 0
    
    
    # CONSTRAINT 20: Ensure that job 0 is assigned to a valid machine
    # print ("<<<< CONSTRAINT 20 >>>>")
    # for i in Machines:
    #     model += (xsum(x[i][j][nJobs+1] for j in Jobs_N) == 1)
    
    
    model.objective = C_max
    
    model.write ("model_MIP.lp")
    
    start_time = time.time()
    status = model.optimize(max_seconds=120)
    end_time = time.time()
    cpu_time = end_time - start_time
    
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    
        model.write ("model_MIP.sol")
        
        Cmax = C_max.x
        print("Makespan: ", Cmax)
        print ("++++++++++++++++++++++==========+++++++++++++++")
        
        # Figure and set of subplots
        fig, axs = plt.subplots(2, 1, figsize=(20, 15), gridspec_kw={'height_ratios': [6, 2]})
        # fig.set_figheight(12)
        # fig.set_figwidth(18)
        
        # Display scheduling of jobs
        ax = axs[0]
        ax.set_ylabel('Machine', fontweight ='bold', loc='top', color='magenta', fontsize=16)
        # ax.set_ylim(-0.5, nMachines-0.5)
        ax.set_ylim(0.5, nMachines+1-0.5)
        ax.set_yticks(Machines, minor=True)
        ax.tick_params(axis='y', labelcolor='magenta', labelsize=16)
        
        ax.set_xlabel('Time', fontweight ='bold', loc='right', color='red', fontsize=16)
        ax.set_xlim(0, Cmax+2)
        
        ax.tick_params(axis='x', labelcolor='red', labelsize=16)
        
        ax.grid(True)
        
        tmpTitle = 'Job Shop Scheduling (m={0}; n={1}; AMRs = {3}; Makespan={2})'.format(nMachines, nJobs, Cmax, nAMR)
        ax.set_title(tmpTitle, size=24, color='blue')
        
        colors = ['orange', 'deepskyblue', 'indianred', 'limegreen', 'slateblue', 'gold', 'violet', 'grey', 'red', 'magenta']
        
        # print ("-------------------------------------------------------------")
        # for val in AR.values():
        #     i = val[0]
        #     j = val[1]
        #     iIndx = O_j[j-1].index (i)
        #     a_j = 0
        #     for a in AMRs:
        #         if delta[a][j].x > 0:
        #             a_j = a
        #     print ("{}/{}/{}/{}/{}".format(i, j, a_j, P_j[j-1][iIndx], C[i][j].x))
        # print ("-------------------------------------------------------------")
        
        for val in AR.values():
            i = val[0]
            j = val[1]
            iIndx = O_j[j-1].index (i)
            # print ("{} - {} - {}".format(i, j, iIndx))
            
            Pj = P_j[j-1][iIndx]
            CT = C[i][j].x
            ST = CT - Pj
            
            a_j = 0
            for a in AMRs:
                if delta[a][j].x > 0:
                    a_j = a
            
            print ("Job{} on Machine {} and AMR {}: ST {} + Pj {} = CT {}".format(j, i, a_j, ST, Pj, CT))
                
            cIndx = 0
            cIndx = j % len(colors)
            ax.broken_barh([(ST, Pj)], (-0.3+i, 0.6), facecolor=colors[cIndx], linewidth=1, edgecolor='black')
            ax.text((ST + (Pj/2-0.3)), (i+0.03), '{}'.format(j), fontsize=18)
        
        # Display AMR assignment
        top_ax = axs[1]
        top_ax.set_ylabel('AMRs', fontweight='bold', loc='top', color='magenta', fontsize=16)
        top_ax.set_xlabel('Time', fontweight='bold', loc='right', color='red', fontsize=16)
        top_ax.set_ylim(0.5, nAMR + 0.5)
        top_ax.set_yticks(range(1, nAMR+1), minor=False)
        top_ax.tick_params(axis='y', labelcolor='magenta', labelsize=16)
        top_ax.set_xlim(0, Cmax + 2)
        top_ax.tick_params(axis='x', labelcolor='red', labelsize=16)
        top_ax.grid(True)
        
        # Example data for the top Gantt chart
        top_colors = ['orange', 'deepskyblue', 'indianred', 'limegreen', 'slateblue', 'gold', 'violet', 'grey', 'red', 'magenta', 'blue', 'green', 'silver']
        
        for a in AMRs:
            for j in Jobs_N:
                if delta[a][j].x > 0:
                    i_Frst = O_j[j-1][1]
                    i_Last = O_j[j-1][-2]
                    
                    Pj_1 = P_j[j-1][1]
                    ST_1 = C[i_Frst][j].x - Pj_1
                    CT = C[i_Last][j].x
                    duration = CT-ST_1
                    # print("Job {0} is assigned to AMR {1} with starting at {2} and completing at {3}!".format(j, a, ST_1, CT))
                    
                    top_ax.broken_barh([(ST_1, duration)], (-0.3 + a+1, 0.6), facecolor=top_colors[j], linewidth=1, edgecolor='black')
                    top_ax.text(ST_1 + (duration) / 2 , a+1 - 0.1, '{}'.format(j), fontsize=14, ha = 'center')
        
        plt.tight_layout()
        plt.show()
        
        chartName = GetUniqueFileName ("MILP", nMachines, nJobs, nAMR, "png")
        fig.savefig(chartName)
        
        
        
        # ---------------------------------------------------------------------
        fileName = GetUniqueFileName ("MILP", nMachines, nJobs, nAMR, "txt")
        f = open (fileName, "a")
        f.write (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        f.write ("\nWelcome to main function at {0}".format(dt.datetime.now().strftime('%d-%m %H:%M:%S.%f')))
        f.write ("\nNumber of Jobs: {0}".format(nJobs))
        f.write ("\nNumber of machines: {0}".format(nMachines))
        f.write ("\nNumber of AMRs: {0}".format(nAMR))
        f.write ("\nProduction Routing: {0}".format(O_j))
        f.write ("\nProcessing time: {0}".format(P_j))
        
        
        f.write ('\n\n\nNumber of Integer Variables is {0}'.format(model.num_cols - model.num_int))
        f.write ('\nNumber of Binary Decision Variables is {0}'.format(model.num_int))
        f.write ('\nNumber of Constraints is {0}'.format(model.num_rows))
        
        f.write ('\n\n\nObjective is {0} time units'.format(Cmax))
        f.write ("\nProblem solved in {0} seconds".format(cpu_time))
        # f.write ("\nProblem solved in {0} microseconds".format())
        # f.write ("\nProblem solved in {0} iterations".format())
        
        f.write ("\n\n-----------------------------------------------------------")
        f.write ("\nm \t n\t a\t Integer Variables \t Binary Variables \t Constraints \t Objective \t CPU Time (s)")
        f.write ("\n-----------------------------------------------------------")
        f.write ("\n\n{0} \t {1} \t {2} \t {3} \t {4} \t {5} \t {6} \t {7}".format(nMachines, nJobs, nAMR, model.num_cols - model.num_int, model.num_int, model.num_rows, Cmax, cpu_time))
        f.write ("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        # ---------------------------------------------------------------------
        
        f.close ()
        
    else:
        print("No OPTIMAL solution!!!")
        
except AttributeError:
    print('Encountered an attribute error') 
