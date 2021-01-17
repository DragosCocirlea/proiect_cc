FROM python:3.6

WORKDIR /auth

COPY requirements.txt /auth
COPY auth.py /auth
COPY resources.py /auth
COPY models.py /auth
COPY wait-for-it.sh /auth
RUN chmod +x wait-for-it.sh

RUN pip install -r requirements.txt

CMD ./wait-for-it.sh dbauth:3306 && python auth.py
