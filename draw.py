import matplotlib.pyplot as plt
import networkx as nx

def drawDFA(states, transitions):
    edge_labels = {}
    G = nx.DiGraph()
    G.add_nodes_from([min(states), max(states)])
    for state in transitions:
        for value in transitions[state]:
            for node in transitions[state][value]:
                if state == node:
                    print((state, node), value)
                G.add_edge(state, node)
                edge_labels[(state, node)] = value
    pos = nx.spring_layout(G)
    plt.subplot(111)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.25)
    plt.show()

#states = [0, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#transitions = {0: {'#': [4, 3]}, 1: {'b': [-1]}, 2: {'b': [1]}, 3: {'a': [2]}, 4: {'#': [6, 7]}, 5: {'#': [3, 4]}, 6: {'b': [8]}, 7: {'a': [9]}, 8: {'#': [5]}, 9: {'#': [5]}}
#states = 'ABCDE'
#transitions = {'A': {'a': ['B'], 'b': ['C']}, 'B': {'a': ['B'], 'b': ['D']}, 'C': {'a': ['B'], 'b': ['C']}, 'D': {'a': ['B'], 'b': ['E']}, 'E': {'a': ['B'], 'b': ['C']}}
#edge_labels = {}

#G = nx.DiGraph()
#
#G.add_nodes_from([min(states), max(states)])
#for state in transitions:
#    for value in transitions[state]:
#        for node in transitions[state][value]:
#            if state == node:
#                print((state, node), value)
#            G.add_edge(state, node)
#            edge_labels[(state, node)] =  value
#
#pos = nx.spring_layout(G)
#plt.subplot(111)
#nx.draw(G, pos, with_labels=True)
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.25)
#plt.show()
