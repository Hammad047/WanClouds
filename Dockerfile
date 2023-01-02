FROM python:3.8.0-buster
WORKDIR /car_app_file
ADD . /car_app_file
EXPOSE 8000
COPY . /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
