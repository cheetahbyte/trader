FROM python:alpine
WORKDIR /app
COPY requirements.txt .
COPY scraper.ini config.ini
RUN pip install -r requirements.txt
# this file holds all default stocks
COPY stocks.txt .
COPY *.py .
CMD [ "python", "main.py" ]