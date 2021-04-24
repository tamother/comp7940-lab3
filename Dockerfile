FROM python
COPY chatbot.py /
COPY requirements.txt /
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=1648003022:AAGMCAwA649B465cPzPKHi44ozpP8XH0uzI
ENV HOST=redis-10366.c228.us-central1-1.gce.cloud.redislabs.com
ENV PASSWORD=ICZB0tTsfp1fr6a51wp4MfW0gC8E1wLT
ENV REDISPORT=10366
CMD ["python","chatbot.py"]