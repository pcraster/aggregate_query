#!/usr/bin/env bash
set -e
docker build -t test/aggregate_query .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/aggregate_query:/aggregate_query test/aggregate_query
