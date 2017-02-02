#!/usr/bin/env bash
set -e


docker build -t test/emis_aggregate_query .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/emis_aggregate_query:/emis_aggregate_query test/emis_aggregate_query
