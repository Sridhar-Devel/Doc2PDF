
FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y unoconv && \
    apt-get install -y fonts-comic-neue && \
    apt-get install -y supervisor && \  
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/pdf_creator.py /app/pdf_creator.py
COPY supervisord.conf /etc/supervisord.conf

EXPOSE 5000

CMD ["supervisord", "-c", "/etc/supervisord.conf"]

