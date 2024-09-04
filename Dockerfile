FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3.10
RUN apt install -y python3-pip
RUN pip3 install requests
RUN pip3 install torchxrayvision
RUN pip3 install pydicom
RUN pip3 install pynetdicom

WORKDIR /app

COPY entrypoint.sh /app

ADD src /app

RUN mkdir /app/results_classification
RUN mkdir /app/results_dicom_sr

RUN chmod +x /app/entrypoint.sh

CMD ["sh", "/app/entrypoint.sh"]