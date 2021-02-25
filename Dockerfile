FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir -p code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000