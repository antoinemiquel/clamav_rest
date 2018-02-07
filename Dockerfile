FROM python:2

#https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
#https://github.com/miguelgrinberg/REST-tutorial/blob/master/setup.sh

RUN apt-get update && \
    apt-get -y install apt-utils clamav clamav-daemon

RUN mkdir /var/run/clamav && \
    chown clamav:clamav /var/run/clamav && \
    chmod 750 /var/run/clamav

RUN /usr/bin/freshclam

ADD bootstrap.sh /

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip `[ "$HTTP_PROXY" != "" ] && echo "--proxy $HTTP_PROXY"` install --no-cache-dir -r requirements.txt

COPY *.py ./

RUN mkdir download

CMD ["/bootstrap.sh"]
