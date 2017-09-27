FROM pcraster/emis_base:1.0.0

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

COPY cmd.sh server.py server_flask.py uwsgi.ini /
COPY emis_aggregate_query /emis_aggregate_query
COPY test /test

CMD ["/cmd.sh"]
