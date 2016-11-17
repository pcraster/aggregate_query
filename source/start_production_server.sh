#!/usr/bin/env bash
set -e
docker build -t test/aggregate_query .
docker run -p5000:9090 test/aggregate_query
