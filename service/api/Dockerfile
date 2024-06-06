FROM python:3.9-slim

RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser
WORKDIR /app

COPY api_server.py /app
COPY requirements.txt /app
RUN mkdir uploads
RUN chown -R appuser:appuser /app/uploads/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=api_server.py
CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["flask", "run", "--debug", "--host=0.0.0.0"]