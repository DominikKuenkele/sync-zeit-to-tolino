FROM python:latest

RUN apt-get install -y wget tar

RUN apt-get update && \
    apt-get install -y firefox-esr

RUN wget -q -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz && \
    tar -zxf /tmp/geckodriver.tar.gz -C /usr/bin && \
    rm /tmp/geckodriver.tar.gz

WORKDIR /opt/sync-zeit-to-tolino

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src .

CMD [ "/bin/bash"]