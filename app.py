import streamlit as st
import pandas as pd 
import pickle
import numpy as np

prediction_model = pickle.load(open('./models/customer-segmenation-model.pkl', 'rb'))

def pre_process(data):
    features = ["sip_amount", "networth", "age"]
    data = data[features]
    updated_data = ((data - data.min())/(data.max() - data.min())) * 9 + 1
    return updated_data

@st.cache_data
def store_output_data(data):
    return data.to_csv(index=False).encode('utf-8')   

st.header('Customer Segmentation')

tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs([r"$\textsf{\large Test Model}$",r"$\textsf{\large Train Model}$",r"$\textsf{\large Flow}$", r"$\textsf{\large Architecture}$", r"$\textsf{\large Info}$"])

with tab_1:
    uploaded_file = st.file_uploader("Select bank customer data file")

    if uploaded_file is not None:
        st.write("Bank customer data for prediction")
        input_data = pd.read_csv(uploaded_file)
        st.write(input_data)
        processed_input_data = pre_process(input_data)

    if st.button('Segment Customers'):
        if uploaded_file is None:
            st.warning('Upload bank customer data file', icon="⚠️")
        else: 
            pred = prediction_model.predict(processed_input_data)
            label_1 = input_data[pred == 0]
            label_2 = input_data[pred == 1]
            label_3 = input_data[pred == 2]

            with st.expander("Aged Agressive Investor with Medium Networth"):
                st.write(label_1)      
                csv = store_output_data(label_1)

                st.download_button(
                    "Export label 1",
                    csv,
                    "Aged Agressive Investor with Medium Networth.csv", 
                    "text/csv",
                    key='download-csv'
                    )

            with st.expander("Young Passive Investor with Low Networth"): 
                st.write(label_2)
                csv = store_output_data(label_2)

                st.download_button(
                    "Export label 2",
                    csv,
                    "Young Passive Investor with Low Networth.csv", 
                    "text/csv",
                    key='download-label-2-csv'
                    )
                
            with st.expander("Middle Age Passive Investor with High Networth"):
                st.write(label_3)
                csv = store_output_data(label_3)

                st.download_button(
                    "Export label 3",
                    csv,
                    "Middle Age Passive Investor with High Networth.csv", 
                    "text/csv",
                    key='download-label-3-csv'
                    )
with tab_2:
    pass

with tab_3:
    st.markdown("Training flowchart:")
    st.image("./images/customer-segmentation-training-flowchat.png", caption='customer-segmentation training flowchart')
    st.markdown("Prediction flowchart:")
    st.image("./images/customer-segmentation-prediction-flowchart.png", caption="customer-segmentation prediction flowchart")

with tab_4:
    pass

with tab_5:
    with open("./tabs/info.md", "r") as f:
        info = f.read()
    st.markdown(info)