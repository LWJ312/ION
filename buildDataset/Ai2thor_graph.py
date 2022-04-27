import networkx as nx
import json
from networkx.readwrite import json_graph

def get_next(num_node,gridSize):
    rotlist=[0,45,90,135,180,225,270,315]
    x=num_node[0]
    z=num_node[1]
    rot=num_node[2]
    hoz=num_node[3]
    rot_idx=rotlist.index(rot)
    if rot == 0:
        z += gridSize
    elif rot == 90:
        x += gridSize
    elif rot == 180:
        z -= gridSize
    elif rot == 270:
        x -= gridSize
    elif rot == 45:
        z += gridSize
        x += gridSize
    elif rot == 135:
        z -= gridSize
        x += gridSize
    elif rot == 225:
        z -= gridSize
        x -= gridSize
    elif rot == 315:
        z += gridSize
        x -= gridSize
    next1=str('%.2f' % x) + '|' + str('%.2f' % z) + '|'+ str(int(rot)) + '|' + str(int(hoz))
    next2=str('%.2f' % num_node[0]) + '|' + str('%.2f' % num_node[1]) + '|'+ str(int(rot)) + '|' + str(int(30-hoz))
    if rot_idx!=7:
        next3=str('%.2f' % num_node[0]) + '|' + str('%.2f' % num_node[1]) + '|'+ str(rotlist[rot_idx+1]) + '|' + str(int(hoz))
    else:
        next3 = str('%.2f' % num_node[0]) + '|' + str('%.2f' % num_node[1]) + '|' + str(
            rotlist[0]) + '|' + str(int(hoz))
    next4 = str('%.2f' % num_node[0]) + '|' + str('%.2f' % num_node[1]) + '|' + str(rotlist[rot_idx-1]) + '|' + str(int(hoz))
    next=[next1,next2,next3,next4]
    return next

def add_next(node,next,nodes,graph):
    if next[0] in nodes:
        graph.add_edge(node, next[0])
    graph.add_edge(node, next[1])
    graph.add_edge(node, next[2])
    graph.add_edge(node, next[3])

def generate_graph(save_dir,gridSize,positions):
    nodes=[]
    for pos in positions:
        rotation=-45
        for i in range(8):
            rotation+=45
            pos_str = str('%.2f' % pos['x']) + '|' + str('%.2f' % pos['z']) + '|'+ str(rotation) + '|' + str(0)
            nodes.append(pos_str)
            pos_str = str('%.2f' % pos['x']) + '|' + str('%.2f' % pos['z']) + '|'+ str(rotation) + '|' + str(30)
            nodes.append(pos_str)
    graph=nx.DiGraph()
    graph.add_nodes_from(nodes)
    for node in nodes:
        str_list=node.split('|')
        num_node=[float(x) for x in str_list]
        next = get_next(num_node,gridSize)
        add_next(node,next,nodes,graph)
    with open(save_dir+'/graph.json', "w") as outfile:
        data = json_graph.node_link_data(graph)
        json.dump(data, outfile)
