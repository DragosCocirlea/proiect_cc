FROM python:3.6

WORKDIR /server

COPY requirements.txt /server
COPY templates/* /server/templates/
COPY server.py /server
COPY resources.py /server
COPY models.py /server
COPY init_functions.py /server
COPY wait-for-it.sh /server
RUN chmod +x wait-for-it.sh

RUN pip install -r requirements.txt

CMD ./wait-for-it.sh dbserver:3306 && python server.py
