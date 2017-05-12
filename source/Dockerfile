FROM posbank.geoneric.eu:5000/nca/nc_base:latest

MAINTAINER Kor de Jong <k.dejong@geoneric.eu>

COPY cmd.sh server.py /
COPY nc_gdx /nc_gdx
COPY test /test
COPY gdx-20170213 /usr/local/bin/gdx

CMD ["/cmd.sh"]
