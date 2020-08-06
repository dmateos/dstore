FROM python:3.8

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY src/* /app/

EXPOSE 8080
CMD ["/usr/local/bin/uvicorn", "--host=0.0.0.0", "--port=8080", "main:app"]
