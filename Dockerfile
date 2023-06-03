# syntax=docker/dockerfile:1

FROM python:3.12-rc-alpine3.18

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .

CMD ["python3", "tracking_devman_api.py"]