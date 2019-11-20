#Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
# ENTRYPOINT ["python3"]
CMD ["nohup","python3", "-u","server.py","&"]
