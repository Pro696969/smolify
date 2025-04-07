FROM python:3.12.9-alpine3.20 as dev

COPY ./requirements.txt /work/requirements.txt

WORKDIR /work

RUN pip install -r requirements.txt

COPY . /work

ENTRYPOINT ["python3"]

CMD ["-u", "main.py"]