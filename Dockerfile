FROM python:3.8-slim-buster
WORKDIR /python-docker
COPY requirements.txt requirements.txt
ENV FLASK_APP=web_calculator.py
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000