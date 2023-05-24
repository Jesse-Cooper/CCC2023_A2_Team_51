# using python3 as basic image. can change to ubuntu if needed
FROM python:3.8-slim-buster

WORKDIR /app 

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]