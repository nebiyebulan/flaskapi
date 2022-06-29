FROM python:3.7

COPY .  /SmartGateX
WORKDIR /SmartGateX

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 User.py
