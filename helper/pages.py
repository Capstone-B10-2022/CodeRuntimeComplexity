# Helper functions
def data_preprocess(state, process_table_sidebar):
    autosave_session(state)
    st.title("Data Preprocess")
    ...
def training(state, process_table_sidebar):
    autosave_session(state)
    st.title("Train Model")
    ...
... # evaluation, prediction, save_and_load, free_coding, deployment
# Implementation
def main(state)
    pages = {
        "Preprocessing": data_preprocess,
        "Training": training,
        "Evaluation": evaluation,
        "Prediction": prediction,
        "Save & Load": save_and_load,
        "Free Coding": free_coding,    
        "Deployment": deployment}
state.page = st.sidebar.radio("CRISP-DM", 
    tuple(pages.keys()),                             
    index=tuple(pages.keys()).index(state.page) if state.page
                                                else   0)
   if st.sidebar.button("Logout"):
      state.clear()