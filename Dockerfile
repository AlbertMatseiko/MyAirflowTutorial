FROM apache/airflow:2.8.0

USER root

RUN sudo apt-get update \
    && sudo apt-get install -y wget ghostscript tesseract-ocr tesseract-ocr-rus \
    && export TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata \
    && wget -O $TESSDATA_PREFIX/equ.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/equ.traineddata \
    && rm -rf /var/lib/apt/lists/*

# Add your additional Dockerfile instructions for the Airflow setup here