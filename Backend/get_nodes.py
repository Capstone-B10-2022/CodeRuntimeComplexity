from capstone_c_ast import c_nodes
from capstone_java_ast import java_nodes
from capstone_python_ast import python_nodes

filename = 'testPP.c' #input file
target = 'nodes.txt' #output file
#c_nodes(filename,target)
lang=""

if 'c' in filename:
    lang='C'
    c_nodes(filename,target)
elif 'py' in filename:
    lang='Python'
    python_nodes(filename,target)
elif 'java' in filename:
    lang='Java'
    java_nodes(filename,target)
else:
    print('Invalid file type')