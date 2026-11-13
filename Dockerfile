FROM python:3.15.0

WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code

CMD ["python", "server.py"]