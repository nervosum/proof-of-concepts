FROM python:3.7-stretch AS builder

COPY ./app /app/
RUN pip install -r /app/requirements.txt


FROM gcr.io/distroless/python3-debian10
COPY --from=builder ./app /app/
COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages

ENV PYTHONPATH=/usr/local/lib/python3.7/site-packages:/app
WORKDIR /app
EXPOSE 5000
VOLUME ["/trained_models"]
CMD ["./wrapper/main.py"]
