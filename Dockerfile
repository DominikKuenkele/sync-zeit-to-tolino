FROM python:latest

WORKDIR /opt/sync-zeit-to-tolino

RUN apt-get update && \
    apt-get install -y wget tar

RUN apt-get install -y firefox-esr

RUN wget -q -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz && \
    tar -zxf /tmp/geckodriver.tar.gz -C /usr/bin && \
    rm /tmp/geckodriver.tar.gz

RUN apt-get -y install cron
COPY zeit_cron /etc/cron.d/zeit_cron
RUN chmod 0644 /etc/cron.d/zeit_cron
RUN crontab /etc/cron.d/zeit_cron
RUN touch /var/log/cron.log

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src .

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "cron", "-f", "-L", "2" ]