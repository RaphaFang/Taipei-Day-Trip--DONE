FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn[standard] mysql-connector-python

ENV SQL_USER=root
ENV SQL_PASSWORD=000000
ENV SQL_HOST=db  
ENV SQL_DATABASE=website

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
