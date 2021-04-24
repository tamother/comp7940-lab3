FROM python
COPY chatbot.py /
COPY requirements.txt /
EXPOSE 8080
RUN pip install pip update
RUN pip install -r requirements.txt
CMD ["python","chatbot.py"]