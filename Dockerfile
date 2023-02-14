FROM python:3.8-slim-bullseye


workdir /app
copy . .
RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3", "/app/run.py"]
