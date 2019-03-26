# Glimpse Makefile

AWS_USER = "glimpse"
S3_BUCKET = "glimpsefiles"

# Outdated
S3_KEY = "functions/screenshot/build.zip"
FUNCTION_NAME = "GlimpseScan"
# Outdated

RUN_S3_KEY = "run/function/build.zip"
RUN_FUNCTION_NAME = "glimpseRun"
TEST_S3_KEY = "test/function/build.zip"
TEST_FUNCTION_NAME = "glimpseTest"

set:
	source ./access.secret

clean:
	rm -rf build dist
	rm -rf __pycache__

#
# Get browser binaries and drivers. Place in bin/
#
fetch-dependencies:
	mkdir -p bin/

	# Get chromedriver
	curl -SL --silent https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip > chromedriver.zip
	unzip -n chromedriver.zip -d bin/
	rm chromedriver.zip

	# Get Headless-chrome
	curl -SL --silent https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-29/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip -n headless-chromium.zip -d bin/
	rm headless-chromium.zip

	# When Firefox is supported

	# Get geckodriver
	#curl -SL --silent https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz > geckodriver.tar.gz
	#tar -xzvf geckodriver.tar.gz -C bin/
	#rm geckodriver.tar.gz

	# Get firefox
	#curl -SL --silent https://download-installer.cdn.mozilla.net/pub/firefox/releases/65.0.2/linux-x86_64/en-US/firefox-65.0.2.tar.bz2 > firefox.tar.bz2
	#tar -xjvf firefox.tar.bz2 -C bin/ 
	#rm firefox.tar.bz2

#
# Build the docker container for local testing. Only
# needed when updating the Lambda configuration in
# docker-compose.yml or Dockerfile 
#
build: clean fetch-dependencies
	docker-compose build

#
# Scan a URL but don't update if already scanned
#
run:
	docker-compose run --rm lambda src.lambda_function.lambda_handler '{"url": "${URL}"}'

#
# Scan a URL and force an update
#
update:
	docker-compose run --rm lambda src.lambda_function.lambda_handler '{"url": "${URL}", "update": "true"}'

#
# Make a deployment package to be uploaded for Lambda
#
pack: clean fetch-dependencies
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.
	pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr build.zip .
	mkdir -p dist/function
	cp build/build.zip dist/function/build.zip
	rm -rf build

#
# Update the test Lambda function with the current local code
#
deploy-test: pack
	aws s3 cp ./build.zip s3://${S3_BUCKET}/${TEST_S3_KEY} --profile ${AWS_USER}
	aws lambda update-function-code --function-name ${TEST_FUNCTION_NAME} --s3-bucket ${S3_BUCKET} --s3-key ${TEST_S3_KEY} --profile ${AWS_USER} 

#
# Copy the code from the test environment to
# production and update the Lambda function
#
deploy-run:
	aws s3 cp s3://${S3_BUCKET}/${TEST_S3_KEY} s3://${S3_BUCKET}/${RUN_S3_KEY} --profile ${AWS_USER}
	aws lambda update-function-code --function-name ${RUN_FUNCTION_NAME} --s3-bucket ${S3_BUCKET} --s3-key ${RUN_S3_KEY} --profile ${AWS_USER}

