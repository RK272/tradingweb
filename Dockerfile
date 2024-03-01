FROM python:3.8-slim-buster
WORKDIR /service   # set working dir as service in container it was isolated system
COPY requirements.txt .
COPY . ./ # copy erey thing from local to container
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]