FROM python:3.8-slim AS base

ENV GOOGLE_CHROME_VERSION=google-chrome-stable_current_amd64.deb
ENV DISPLAY=:99
ENV APP_DIR /app

RUN apt-get -y update \
    && apt-get install -y libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev

#    && apt-get -y install wget gnupg --no-install-recommends \
#    && wget https://dl.google.com/linux/direct/$GOOGLE_CHROME_VERSION \
#    && apt install -y ./$GOOGLE_CHROME_VERSION \
#    && rm $GOOGLE_CHROME_VERSION \
#    && apt-get -y remove gnupg \
#    && apt-get -y autoremove

RUN mkdir -p /app
WORKDIR $APP_DIR

RUN pip install chromedriver_py==86.0.4240.22
#RUN pip install chromedriver_py==$(google-chrome --product-version)

FROM base AS lambda

COPY . $APP_DIR
RUN pip install -r requirements.txt

ENV PATH=$PATH:$APP_DIR/bin:$APP_DIR/lib

CMD ["python","lambda_function.py"]
