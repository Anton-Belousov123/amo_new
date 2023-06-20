FROM python:3.11-buster
WORKDIR /app
COPY . /app
RUN pip install -r misc/requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]
