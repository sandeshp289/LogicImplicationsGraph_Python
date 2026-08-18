#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#// File       : implications.py
#// Language   : Python
#// Description: Graph-based Computation of Static Logic Implications (direct, indirect, extended backward, contrapositive)
#//              Option to either compute for a specific gate OR all gates
#// Author     : Sandesh Prabhakar
#// Created    : April 4, 2026
#// Modified   : August 17, 2026
#// Version    : 1.0
#//
#// Copyright (c) 2026 Sandesh Prabhakar
#// All rights reserved
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# %%
import sys
import numpy as np
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt
import math

# %%
class Gate(Enum):
	G_JUNK   =  0
	G_INPUT  =  1
	G_OUTPUT =  2
	G_XOR    =  3
	G_XNOR   =  4
	G_DFF    =  5
	G_AND    =  6
	G_NAND   =  7
	G_OR	 =  8
	G_NOR    =  9
	G_NOT    =  10
	G_BUF    =  11
	G_TIE1   =  12
	G_TIE0   =  13
	G_PSI    =  14
	G_PSO    =  15

# %%
def evaluate (j, gtype, value, fanin, faninlist ):
	match gtype[j]:
		#PSEUDO OUTPUT PSO
		case 15:
			value[j]=value[int(faninlist[j][0])]

		#NAND gate
		case 7:
			out='0'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '0':
					value[j]='1'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out 

		#AND gate
		case 6:
			out='1'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '0':
					value[j]='0'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out

		#OR gate
		case 8:
			out='0'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '1':
					value[j]='1'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out

		#NOR gate
		case 9:
			out='1'
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == '1':
					value[j]='0'
					return
				elif value[int(faninlist[j][nn])] == 'X':
					out='X'
				value[j]=out

		#XOR gate
		case 3:
			out_int=0;
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == 'X':
					value[j]='X'
					return
				elif value[int(faninlist[j][nn])] == '1':
					out_int=not out_int

				match out_int:
					case 0:
						out = '0'
					case 1:
						out = '1'
				value[j]=out

		#XNOR gate
		case 4:
			out_int=0;
			for nn in range(0,int(fanin[j])):
				if value[int(faninlist[j][nn])] == 'X':
					value[j]='X'
					return
				elif value[int(faninlist[j][nn])] == '1':
					out_int=not out_int

				match out_int:
					case 0:
						out = '1'
					case 1: 
							out = '0'
				value[j]=out 

		#NOT gate
		case 10:
			if value[int(faninlist[j][0])] == '0':
				value[j]='1'
			elif value[int(faninlist[j][0])] == '1':
				value[j]='0'
			elif value[int(faninlist[j][0])] == 'X':
				value[j]='X'

		#BUF gate
		case 11:
			value[j]=value[int(faninlist[j][0])]

		#TIE_1
		case 12:
			value[j]='1'

		#TIE_0
		case 13:
			value[j] = '0'

		#OUTPUT
		case 2:
			value[j]=value[int(faninlist[j][0])]

		#D_FF
		case 5:
			value[j]=value[int(faninlist[j][0])]

# %%
def direct_implications(tcount,gtype,fanout,fanoutlist,fanin,faninlist,psi,pso,DGI,Gate):

	for i in range(1,tcount+1):
		DGI.add_node(i)
		DGI.add_node(int(i+tcount))
		match gtype[i]:
			#INPUT
			case 1:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					
			#PSEUDO INPUT PSI
			case 14:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
				DGI.add_edge(i,int(faninlist[int(pso[i])][0]),weight=-1)
				DGI.add_edge(int(i+tcount),int(faninlist[int(pso[i])][0]+tcount),weight=-1)
				#print("PSI edge: ",i,int(faninlist[int(pso[i])][0]),"weight=-1")
				#print("PSI edge: ",int(i+tcount),int(faninlist[int(pso[i])][0]+tcount),"weight=-1")

			#PSEUDO OUTPUT PSO
			case 15:
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					#DGI.add_edge(i,k,weight=0)
					#DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					DGI.add_edge(k,int(psi[i]),weight=1)
					DGI.add_edge(int(k+tcount),int(psi[i]+tcount),weight=1)
					#print("PSO edge: ",k,int(psi[i]),"weight=1")
					#print("PSO edge: ",int(k+tcount),int(psi[i]+tcount),"weight=1")

			#NAND gate
			case 7:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					DGI.add_edge(i,int(k+tcount),weight=0)
			#AND gate
			case 6:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)

			#OR gate
			case 8:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					DGI.add_edge(i,k,weight=0)

			#NOR gate
			case 9:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					DGI.add_edge(int(i+tcount),k,weight=0)

			#XOR gate
			case 3:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)


			#XNOR gate
			case 4:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)

			#NOT gate
			case 10:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					DGI.add_edge(i,int(k+tcount),weight=0)
					DGI.add_edge(int(i+tcount),k,weight=0)

			#BUF gate
			case 11:
				for nn in range(0,int(fanout[i])):
					k=int(fanoutlist[i][nn])
					if gtype[k]==Gate.G_AND.value:
						DGI.add_edge(i,k,weight=0)
					elif gtype[k]==Gate.G_NAND.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_OR.value:
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOR.value:
						DGI.add_edge(int(i+tcount),k,weight=0)
					elif gtype[k]==Gate.G_BUF.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_NOT.value:
						DGI.add_edge(i,int(k+tcount),weight=0)
						DGI.add_edge(int(i+tcount),k,weight=0)					
					elif gtype[k]==Gate.G_OUTPUT.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
					elif gtype[k]==Gate.G_PSO.value:
						DGI.add_edge(i,k,weight=0)
						DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					DGI.add_edge(i,k,weight=0)
					DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)

			#OUTPUT
			case 2:
				for nn in range(0,int(fanin[i])):
					k=int(faninlist[i][nn])
					DGI.add_edge(i,k,weight=0)
					DGI.add_edge(int(i+tcount),int(k+tcount),weight=0)


# %%
def display_graph(DGI):
    rad=0.0
    pos=nx.spring_layout(DGI)
    for u, v, k, data in DGI.edges(keys=True, data=True):
            # Adjust 'rad' for different curves if desired for each parallel edge
            rad = rad+0.1
            print(u,v,k,data)
            nx.draw_networkx(DGI, pos, edgelist=[(u, v, k)],
                                connectionstyle=f'arc3,rad={rad}',
                                width=1.5, alpha=0.7,arrows=True)
            # Optionally add edge labels
            #edge_labels = nx.get_edge_attributes(DG, 'weight','key')
            #edge_labels = {(u, v): data['weight'] for u, v, data in DG.edges(data=True)}
            edge_labels = {(u, v): data['weight']}
            nx.draw_networkx_edge_labels(DGI, pos, connectionstyle=f'arc3,rad={rad}',edge_labels=edge_labels, font_color='red')        


# %%
def transitive_closure(snode,tcount,EventList,value,levelNum,DGI):
    temp_impl=[]
    #print("Repeating")
    #print("Inside TC:",type(DGI))
    #print("Inside TC:",type(snode))
    #print("Inside TC:",type(nx))
    list_nodes=nx.dfs_postorder_nodes(DGI,source=snode)
    for x in list_nodes:
        #print("x=",x)
        all_paths=list(nx.all_simple_edge_paths(DGI,source=snode,target=x))
        z=len(all_paths)
        #print(all_paths)
        for zz in range(0,z):
            temp=all_paths[zz]
            #print(temp)
            yy=len(all_paths[zz])
            temp_weight=0
            key_t=0
            for yk in range(0,yy):
                key_t=all_paths[zz][yk][2]
                temp_src=all_paths[zz][yk][0]
                temp_target=all_paths[zz][yk][1]
                temp_weight=DGI[int(temp_src)][int(temp_target)][int(key_t)]['weight'] + temp_weight
                #print("temp_src=",temp_src,";temp_target=",temp_target,";DGI[temp_src][temp_target][key_t]['weight']=",DGI[int(temp_src)][int(temp_target)][int(key_t)]['weight'])
            if x > tcount:
                #print(x-tcount,", 1, ",temp_weight)
                temp_impl.append((x-tcount,1,temp_weight))
                if temp_weight == 0:
                    EventList[int(levelNum[int(int(x)-tcount)])][int(x-tcount)]=0
                    value[int(x-tcount)]='1'
            else:
                #print(x,", 0, ",temp_weight)
                temp_impl.append((x,0,temp_weight))
                if temp_weight == 0:
                    EventList[int(levelNum[x])][x]=0
                    value[x]='0'
            #print("weight=",temp_weight)
    #print(temp_impl)
    #print(type(temp_impl))
    return temp_impl
    #unique_temp_impl=set(temp_impl)
    #print(unique_temp_impl)
    #len(unique_temp_impl)

def transitive_closure_with_revisits(start_node,tcount,EventList,value,levelNum,graph, max_depth=None):
	stack = [(start_node, [start_node], 0, 0)]  # (current_node, current_path, current_depth)
	all_paths = []
	temp_impl = []

	while stack:
		current_node, current_path, current_depth, current_weight = stack.pop()
		all_paths.append((current_path, current_weight))
		xt=len(current_path)
		dest=int(current_path[xt-1])
		if dest > tcount:
			temp_impl.append((dest-tcount,1,current_weight))
			if current_weight == 0:
				EventList[int(levelNum[int(int(dest)-tcount)])][int(dest-tcount)]=0
				value[int(dest-tcount)]='1'
		else:
			temp_impl.append((dest,0,current_weight))
			if current_weight == 0:
				EventList[int(levelNum[dest])][dest]=0
				value[dest]='0'

		if max_depth is not None and current_depth >= max_depth:
			continue

		for neighbor, edge_data in graph[current_node].items():
			# Iterate through all parallel edges between current_node and neighbor
			for key, attributes in edge_data.items():
				new_path = current_path + [neighbor]
				stack.append((neighbor, new_path, current_depth + 1,current_weight+int(attributes['weight'])))
	#return all_paths, temp_impl
	return temp_impl

# %%
def indirect_and_contrapositive_implications(snode, tcount, maxlevels,num_gate_per_level,gate_at_level,EventList,gtype, value, fanin, faninlist, fanout, fanoutlist, levelNum, DGI, Gate, o_file):
	num_i=0
	num_c=0
	if snode > tcount:
		#print("Indirect Implications of (",snode-tcount,",1",",0",")")
		o_file.write("Indirect and Contrapositive Implications:\n")
	else:
		#print("Indirect Implications of (",snode,",0",",0",")")
		o_file.write("Indirect and Contrapositive Implications:\n")
			
	for i in range(0,maxlevels,5):
					for js in range(1,num_gate_per_level[i]+1):
						j=int(gate_at_level[i][js])
						if EventList[i][j]==1:
							temp=value[j]
							evaluate(j, gtype, value, fanin, faninlist )

							if temp==value[j]:
								for kk in range(0,int(fanout[j])):
									h=int(fanoutlist[j][kk])
									r=int(levelNum[h])
									if EventList[r][h]==1:
										break
									else:
										EventList[r][h]=0
							else:
								#print("HERE")
								if gtype[j]!=Gate.G_PSO.value:
									#print("HERE2",j, value[j])
									if value[j]=='0':
										DGI.add_edge(snode,j,weight=0)
										#print(j,"0","0")
										o_file.write("--Indirect: (" + str(j) + ",0,0)\n")
										num_i += 1
										#Contrapositive Implication
										if snode > tcount:
											DGI.add_edge(int(j+tcount),int(snode-tcount),weight=0)
											#print("Contrapositive Implication: (",j,", 1, 0) -> (",int(snode-tcount),", 0, 0)")
											o_file.write("--Contrapositive: (" + str(j) + ",1,0) -> (" + str(int(snode-tcount)) + ",0,0)\n")
											num_c += 1
										else:
											DGI.add_edge(int(j+tcount),int(snode+tcount),weight=0)
											#print("Contrapositive Implication: (",j,", 1, 0) -> (",snode,", 1, 0)")
											o_file.write("--Contrapositive: (" + str(j) + ",1,0) -> (" + str(snode) + ",1,0)\n")
											num_c += 1
									if value[j]=='1':
										DGI.add_edge(snode,int(j+tcount),weight=0)
										#print(j,"1","0")
										o_file.write("--Indirect: (" + str(j) + ",1,0)\n")
										num_i += 1
										#Contrapositive Implication
										if snode > tcount:
											DGI.add_edge(j,int(snode-tcount),weight=0)
											#print("Contrapositive Implication: (",j,", 0, 0) -> (",int(snode-tcount),", 0, 0)")
											o_file.write("--Contrapositive: (" + str(j) + ",0,0) -> (" + str(int(snode-tcount)) + ",0,0)\n")
											num_c += 1
										else:
											DGI.add_edge(j,int(snode+tcount),weight=0)
											#print("Contrapositive Implication: (",j,", 0, 0) -> (",snode,", 1, 0)")
											o_file.write("--Contrapositive: (" + str(j) + ",0,0) -> (" + str(snode) + ",1,0)\n")
											num_c += 1
								for kk in range(0,int(fanout[j])):
									h=int(fanoutlist[j][kk])
									r=int(levelNum[h])
									EventList[r][h]=1
						else:
							if value[j] != 'X':
								for kk in range(0,int(fanout[j])):
									h=int(fanoutlist[j][kk])
									r=int(levelNum[h])
									if value[h]=='X':
										EventList[r][h]=1
	print(str(num_i) + "  Indirect Implications" )
	print(str(num_c) + "  Indirect Contrapositive Implications" )
	o_file.write(str(num_i) + "  Indirect Implications\n" )
	o_file.write(str(num_c) + "  Indirect Contrapositive Implications\n" )


# %%
def eb_logic_simulation(maxlevels,tcount, num_gate_per_level,gate_at_level,EventList,value,gtype,fanin,faninlist,fanout,fanoutlist,levelNum,Gate):
    tmp_impl_list=[]  
    for i in range(0,maxlevels,5):
                        for js in range(1,num_gate_per_level[i]+1):
                            j=int(gate_at_level[i][js])
                            if EventList[i][j]==1:
                                temp=value[j]
                                evaluate(j, gtype, value, fanin, faninlist )

                                if temp==value[j]:
                                    for kk in range(0,int(fanout[j])):
                                        h=int(fanoutlist[j][kk])
                                        r=int(levelNum[h])
                                        if EventList[r][h]==1:
                                            break
                                        else:
                                            EventList[r][h]=0
                                else:
                                    #print("HERE")
                                    if gtype[j]!=Gate.G_PSO.value:
                                        #print("HERE2",j, value[j])
                                        if value[j]=='0':
                                            tmp_impl_list.append((j,0,0))
                                            #DGI.add_edge(snode,j,weight=0)
                                            #print(j,"0","0")
                                        if value[j]=='1':
                                            tmp_impl_list.append((int(j+tcount),1,0))
                                            #DGI.add_edge(snode,int(j+tcount),weight=0)
                                            #print(j,"1","0")
                                    for kk in range(0,int(fanout[j])):
                                        h=int(fanoutlist[j][kk])
                                        r=int(levelNum[h])
                                        EventList[r][h]=1
                            else:
                                if value[j] != 'X':
                                    for kk in range(0,int(fanout[j])):
                                        h=int(fanoutlist[j][kk])
                                        r=int(levelNum[h])
                                        if value[h]=='X':
                                            EventList[r][h]=1
    return tmp_impl_list


# %%
def impl_unjustified_nodes_and_simulate(gx,imp_val,fanin,value,EventList,faninlist,tcount,levelNum,DGI,maxlevels,num_gate_per_level,gate_at_level,gtype,fanout,fanoutlist,Gate,max_depth):
	tmp_set=[]
	for k in range(0,int(fanin[gx])):
		tmp_value=value.copy()
		tmp_EventList=EventList.copy()
		fn=int(faninlist[gx][k])
		if imp_val==0:
			tmp_snode=fn
		if imp_val==1:
			tmp_snode=int(fn+tcount)
		#print(imp_val)
		#print(tmp_snode)
		#print(type(tmp_snode))
		#print(type(DGI))
		if value[fn]=='X':
			#tmp_impl=list(set(transitive_closure(tmp_snode,tcount,tmp_EventList,tmp_value,levelNum,DGI)))
			tmp_impl=list(set(transitive_closure_with_revisits(tmp_snode,tcount,tmp_EventList,tmp_value,levelNum,DGI,max_depth)))
			tmp_set.append(eb_logic_simulation(maxlevels,tcount, num_gate_per_level,gate_at_level,tmp_EventList,tmp_value,gtype,fanin,faninlist,fanout,fanoutlist,levelNum,Gate))
	return tmp_set

# %%
def common_implication_list(tmp_set):
    intersection_set=[]
    if len(tmp_set) > 0:
        intersection_set=set(tmp_set[0])
    for sublist in tmp_set[1:]:
        intersection_set=intersection_set.intersection(set(sublist))         
    intersection_set=list(intersection_set)
    return intersection_set

# %%
def add_eb_implications(tmp_impl,snode,tcount,DGI,o_file):
	num_eb=0
	num_eb_c=0
	kk=len(tmp_impl)
	for kkn in range(0,kk):
		gn=tmp_impl[kkn][0]
		if tmp_impl[kkn][1]==1:
			DGI.add_edge(snode,int(gn+tcount),weight=0)
			#print("(",gn,", 1, 0)")
			o_file.write("--EB: " + "(" + str(gn) + ",1,0)\n")
			num_eb += 1
			#Contrapositive Implication
			if snode > tcount:
				DGI.add_edge(gn,int(snode-tcount),weight=0)
				#print("Contrapositive Implication: (",gn,", 0, 0) -> (",int(snode-tcount),", 0, 0)")
				o_file.write("--Contrapositive: (" + str(gn) + ",0,0) -> (" + str(int(snode-tcount)) + ",0,0)\n")
				num_eb_c += 1
			else:
				DGI.add_edge(gn,int(snode+tcount),weight=0)
				#print("Contrapositive Implication: (",gn,", 0, 0) -> (",snode,", 1, 0)")
				o_file.write("--Contrapositive: (" + str(gn) + ",0,0) -> (" + str(snode) + ",1,0)\n")
				num_eb_c += 1
		if tmp_impl[kkn][1]==0:
			DGI.add_edge(snode,gn,weight=0)
			#print("(",gn,", 0, 0)")
			o_file.write("--EB: " + "(" + str(gn) + ",0,0)\n")
			num_eb += 1
			#Contrapositive Implication
			if snode > tcount:
				DGI.add_edge(int(gn+tcount),int(snode-tcount),weight=0)
				#print("Contrapositive Implication: (",gn,", 1, 0) -> (",int(snode-tcount),", 0, 0)")
				o_file.write("--Contrapositive: (" + str(gn) + ",1,0) -> (" + str(int(snode-tcount)) + ",0,0)\n")
				num_eb_c += 1
			else:
				DGI.add_edge(int(gn+tcount),int(snode+tcount),weight=0)
				#print("Contrapositive Implication: (",gn,", 1, 0) -> (",snode,", 1, 0)")
				o_file.write("--Contrapositive: (" + str(gn) + ",1,0) -> (" + str(snode) + ",1,0)\n")
				num_eb_c += 1
	return num_eb


# %%
def eb_implications(snode,tcount,direct_indirect_contra_impl,levelNum,gtype,fanin,value,EventList,faninlist,DGI,maxlevels,num_gate_per_level,gate_at_level,fanout,fanoutlist,Gate,o_file,max_depth):
	num_eb=0
	if snode > tcount:
		#print("EB Implications of (",snode-tcount,",1",",0",")")
		o_file.write("EB Implications:\n")
		sn=snode-tcount
	else:
		#print("EB Implications of (",snode,",0",",0",")")
		o_file.write("EB Implications:\n")
		sn=snode

	n=len(direct_indirect_contra_impl)
	for nl in range(0,n):
		if direct_indirect_contra_impl[nl][2]==0:
			gx=direct_indirect_contra_impl[nl][0]
			val=direct_indirect_contra_impl[nl][1]
			if(levelNum[gx]<levelNum[sn]):
				flag=0
				ones=0
				zeros=0
				match gtype[gx]:
						#NAND gate
						case 7:
							for k in range(0,int(fanin[gx])):
								fn=int(faninlist[gx][k])
								if value[fn]=='0':
									flag=1
									break
								if value[fn]=='1':
									ones=ones+1   
							if val==1 and flag==0 and ones<int(fanin[gx]):
									tmp_set=impl_unjustified_nodes_and_simulate(gx,0,fanin,value,EventList,faninlist,tcount,levelNum,DGI,maxlevels,num_gate_per_level,gate_at_level,gtype,fanout,fanoutlist,Gate,max_depth)
									tmp_impl=common_implication_list(tmp_set)
									num_eb += add_eb_implications(tmp_impl,snode,tcount,DGI,o_file)
								
						#AND gate
						case 6:
							for k in range(0,int(fanin[gx])):
								fn=int(faninlist[gx][k])
								if value[fn]=='0':
									flag=1
									break
								if value[fn]=='1':
									ones=ones+1   
							if val==0 and flag==0 and ones<int(fanin[gx]):
									tmp_set=impl_unjustified_nodes_and_simulate(gx,0,fanin,value,EventList,faninlist,tcount,levelNum,DGI,maxlevels,num_gate_per_level,gate_at_level,gtype,fanout,fanoutlist,Gate,max_depth)
									tmp_impl=common_implication_list(tmp_set)
									num_eb += add_eb_implications(tmp_impl,snode,tcount,DGI,o_file)
									
						#OR gate
						case 8:
							for k in range(0,int(fanin[gx])):
								fn=int(faninlist[gx][k])
								if value[fn]=='1':
									flag=1
									break
								if value[fn]=='0':
									zeros=zeros+1   
							if val==1 and flag==0 and zeros<int(fanin[gx]):
									#print(gx)
									tmp_set=impl_unjustified_nodes_and_simulate(gx,1,fanin,value,EventList,faninlist,tcount,levelNum,DGI,maxlevels,num_gate_per_level,gate_at_level,gtype,fanout,fanoutlist,Gate,max_depth)
									tmp_impl=common_implication_list(tmp_set)
									num_eb += add_eb_implications(tmp_impl,snode,tcount,DGI,o_file)
									

						#NOR gate
						case 9:
							for k in range(0,int(fanin[gx])):
								fn=int(faninlist[gx][k])
								if value[fn]=='1':
									flag=1
									break
								if value[fn]=='0':
									zeros=zeros+1   
							if val==0 and flag==0 and zeros<int(fanin[gx]):
									tmp_set=impl_unjustified_nodes_and_simulate(gx,1,fanin,value,EventList,faninlist,tcount,levelNum,DGI,maxlevels,num_gate_per_level,gate_at_level,gtype,fanout,fanoutlist,Gate,max_depth)
									tmp_impl=common_implication_list(tmp_set)
									num_eb += add_eb_implications(tmp_impl,snode,tcount,DGI,o_file)
	print(str(num_eb) + "  EB Implications")
	print(str(num_eb) + "  EB Contrapositive Implications")
	o_file.write(str(num_eb) + "  EB Implications\n")
	o_file.write(str(num_eb) + "  EB Contrapositive Implications\n")

# %%
#lev_file="s15b" + ".lev"
#vec_file="s15b" + ".vec"
#lev_file="s27" + ".lev"
#vec_file="s27" + ".vec"

if len(sys.argv) <3:
	print("Error: Missing command-line arguments.")
	print("Usage: python implications_full_outfile.py <circuit-name> <node number>/<all>")
	sys.exit(1)

lev_file=sys.argv[1] + ".lev"
#vec_file=sys.argv[1] + ".vec"

# %%
try:
	with open(lev_file, "r") as file:
		content = file.read()
		print("File",lev_file," found")
		#print(content)
except FileNotFoundError:
	print("Error: The file ",lev_file," was not found.")

# %%
#try:
#	with open(vec_file, "r") as file:
#		content = file.read()
#		print("File",vec_file," found")
#		#print(content)
#except FileNotFoundError:
#	print("Error: The file ",vec_file," was not found.")

# %%
if sys.argv[2] == "all":
	out_file=sys.argv[1] + ".impl"
else:
	out_file=sys.argv[1] + "_" + sys.argv[2] + ".impl"

#with open(out_file,"w") as o_file:
o_file = open(out_file,"w")
o_file.write("IMPLICATION ENGINE OUTPUT:\n")

line_number=0
gate_count=0
numInputs=0
numOutputs=0
numDFFs=0
maxlevels=0
numgates=0
numPSIs=0
numPSOs=0
with open(lev_file, "r") as f:
	for line in f:
		line_number=line_number+1
		# Assuming space-separated values
		parts = line.split() 
		if line_number==1:
			count=int(parts[0])
			gate_count=count-1
			gtype=np.empty(count*2)
			fanin=np.empty(count*2)
			fanout=np.empty(count*2)
			levelNum=np.empty(count*2)
			dff=np.empty(count)
			pout=np.empty(count)
			faninlist=np.empty((count*2,count))
			fanoutlist=np.empty((count*2,count))
			gate_at_level=np.empty((5000,count*2))
			EventList=np.empty((5000,count*2))
			num_gate_per_level=np.zeros(5000,dtype=int)
			pso=np.empty(count)
			value=np.empty(count*2,dtype=object)
			psi_list=np.empty(count)
			pso_list=np.empty(count)

			
		if line_number>2:
			if line_number < count+2:
				numgates += 1
				gatenum=int(parts[0])
				f1=int(parts[1])
				f2=int(parts[2])
				f3=int(parts[3])

				gtype[gatenum]=f1
				if gtype[gatenum] > 13:
					print("gate ",gatenum," is an unimplemented gate type")
				elif gtype[gatenum] == Gate.G_INPUT.value :
					numInputs += 1
				elif gtype[gatenum] == Gate.G_OUTPUT.value :
					numOutputs += 1
					pout[numOutputs]=gatenum
				elif gtype[gatenum] == Gate.G_DFF.value :
					numDFFs += 1
					dff[numDFFs]=gatenum


				#levenNum[gatenum]= (f2+5)/5;
				levelNum[gatenum] = f2

				if f2 >= maxlevels:
					maxlevels=f2 + 5; 

				fanin[gatenum]=f3

				f4=int(parts[3+(2*f3)+1])
				fanout[gatenum]=f4

# %%
total_levels = int(maxlevels/5)

psi=np.empty(numgates+numDFFs+1)
line_number=0		
numDFFs=0
numInputs=0
numOutputs=0

with open(lev_file, "r") as f:
	for line in f:
		line_number=line_number+1
		# Assuming space-separated values
		parts = line.split() 

		if line_number>2:
			if line_number < count+2:
				gatenum=int(parts[0])
				f1=int(parts[1])
				f2=int(parts[2])
				f3=int(parts[3])
				gtype[gatenum]=f1
				if gtype[gatenum] > 13:
					print("gate ",gatenum," is an unimplemented gate type")
				elif gtype[gatenum] == Gate.G_INPUT.value :
					numInputs += 1
				elif gtype[gatenum] == Gate.G_OUTPUT.value :
					numOutputs += 1
					pout[numOutputs]=gatenum
				elif gtype[gatenum] == Gate.G_DFF.value :
					numDFFs += 1
					dff[numDFFs]=gatenum
					gtype[gatenum]= Gate.G_PSI.value
					numPSIs += 1
					psi_list[numPSIs]=gatenum
					gtype[count-1+numDFFs]= Gate.G_PSO.value
					numPSOs +=1
					pso_list[numPSOs]=count-1+numDFFs 
					pso[gatenum]=count-1+numDFFs
					psi[count-1+numDFFs]=gatenum


				#levenNum[gatenum]= (f2+5)/5;
				levelNum[gatenum] = f2
				levelNum[count-1+numDFFs] = int(maxlevels-5)


				if gtype[gatenum]==Gate.G_PSI.value:
					num_gate_per_level[f2] = num_gate_per_level[f2] + 1
					num_gate_per_level[int(maxlevels-5)] = num_gate_per_level[int(maxlevels-5)] + 1
					gate_at_level[f2][num_gate_per_level[f2]] = gatenum;
					gate_at_level[int(maxlevels-5)][num_gate_per_level[int(maxlevels-5)]] = count-1+numDFFs;
					fanin[gatenum]=0
					fanin[count-1+numDFFs]=f3
					f4=int(parts[3+(2*f3)+1])
					fanout[gatenum]=f4
					fanout[count-1+numDFFs]=0
							
					for i in range(0,f3):
						faninlist[count-1+numDFFs][i]=int(parts[3+(i+1)])
			
					for i in range(0,f4):
						fanoutlist[gatenum][i]=int(parts[3+(2*f3)+1+(i+1)])

					value[gatenum]='X'
					value[count-1+numDFFs]='X'


				
				else:
					num_gate_per_level[f2] = num_gate_per_level[f2] + 1
					gate_at_level[f2][num_gate_per_level[f2]] = gatenum;
					fanin[gatenum]=f3
					f4=int(parts[3+(2*f3)+1])
					fanout[gatenum]=f4

					for i in range(0,f3):
						faninlist[gatenum][i]=int(parts[3+(i+1)])
			
					for i in range(0,f4):
						fanoutlist[gatenum][i]=int(parts[3+(2*f3)+1+(i+1)])

					value[gatenum]='X'

print("Successfully read in circuit:")
print(numInputs," PIs.")
print(numOutputs," POs.")
print(numDFFs," DFFs.")
print(numgates," total number of gates.")
print(total_levels," levels in the circuit.")
print("\n")

o_file.write("Successfully read in circuit:\n")
o_file.write(str(numInputs) + " PIs.\n")
o_file.write(str(numOutputs) +" POs.\n")
o_file.write(str(numDFFs) + " DFFs.\n")
o_file.write(str(numgates) + " total number of gates.\n")
o_file.write(str(total_levels) + " levels in the circuit.\n")
o_file.write("\n")


# %%
tcount=int(numgates+numDFFs)
DGI=nx.MultiDiGraph()
direct_implications(tcount,gtype,fanout,fanoutlist,fanin,faninlist,psi,pso,DGI,Gate)

# %%
#display_graph(DGI)

# %%
#if sys.argv[2] != "all" and int(sys.argv[2]) < (2*tcount)+1 and gtype[int(sys.argv[2])]!=Gate.G_PSO.value:
#	i_start=int(sys.argv[2])
#	i_end=int(sys.argv[2]) + 1
#elif sys.argv[2] != "all" and gtype[int(sys.argv[2])]==Gate.G_PSO.value:
#	print(int(sys.argv[2])," is a Psuedo Primary Output and not a valid node for implication determination")
#	i_start=1
#	i_end=0
#else:
#	i_start=1
#	i_end=int((2*tcount)+1)
if sys.argv[2] == "all":
	i_start=1
	i_end=int((2*tcount)+1)
else:
	if (int(sys.argv[2]) >= (2*tcount)+1):
		print(int(sys.argv[2])," is out of range and not a valid node for implication determination")
		i_start=1
		i_end=0
	else:
		if int(sys.argv[2]) > tcount:
			if gtype[int(sys.argv[2])-tcount]==Gate.G_PSO.value:
				print((int(sys.argv[2])-tcount)," is a Psuedo Primary Output and not a valid node for implication determination")
				i_start=1
				i_end=0
			else:
				i_start=int(sys.argv[2])
				i_end=int(sys.argv[2]) + 1
		else:
			if gtype[int(sys.argv[2])]==Gate.G_PSO.value:
				print(int(sys.argv[2])," is a Psuedo Primary Output and not a valid node for implication determination")
				i_start=1
				i_end=0
			else:
				i_start=int(sys.argv[2])
				i_end=int(sys.argv[2]) + 1


total_direct_implications=0
total_indirect_implications=0
total_indirect_eb_implications=0
#for i_impl in range(1,(2*tcount)+1):
for i_impl in range(i_start,i_end):
	snode=i_impl
	#snode=25
	#snode=17
	if snode > tcount:
		gt=snode-tcount
	else:
		gt=snode
	if gtype[gt]!=Gate.G_PSO.value:
		EventList=np.zeros((5000,count*2))

		for tgates in range(1,numgates+numDFFs+1):
			value[tgates]='X'

		if snode > tcount:
			#print("Direct Implications of (",snode-tcount,",1",",0",")")
			o_file.write("---------------------------------------------------\n")
			o_file.write("Implications of (" + str(snode-tcount) + ",1,0)\n")
			o_file.write("---------------------------------------------------\n")
			o_file.write("Direct Implications:\n")
			print("Implications of (",snode-tcount,",1",",0",")")
		else:
			#print("Direct Implications of (",snode,",0",",0",")")
			o_file.write("---------------------------------------------------\n")
			o_file.write("Implications of (" + str(snode) + ",0,0)\n")
			o_file.write("---------------------------------------------------\n")
			o_file.write("Direct Implications:\n")
			print("Implications of (",snode,",0",",0",")")

		#direct_impl=[]
		#print(direct_impl)
		#print(type(direct_impl))
		#direct_impl=list(set(transitive_closure(snode,tcount,EventList,value,levelNum,DGI)))
		max_depth=5
		direct_impl=list(set(transitive_closure_with_revisits(snode,tcount,EventList,value,levelNum,DGI,max_depth)))
		#print(direct_impl)
		o_file.write(str(direct_impl))
		o_file.write("\n")
		o_file.write(str(len(direct_impl))+" Direct Implications\n")
		print(len(direct_impl)," Direct Implications")
		total_direct_implications += int(len(direct_impl))


		indirect_and_contrapositive_implications(snode, tcount, maxlevels,num_gate_per_level,gate_at_level,EventList,gtype, value, fanin, faninlist, fanout, fanoutlist, levelNum, DGI, Gate, o_file)

		EventList=np.zeros((5000,count*2))

		for tgates in range(1,numgates+numDFFs+1):
			value[tgates]='X'

		#snode=25
		if snode > tcount:
			#print("Direct and Indirect Implications of (",snode-tcount,",1",",0",")")
			o_file.write("Direct + Indirect Implications:\n")
			sn=snode-tcount
		else:
			#print("Direct and Indirect Implications of (",snode,",0",",0",")")
			o_file.write("Direct + Indirect Implications:\n")
		
			sn=snode
		#direct_indirect_contra_impl=[]
		#print(direct_indirect_contra_impl)
		#direct_indirect_contra_impl=list(set(transitive_closure(snode,tcount,EventList,value,levelNum,DGI)))
		direct_indirect_contra_impl=list(set(transitive_closure_with_revisits(snode,tcount,EventList,value,levelNum,DGI,max_depth)))
		#print(direct_indirect_contra_impl)
		o_file.write(str(direct_indirect_contra_impl))
		o_file.write("\n")
		o_file.write(str(len(direct_indirect_contra_impl))+" Direct+Indirect Implications\n")
		print(len(direct_indirect_contra_impl)," Direct+Indirect Implications")
		total_indirect_implications += int(len(direct_indirect_contra_impl))
		#unique_temp_impl=set(temp_impl)
		#print(unique_temp_impl)
		#stage2_impl = [0]*tcount*2
		#print(stage2_impl)
		#stage2_impl.insert(snode-1,unique_temp_impl)
		#print(stage2_impl)


		eb_implications(snode,tcount,direct_indirect_contra_impl,levelNum,gtype,fanin,value,EventList,faninlist,DGI,maxlevels,num_gate_per_level,gate_at_level,fanout,fanoutlist,Gate,o_file,max_depth)

		if snode > tcount:
			#print("Direct, Indirect and EB Implications of (",snode-tcount,",1",",0",")")
			o_file.write("Direct+Indirect+EB Implications:\n")
			sn=snode-tcount
		else:
			#print("Direct, Indirect and EB Implications of (",snode,",0",",0",")")
			o_file.write("Direct+Indirect+EB Implications:\n")
			sn=snode
		#direct_indirect_eb_impl=list(set(transitive_closure(snode,tcount,EventList,value,levelNum,DGI)))
		direct_indirect_eb_impl=list(set(transitive_closure_with_revisits(snode,tcount,EventList,value,levelNum,DGI,max_depth)))
		#print(direct_indirect_eb_impl)
		o_file.write(str(direct_indirect_eb_impl))
		o_file.write("\n")
		o_file.write(str(len(direct_indirect_eb_impl))+" Total (Direct+Indirect+EB) Implications\n")
		print(str(len(direct_indirect_eb_impl)) + "  Total (Direct+Indirect+EB) Implications")
		total_indirect_eb_implications += int(len(direct_indirect_eb_impl))

print("Total Implications: ",total_indirect_eb_implications)
print("Total Direct Implications: ",total_direct_implications)
print("Total Indirect non-EB Implications: ",(total_indirect_implications-total_direct_implications))
print("Total Indirect EB Implications: ",(total_indirect_eb_implications-total_indirect_implications))
print("Total Indirect Implications: ",(total_indirect_eb_implications-total_direct_implications))

final_total_implications=0
for i_impl in range(i_start,i_end):
	snode=i_impl
	direct_indirect_eb_impl=list(set(transitive_closure_with_revisits(snode,tcount,EventList,value,levelNum,DGI,max_depth=5)))
	final_total_implications += int(len(direct_indirect_eb_impl))
print("Final Total Implications: ",final_total_implications)

o_file.close()

