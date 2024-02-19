FROM umihico/aws-lambda-selenium-python:3.12.0-selenium4.17.2-chrome121.0.6167.184

COPY requirements-scraper.txt /var/task/requirements.txt
RUN pip install -r /var/task/requirements.txt
COPY scraper.py /var/task/main.py
