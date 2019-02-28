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

	# Get browsermob-proxy
	#curl -SL https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip > browsermob.zip
	#unzip browsermob.zip -d bin/

	# Get Java JRE
	#curl -SL https://sdlc-esd.oracle.com/ESD6/JSCDL/jdk/8u201-b09/42970487e3af4f5aa5bca3f542482c60/jre-8u201-linux-x64.tar.gz?GroupName=JSC&FilePath=/ESD6/JSCDL/jdk/8u201-b09/42970487e3af4f5aa5bca3f542482c60/jre-8u201-linux-x64.tar.gz&BHost=javadl.sun.com&File=jre-8u201-linux-x64.tar.gz&AuthParam=1551234378_7445fc2a8d97b7b62b01777726d168cd&ext=.gz > jre.tar.gz


	# Clean
	rm headless-chromium.zip chromedriver.zip

docker-build:
	docker-compose build

docker-run: docker-build
	docker-compose run lambda src.lambda_function.lambda_handler

test: docker-build
	docker-compose run lambda src.lambda_function.lambda_handler '{"url": "$(URL)"}'

build-lambda: clean fetch-dependencies
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.
	pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build
