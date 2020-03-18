#import matplotlib.pyplot as plt
#import networkx as nx
from graphviz import Digraph

#def drawDFA(states, transitions):
#    edge_labels = {}
#    G = nx.DiGraph()
#    #G.add_nodes_from([min(states), max(states)])
#    for state in states:
#        G.add_node(state)
#    color_map=['blue' for i in states]
#    for state in transitions:
#        for value in transitions[state]:
#            for node in transitions[state][value]:
#                if state == node:
#                    print((state, node), value)
#                    color_map[states.index(state)] = 'green'
#                G.add_edge(state, node)
#                edge_labels[(state, node)] = value
#    pos = nx.spring_layout(G)
#    plt.subplot(111)
#    nx.draw(G, pos, node_color=color_map, with_labels=True)
#    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.25)
#    plt.show()

def drawPrettyDFA(states, transitions, accept_states):
    f = Digraph('finite_state_machine', filename='fsm.gv')
    f.attr(rankdir='LR', size='8,5')
    f.attr('node', shape='doublecircle')
    for accept in accept_states:
        f.node(str(accept))
    f.attr('node', shape='circle')
    for state in transitions:
        for value in transitions[state]:
            for node in transitions[state][value]:
                f.edge(str(state), str(node), label=str(value))
    f.view()

#states = [0, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#transitions = {0: {'#': [4, 3]}, 1: {'b': [-1]}, 2: {'b': [1]}, 3: {'a': [2]}, 4: {'#': [6, 7]}, 5: {'#': [3, 4]}, 6: {'b': [8]}, 7: {'a': [9]}, 8: {'#': [5]}, 9: {'#': [5]}}
#states = 'ABCDE'
#transitions = {'A': {'a': ['B'], 'b': ['C']}, 'B': {'a': ['B'], 'b': ['D']}, 'C': {'a': ['B'], 'b': ['C']}, 'D': {'a': ['B'], 'b': ['E']}, 'E': {'a': ['B'], 'b': ['C']}}
#edge_labels = {}
#G = nx.DiGraph()
#color_map=['blue' if i == 'A' else 'red' if i == 'E' else 'purple' for i in states]
##G.add_nodes_from([min(states), max(states)])
#for state in states:
#    G.add_node(state)
#for state in transitions:
#    for value in transitions[state]:
#        for node in transitions[state][value]:
#            if state == node:
#                print((state, node), value)
#                print(states.index(state))
#                color_map[states.index(state)] = 'green'
#            G.add_edge(state, node)
#            edge_labels[(state, node)] =  value
#
#pos = nx.spring_layout(G)
#plt.subplot(111)
#print(color_map)
#nx.draw(G, pos, node_color=color_map, with_labels=True)
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.25)
#plt.show()
