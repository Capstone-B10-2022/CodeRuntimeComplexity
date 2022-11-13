from Backend.integrated import *
from Backend.capstone_c_ast import *
from Backend.capstone_python_ast import *
from Backend.capstone_java_ast import *
from Backend.script import *
from Backend.vector import *

import streamlit as st
import os
from PIL import Image
import glob
import zipfile
import shutil
import math

import warnings as wr
wr.filterwarnings("ignore")

base_directory = os.getcwd() + '\\Dataset'

def data_upload():
    st.title('Upload')
    code = st.file_uploader("Choose Code files in Python, C or Java and upload Zip file", type = ['zip'] , help = "Choose Code files in Python, C or Java and upload Zip file")


    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    shutil.rmtree(base_directory)
    
    if 'dcount' not in st.session_state:
        st.session_state['dcount'] = 0

    if not code:
        return
    
    with zipfile.ZipFile(code,"r") as zipf:
        st.session_state['dcount'] += 1
        zipf.extractall("Dataset/v{}".format(st.session_state['dcount']))

    Codeset = os.listdir("Dataset/v{}".format(st.session_state['dcount']))


def data_show():

    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    try: 
        pred = integrated_main()
    except ValueError as ve:
        st.title("MetaData and Dataset")
        c = st.container()
        c.write('___________  FILES  ___________')
        c.write('\n\n')
        c.write('NO FILES')
        return

    st.title("MetaData and Dataset")

    c = st.container()
    c.write('___________  FILES  ___________')
    c.write('\n\n')
    Codeset = base_directory + '\\v*'
    
    count = 0
    for i in ['*.c','*.py','*.java']:
        for code_path in sorted(glob.glob(os.path.join(Codeset, i))):
            code_path = code_path.replace("/","\\")
            all = open(code_path)
            file_stat = os.stat(code_path)
            if i == '*.py':
                file_type = 'Python'
            elif i == '*.c':
                file_type = 'C'
            else:
                file_type = 'Java'
            file_details = {
                            "filename":code_path,
                            "filetype":file_type,
                            "filesize":file_stat.st_size,
                            "TimeComplexity":pred[count]
                            }
            count += 1
            st.write(file_details)
            st.text(all.read())
            st.write('\n')

def data_metadata():
    st.title("Files")
    filelist=[]
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            filename = os.path.join(root, file)
            path = filename
            if getParent(path,).split('\\')[0][0] == 'v': 
                filelist.append(filename)
    st.write(filelist)

def main():
    pages = {
        "Upload": data_upload,
        "Dataset": data_show,
        "Files": data_metadata,
    }
    st.title('Time Complexity Prediction')
    st.sidebar.title('Time Complexity Prediction')
    selected_page = st.sidebar.radio("Select a page", pages.keys())
    pages[selected_page]()

main()