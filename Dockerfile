FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /ebaycomics
COPY requirements.txt /ebaycomics/
RUN pip install -r requirements.txt
COPY . /ebaycomics/