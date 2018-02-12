FROM python:2.7

EXPOSE 8765

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["plex-webhook-redirector.py"]
