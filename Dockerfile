FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV MONGODB_URL=mongodb://mongodb:27017/db
ENV FLASK_DEBUG=1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 6000
COPY . .
CMD ["flask", "run"]
