# PyChromeless

Python (selenium) Lambda Chromium Automation (naming pending)

PyChromeless allows to automate actions to any webpage from AWS Lambda. The aim of this project is to provide
 the scaffolding for future robot implementations.

## But... how?

All the process is explained [here](https://engineering.21buttons.com/crawling-thousands-of-products-using-aws-lambda-80332e259de1). Technologies used are:
* Python 3.6
* Selenium
* [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)
* [Small chromium binary](https://github.com/adieuadieu/serverless-chrome/releases)

## Requirements

Install docker and dependencies:

* `make fetch-dependencies`
* [Installing Docker](https://docs.docker.com/engine/installation/#get-started)
* [Installing Docker compose](https://docs.docker.com/compose/install/#install-compose)

## Working locally

To make local development easy, you can use the included docker-compose. 
Have a look at the example in `lambda_function.py`: it looks up “21 buttons” on Google and prints the first result. 

Run it with: `make docker-run`

## Building and uploading the distributable package

Everything is summarized into a simple Makefile so use:

* `make build-lambda-package`
* Upload the `build.zip` resulting file to your AWS Lambda function
* Set Lambda environment variables (same values as in docker-compose.yml)
    * `PYTHONPATH=/var/task/src:/var/task/lib`
    * `PATH=/var/task/bin`
* Adjust lambda function parameters to match your necessities, for the given example:
    * Timeout: +10 seconds
    * Memory: + 250MB 

## Shouts to
* [Docker lambda](https://github.com/lambci/docker-lambda)
* [Lambdium](https://github.com/smithclay/lambdium)
* [Serverless Chrome repo](https://github.com/adieuadieu/serverless-chrome) & [medium post](https://medium.com/@marco.luethy/running-headless-chrome-on-aws-lambda-fa82ad33a9eb)
* [Chromeless](https://github.com/graphcool/chromeless)

## Contributors
* Jairo Vadillo ([@jairovadillo](https://github.com/jairovadillo))
* Pere Giro ()
* Ricard Falcó ([@ricardfp](https://github.com/ricardfp))
