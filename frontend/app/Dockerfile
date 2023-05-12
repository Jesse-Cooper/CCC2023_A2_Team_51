# using python3 as basic image. can change to ubuntu if needed
FROM python3 

# # Setting working directory in our container which is to app in this situation 
WORKDIR /app 

ENV FLASK_APP = flasktest.py
ENV FLASK_RUN_HOST = 0.0.0.0

# copy and install Python dependencies 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# adding metadata to image to describe container is listening to 5000 
EXPOSE 5000
# copy current directory to workdir in the image 
COPY . .

CMD ["flask", "run"]

#RUN apt update 
#RUN apt install python3-pip -y
#RUN pip install -r requirements.txt

#WORKDIR /app

#COPY . . 

#CMD python ./app/index.py
#CMD ['python3', '-m', 'flask', 'run', '--host==0.0.0.0']