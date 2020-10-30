FROM python:3.7-slim AS builder

COPY ./app /app/
RUN mkdir /install
RUN pip install --target=/install -r /app/requirements.txt


FROM gcr.io/distroless/python3-debian10
COPY --from=builder ./app /app/
COPY --from=builder /install /install

ENV PYTHONPATH=/install:/app
WORKDIR /app
EXPOSE 5000
VOLUME ["/trained_models"]
CMD ["./wrapper/main.py"]
