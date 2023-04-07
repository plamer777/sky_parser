FROM ubuntu:latest
WORKDIR /sky_parser
COPY requirements.txt .
COPY prepare_files.sh .
RUN /bin/bash prepare_files.sh
RUN pip install -r requirements.txt
COPY . .
CMD python3 main.py
