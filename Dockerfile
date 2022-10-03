# syntax=docker/dockerfile:1
FROM python:alpine
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "tracking_devman_api.py"]