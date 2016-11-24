#!/usr/bin/env bash
set -e
docker build -t test/aggregate_query .
docker run -p9090:9090 test/aggregate_query
