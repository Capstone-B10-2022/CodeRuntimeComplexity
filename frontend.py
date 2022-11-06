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

global pred
gcount = 0

base_directory = 'C:/Users/nikhi/OneDrive/Documents/gitUploads/Frontend/dataset'
def data_upload():
    st.title('Upload')
    code = st.file_uploader("Choose Code files in Python, C or Java and upload Zip file", type = ['zip'] , help = "Choose Code files in Python, C or Java and upload Zip file")
    
    if 'dcount' not in st.session_state:
        st.session_state['dcount'] = 0

    if not code:
        return
        
    with zipfile.ZipFile(code,"r") as zipf:
        st.session_state['dcount'] += 1
        zipf.extractall("dataset/v{}".format(st.session_state['dcount']))

    Codeset = os.listdir("dataset/v{}".format(st.session_state['dcount']))

def data_show():
    global pred
    global gcount
    if gcount == 0:
        pred = integrated_main()
        gcount += 1

    st.title("MetaData and Dataset")

    c = st.container()
    c.write('___________  FILES  ___________')
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
            file_details = {"filename":code_path,
                            "filetype":file_type,
                            "filesize":file_stat.st_size,
                            "TimeComplexity":pred[count]}
            count += 1
            st.write(file_details)
            st.text(all.read())

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
    global gcount
    pages = {
        "Upload": data_upload,
        "Dataset": data_show,
        "Files": data_metadata,
    }
    st.title('Time Complexity Prediction')
    st.sidebar.title('Time Complexity Prediction')
    selected_page = st.sidebar.radio("Select a page", pages.keys())
    pages[selected_page]()
    gcount += 1

main()