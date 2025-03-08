FROM python:3.8.10
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /wms-customer-segmentation
COPY . /wms-customer-segmentation
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8501
CMD streamlit run app.py --server.headless true --browser.serverAddress="0.0.0.0" --server.enableCORS false --browser.gatherUsageStats false
