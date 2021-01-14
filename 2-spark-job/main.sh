#!/bin/sh


# train model
python src/training/train.py --output_dir ./models

# Create a docker volume
docker volume create --driver local \
    --opt type=none \
    --opt device=<path/to/>/jobs \
    --opt o=bind shared-workspace

# spin up spark cluster and mount input data and model to master and worker
docker-compose -f docker-compose.yml up --build
