
FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install rar zip python3 python3-dev megatools git curl python3-pip ffmpeg -y
RUN pip3 install -U pip
RUN cd /
RUN git clone https://github.com/muhammedfurkan/TelethonUserBot.git
RUN cd TelethonUserBot
WORKDIR /TelethonUserBot
RUN pip3 install -U -r requirements.txt
CMD python3 -m userbot