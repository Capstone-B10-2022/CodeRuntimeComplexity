import os
from pathlib import Path
import glob
from tqdm import tqdm

def C_PP( ip_path, op_path):
    Preprocessed = op_path
    cmd = ''
    pycpath = r'C:\Users\nikhi\OneDrive\Documents\Engineering-3\6thSEM\Capstone\code\pycparser\utils\fake_libc_include' # Path to pycparsers fake_lib_include
    ip_fname = Path(ip_path).stem
    op_path = Preprocessed+ '\\' + ip_fname + '_PP.c'     # Output file name = ip_fname_PP.c
    cmd = 'gcc -E -I' + pycpath + ' ' + ip_path + ' > ' + op_path
    os.system(cmd)

# def script_main(directory):
#     pycpath = r'C:\Users\nikhi\OneDrive\Documents\Engineering-3\6thSEM\Capstone\code\pycparser\utils\fake_libc_include' # Path to pycparsers fake_lib_include
#     # directory = r'C:\Users\nikhi\OneDrive\Documents\gitUploads\Capstone_Dataset\C' # Base Directory with all C folders
#     for root, subdirectories, files in tqdm(list(os.walk(directory))):
#         for subdirectory in tqdm(list(subdirectories)):
#             ip_path = os.path.join(root, subdirectory)
#             # op_path = ip_path.replace('\C\\','\Preprocessed_C\\')
#             op_path = ip_path + '\Preprocessed_C\\'
#             if not os.path.exists(op_path):
#                 os.makedirs(op_path)
#             C_PP(ip_path,op_path)