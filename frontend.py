import streamlit as st
import os
from PIL import Image
import glob
import zipfile

def main():
    st.title('Time Complexity Prediction')
    code = st.file_uploader("Choose Codes", type = ['zip'] , help = "Choose Code files in Python, C or Java and upload Zip file")
    
    if 'dcount' not in st.session_state:
        st.session_state['dcount'] = 0

    if not code:
        return
        
    with zipfile.ZipFile(code,"r") as zipf:
        st.session_state['dcount'] += 1
        zipf.extractall("dataset/v{}".format(st.session_state['dcount']))

    Codeset = os.listdir("dataset/v{}".format(st.session_state['dcount']))

    
    c = st.container()
    c.write('___________  FILES  ___________')


    Codeset = 'C:/Users/nikhi/OneDrive/Documents/gitUploads/Frontend/dataset/v1'
    for code_path in sorted(glob.glob(os.path.join(Codeset, '*.py' ))):
        code_path = code_path.replace("/","\\")
        all = open(code_path)
        file_stat = os.stat(code_path)
        file_details = {"filename":code_path, "filetype":'Python',"filesize":file_stat.st_size}
        st.write(file_details)
        st.text(all.read())

    for code_path in sorted(glob.glob(os.path.join(Codeset, '*.c' ))):
        code_path = code_path.replace("/","\\")
        all = open(code_path)
        file_stat = os.stat(code_path)
        file_details = {"filename":code_path, "filetype":'C',"filesize":file_stat.st_size}
        st.write(file_details)
        st.text(all.read())

    for code_path in sorted(glob.glob(os.path.join(Codeset, '*.java' ))):
        code_path = code_path.replace("/","\\")
        all = open(code_path)
        file_stat = os.stat(code_path)
        file_details = {"filename":code_path, "filetype":'C',"filesize":file_stat.st_size}
        st.write(file_details)
        st.text(all.read())


main()

# import streamlit as st
# import os

# filename = st.text_input('Enter a file path:')
# try:
#     with open(filename) as input:
#         st.text(input.read())
# except FileNotFoundError:
#     st.error('File not found.')

# file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
# st.write(file_details)

# import os

# file_stat = os.stat('my_file.txt')
# print(file_stat.st_size)

# st.subheader(all.read(), anchor=None)


# import os
# import streamlit as st
# filelist=[]
# for root, dirs, files in os.walk("C:/Users/nikhi/OneDrive/Documents/gitUploads/Frontend/dataset/v1"):
#       for file in files:
#              filename=os.path.join(root, file)
#              filelist.append(filename)
# st.write(filelist)