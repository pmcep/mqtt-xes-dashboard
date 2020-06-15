FROM python:3.8

COPY client.py client.py
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "./client.py"]
