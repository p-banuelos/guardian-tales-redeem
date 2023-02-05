FROM ubuntu:latest

RUN apt-get update && apt-get install --no-install-recommends -y python3.11 python3.11-venv python3.11-dev python3-pip python3-wheel build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/nobody
WORKDIR $HOME    

RUN python3.11 -m venv $HOME/venv
ENV PATH="$HOME/venv/bin:$PATH"

COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R nobody:nogroup $HOME
RUN chmod +x entrypoint.sh

ENV PYTHONUNBUFFERED=1

USER nobody

ENTRYPOINT [ "/home/nobody/entrypoint.sh" ]