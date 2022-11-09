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
import pickle
import shutil
import streamlit as st

def integrated_main():

    base_directory = r"C:\Users\nikhi\OneDrive\Documents\gitUploads\Frontend\dataset"
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    
    if os.path.exists(base_directory + '\\pred.npy'):
        pred = np.load(base_directory + '\\pred.npy').tolist()
        return pred

    dataset = max(glob.glob(os.path.join(base_directory, '*/')), key=os.path.getmtime)
    C_node_num, Python_node_num, Java_node_num = 0, 0, 0
    C_files, Python_files, Java_files = [], [], []
    C_out, Python_out, Java_out = [], [], []
    lang_map = []


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
                lang_map.append(2)
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
                lang_map.append(1)
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
                lang_map.append(0)
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
    test = np.load(out_path)

    model = pickle.load(open(base_directory + '\\rf_lang.pkl', 'rb'), encoding='latin1')
    sc = pickle.load(open(base_directory + '\\scaler.pkl', 'rb'), encoding='latin1')

    test_df = []
    for i in range(len(test)):
        emb = test[i].tolist()
        test_df.append(emb)
    col = []
    for i in range(128):
        col.append('emb'+str(i+1))
    test_df = pd.DataFrame(test_df, columns=col)

    test_df['Language_map'] = lang_map
    test_df= sc.transform(test_df)
    class_names = ['O(logN)',  'O(N)',  'O(N2)', 'O(N3)', 'O(Nd)',  'O(NlogN)']
    pred = [class_names[i] for i in model.predict(test_df)]
    np.save(base_directory + '\\dataset\\pred.npy', pred)
    return pred