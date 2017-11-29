# PyChromeless

Python (selenium) Lambda Chromium Automation (naming pending)

PyChromeless allows to automate actions to any webpage from AWS Lambda. The aim of this project is to provide
 the scaffolding for future robot implementations.

## But... how?

* Python 3.6
* Selenium
* [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)
* [Small chromium binary](https://github.com/adieuadieu/serverless-chrome/releases)

## Requirements

Before working local or uploading to AWS Lambda binaries must be retrieved and docker should be installed:

* `make fetch-dependencies`
* [Installing Docker](https://docs.docker.com/engine/installation/#get-started)


## Working locally

In order to make local development easy a docker-compose is provided and also a very simple example that searches 
 for "21 buttons" on Google and prints the first result (`lambda_function.py`). In order to run the example simply execute:

`docker-compose up`

Also, if you want to run a (python) shell and try stuff by yourself use:

`docker-compose run --rm lambda python` or `docker-compose run --rm lambda bash`

## Building and uploading the distributable package

Everything is summarized into a simple Makefile so use:

* `make lambda-build`
* Compress the resulting build/ directory contents into a .zip file
* Upload this file to your AWS Lambda
* Set `PATH=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/var/task/bin` environment var on your AWS Lambda

_(Terraform file to create the AWS Lambda is provided) # noqa_

## Shouts to
* [Docker lambda](https://github.com/lambci/docker-lambda)
* [Lambdium](https://github.com/smithclay/lambdium)
* [Serverless Chrome repo](https://github.com/adieuadieu/serverless-chrome) & [medium post](https://medium.com/@marco.luethy/running-headless-chrome-on-aws-lambda-fa82ad33a9eb)
* [Chromeless](https://github.com/graphcool/chromeless)

## Contributors
* Jairo Vadillo ([@jairovadillo](https://github.com/jairovadillo))
