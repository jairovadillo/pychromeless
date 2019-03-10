# Glimpse Makefile

AWS_USER = "glimpse"
S3_BUCKET = "glimpsefiles"
S3_KEY = "functions/screenshot/build.zip"
FUNCTION_NAME = "glimpseScreenshot"

clean:
	rm -rf build build.zip
	rm -rf __pycache__

fetch-dependencies:
	mkdir -p bin/

	# Get chromedriver
	curl -SL --silent https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip > chromedriver.zip
	unzip -n chromedriver.zip -d bin/

	# Get Headless-chrome
	curl -SL --silent https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-29/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip -n headless-chromium.zip -d bin/

	# Get geckodriver
	curl -SL --silent https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz > geckodriver.tar.gz
	tar -xzvf geckodriver.tar.gz -C bin/

	# Get firefox
	curl -SL --silent https://download-installer.cdn.mozilla.net/pub/firefox/releases/65.0.2/linux-x86_64/en-US/firefox-65.0.2.tar.bz2 > firefox.tar.bz2
	tar -xjvf firefox.tar.bz2 -C bin/ 

	# Clean
	rm headless-chromium.zip chromedriver.zip geckodriver.tar.gz

build:
	docker-compose build

run:
	docker-compose run --rm lambda src.lambda_function.lambda_handler '{"url": "${URL}"}'

test: build
	docker-compose run --rm lambda src.lambda_function.lambda_handler '{"url": "${URL}"}'

pack: clean fetch-dependencies
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.
	pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build

deploy: pack
	aws s3 cp ./build.zip s3://${S3_BUCKET}/${S3_KEY} --profile ${AWS_USER}
	aws lambda update-function-code --function-name ${FUNCTION_NAME} --s3-bucket ${S3_BUCKET} --s3-key ${S3_KEY} --profile ${AWS_USER} 
