FROM python:3.8

# Set the working directory to /app
WORKDIR /app
COPY * /app/
RUN pip install -r requirements.txt
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn --host=0.0.0.0 main:app"]
