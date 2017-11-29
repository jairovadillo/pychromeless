FROM lambci/lambda:build-python3.6
MAINTAINER tech@21buttons.com

ENV PATH=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/var/task/bin:$PATH

COPY requirements.txt /var/task

RUN pip install -r /var/task/requirements.txt
