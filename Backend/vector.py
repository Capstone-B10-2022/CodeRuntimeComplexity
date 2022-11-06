import networkx as nx
import matplotlib.pyplot as plt
from karateclub.graph_embedding import Graph2Vec
import numpy as np
from tqdm import tqdm
import os
import glob
from pathlib import Path
import os.path

def get_nodes(filename):  
    #lists to get the parents and the children
    parents=[]
    children=[]
    
    f = open(filename, "r")
    for x in f:
        
        #print(x)
        #print(x.split(","))

        #the first node is the parent and the second one is the child
        if(x[0]=='\n'):
          continue
        x1 = x.split(",",1)
        #print(x1)
        parent,child=x1[0],x1[1]
        #parent,child=x.split(",")[0],x.split(",")[1]
        
        parent,child = x1[0],x1[1]

        #appending the nodes to the respective list
        parents.append(parent)
        children.append(child[:-1])
    #
    nodes = list(set(set(parents).union(set(children))))
    #for i in nodes:
      #print(i)
    return [parents,children,nodes]


def get_node_labels(nodes,parents,children):
    #
    labels_list=list()
    for i in nodes:
        i1 = i.split("--")[0]
        #print(i)
        labels_list.append(int(i1))
    labels_list.sort()

    label_keys=dict()
    for i in range(len(labels_list)):
        label_keys[labels_list[i]]=i

    labels=dict()
    for i in nodes:
        i1=i.split("--")
        key=label_keys[int(i1[0])]
        labels[key]=i1[1]

    sorted_labels = sorted(labels.items(), key=lambda x: x[0])
    
    edges = []
    for i,j in zip(parents,children):
        parent=i.split("--")[0]
        child=j.split("--")[0]
        edges.append((label_keys[int(parent)],label_keys[int(child)]))
    edges.sort()

    label=dict()
    for i in sorted_labels:
        label[i[0]]=i[1]
    #print(label)
    #print(edges)
    return [label,edges]

def graph(edges,label):
    #print(len(edges))
    #print(edges)
    tree2graph = nx.DiGraph()
    tree2graph.add_edges_from(edges)
    for node in tree2graph.nodes():
        tree2graph.nodes[node]['feature'] = label[node]
    return tree2graph

def get_graph(file):
    l=get_nodes(file)
    parents,children,nodes = l[0],l[1],l[2] 
    l=get_node_labels(nodes,parents,children)
    #print(l)
    label,edges=l[0],l[1] 
    g=graph(edges,label)
    return g

# Graph2Vec attributed example
def get_embedding(graphs):
    model = Graph2Vec(attributed=True)
    model.fit(graphs)
    embed = model.get_embedding()
    return embed


def getParent(path, levels = 1):
    common = path
    for i in range(levels + 1):
        common = os.path.dirname(common)
    return os.path.relpath(path, common)


# if __name__ == '__main__':
    # directory = r'C:\Users\nikhi\OneDrive\Documents\gitUploads\Capstone_Dataset'    # Base Directory
    # print(directory)
    # lang = ['C','Python','Java']
    # directories = []
    # for i in lang:
    #     directories.append(directory + '\\' + i + "_Nodes")

    # x = []
    # y = []
    # total = []
    # classes = set()

    # for directory in tqdm(list(directories)):
    #     for root, subdirectories, files in tqdm(list(os.walk(directory))):
    #         for subdirectory in subdirectories:
    #             classes.add(subdirectory)
    #         for file in tqdm(list(files)):
    #             path = os.path.join(root, file)

    #             total.append(path)

    #             cmplx_class = getParent(path,).split('\\')[0]
    #             node_lang = getParent(path,2).split('\\')[0]
    #             fname = Path(path).stem

    #             if node_lang == 'Python_Nodes':
    #                 file_type = 'Python'
    #             elif node_lang == 'C_Nodes':
    #                 file_type = 'C'
    #             else:
    #                 file_type = 'Java'
                
    #             entry = (cmplx_class,fname,file_type)
    #             y.append(entry)
    
    # # print(total)      # Paths of all files
    # # print(classes)    # Total Complexity Classes
    # # print(y)          # list of Tuples -> (Complexity Class, file name, Lang)

    # graphs = []

    # for i in total:
    #     g = get_graph(i)
    #     graphs.append(g)

    # embeddings = []
    # embeddings=get_embedding(graphs)

    # out_path = r"C:\Users\nikhi\OneDrive\Documents\gitUploads\Capstone_Dataset\y.txt"
    # with open( out_path, 'w', encoding='utf-8') as fp:
    #     fp.write('\n'.join(f'{tup[0]} {tup[1]} {tup[2]}' for tup in tqdm(list(y))))

    # out_path = r"C:\Users\nikhi\OneDrive\Documents\gitUploads\Capstone_Dataset\x.txt"
    # with open( out_path , 'w') as fp:
    #     for i in tqdm(list(embeddings)):
    #         fp.write("%s\n" % i)

    # out_path = r"C:\Users\nikhi\OneDrive\Documents\gitUploads\Capstone_Dataset\x.npy"
    # with open(out_path, 'wb') as fp:
    #     np.save(fp,embeddings)

    # print(embeddings.shape)

