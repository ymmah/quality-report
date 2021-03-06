FROM python:3.6-alpine

MAINTAINER Frank Niessink <frank.niessink@ictu.nl>

RUN addgroup jenkins && adduser -s /bin/bash -D -G jenkins jenkins

RUN apk --update add gcc musl-dev libxml2-dev libxslt-dev bash git subversion openssh-client \
    && pip install git+https://github.com/ICTU/wekan-python-api-client.git#egg=wekanapi\&subdirectory=src \
    && pip install quality_report \
    && apk del gcc musl-dev  \
    && rm -rf /var/cache/apk/* /tmp/

VOLUME /home/jenkins/.ssh

USER jenkins

ENTRYPOINT ["quality_report.py"]


