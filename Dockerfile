FROM tensorflow/tensorflow:1.14.0-gpu-py3

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt