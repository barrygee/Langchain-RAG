FROM python:3

WORKDIR /usr/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY app .

CMD [ "sh", "-c", "python ./app.py && tail -f /dev/null" ]
