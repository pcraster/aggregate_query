#!/usr/bin/env bash
set -e
docker build -t test/aggregate_query .
docker run --env ENV=TEST -p5000:5000 test/aggregate_query
