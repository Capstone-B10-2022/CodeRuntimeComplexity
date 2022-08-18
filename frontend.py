import streamlit as st
import os
# import torch
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
    for i in Codeset:
        print(i)
    # preds = glob.glob("dataset/v{}/*.*".format(st.session_state['dcount']), recursive=True)

    # results = model(preds)
    # # results.code
    # results.render()
    # os.mkdir("output/v{}".format(st.session_state['dcount']))
    # for index,im in enumerate(results.code):
        
    #     img = Image.fromarray(im)
    #     img.save('output/v{}/{}'.format(st.session_state['dcount'], imgname[index]))

    #     st.image('output/v{}/{}'.format(st.session_state['dcount'], imgname[index]))

    # st.button('Predict')

# dcount = 0
# if __name__ == '__main__':
#     model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, _verbose=False)
#     model.classes = [0]
#     main()
main()