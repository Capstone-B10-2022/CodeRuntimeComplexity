# from Backend.integrated import *
from Backend.capstone_c_ast import *
from Backend.capstone_python_ast import *
from Backend.capstone_java_ast import *
from Backend.script import *
from Backend.vector import *

from tqdm import tqdm
import os
import glob
import joblib
import pandas as pd
import numpy as np

def integrated_main():

    base_directory = r"C:\Users\nikhi\OneDrive\Documents\gitUploads\Frontend\dataset"

    dataset = max(glob.glob(os.path.join(base_directory, '*/')), key=os.path.getmtime)
    C_node_num, Python_node_num, Java_node_num = 0, 0, 0
    C_files, Python_files, Java_files = [], [], []
    C_out, Python_out, Java_out = [], [], []


    for root, subdirectories, files in tqdm(list(os.walk(dataset))):
        for file in tqdm(list(files)):
            path = os.path.join(root, file)
            split_tup = os.path.splitext(path)
            file_name = Path(path).stem
            file_extension = split_tup[1]

            if file_extension == '.c':
                ip_path = path
                op_path = base_directory + '\Preprocessed_C\\'
                if not os.path.exists(op_path):
                    os.makedirs(op_path)
                C_PP(ip_path,op_path)
                C_files.append(ip_path)
                nodes_path = base_directory + '\C_nodes\\'
                if not os.path.exists(nodes_path):
                    os.makedirs(nodes_path)
                filename = op_path + '\\' + file_name + '_PP.c'
                target = nodes_path + "node" + str(C_node_num) + '.txt'
                C_out.append(target)
                C_node_num += 1
                c_nodes(filename,target)
            
            elif file_extension == '.py':
                ip_path = path
                Python_files.append(ip_path)
                nodes_path = base_directory + '\Python_nodes\\'
                if not os.path.exists(nodes_path):
                    os.makedirs(nodes_path)
                filename = path
                target = nodes_path + "node" + str(Python_node_num) + '.txt'
                Python_out.append(target)
                Python_node_num += 1
                python_nodes(filename,target)

            else:
                ip_path = path
                Java_files.append(ip_path)
                nodes_path = base_directory + '\Java_nodes\\'
                if not os.path.exists(nodes_path):
                    os.makedirs(nodes_path)
                filename = path
                target = nodes_path + "node" + str(Java_node_num) + '.txt'
                Java_out.append(target)
                Java_node_num += 1
                java_nodes(filename,target)
    
    total = C_out + Python_out + Java_out
    graphs = []

    for i in total:
        g = get_graph(i)
        graphs.append(g)

    embeddings = []
    embeddings=get_embedding(graphs)
    out_path = base_directory + '\\x.npy'
    with open(out_path, 'wb') as fp:
        np.save(fp,embeddings)
    
    base_directory = r"C:\Users\nikhi\OneDrive\Documents\gitUploads\Frontend"
    x = np.load(out_path)

    df = []
    for i in range(len(x)):
        emb = x[i].tolist()
        # emb.append(y[i])
        df.append(emb)
    col = []
    for i in range(128):
        col.append('emb'+str(i+1))
    # col.append('classes')
    df = pd.DataFrame(df, columns=col)

    X = df.iloc[:,0:128].values
    # model = joblib.load(base_directory + '\\random_forest.joblib')
    # print(X)
    # print(type(X))
    # print(X.shape())

    class_names = ['O(1)',  'O(2n)',  'O(N!)',  'O(N)',  'O(N2)',  'O(N3)',  'O(Nd)',  'O(NlogN)', 'O(logN)','O(sqrt(N))']
    # y_pred = model.predict(X_test)
    # pred = [class_names[i] for i in y_pred]
    # print(pred)
    pred = [1,2,3,4,5,6]
    return pred
    
# integrated_main()
    
        