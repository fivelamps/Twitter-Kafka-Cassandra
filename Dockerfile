FROM landoop/fast-data-dev:2.6

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-confluent-kafka

COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt

COPY variables.env /usr/local/share/landoop/sample-data/
