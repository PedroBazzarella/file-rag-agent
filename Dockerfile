FROM python:3.14.3-slim

WORKDIR /usr/src/app

COPY requirements-docker.txt ./
RUN pip install --no-cache-dir -r requirements-docker.txt
RUN pip install --no-cache-dir --force-reinstall opencv-python-headless

COPY . .

CMD [ "python", "./main.py" ]