# First build step
FROM python:3.7-slim AS builder

# Install python libraries
COPY ./app/requirements.txt /
RUN mkdir /install
RUN pip install --target=/install -r /requirements.txt

# Second build step
FROM gcr.io/distroless/python3-debian10

# Copy app and installed libraries to main image
COPY ./app /app
COPY --from=builder /install /install

# Copy model files
COPY models /trained_models

ENV PYTHONPATH=/install:/app
EXPOSE 5000
WORKDIR /app
CMD ["./wrapper/main.py"]
