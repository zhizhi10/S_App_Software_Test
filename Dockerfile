FROM python:3.8-slim-bullseye



# Install Stardist and tensorflow and its dependencies
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# --------------------------------------------------------------------------------------------
# Install scripts
COPY descriptor.json /app/descriptor.json
COPY run.py /app/run.py

ENTRYPOINT ["python3", "/app/run.py"]
