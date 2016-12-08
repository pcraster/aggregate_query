#!/usr/bin/env bash
set -e


docker build -t test/aggregate_query .
docker run -p3031:3031 test/aggregate_query
