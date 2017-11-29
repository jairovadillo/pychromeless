clean:
	rm -rf build build.zip __pycache__

fetch-dependencies:
	mkdir -p bin/

	# Get chromedriver
	curl -SL https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip > chromedriver.zip
	unzip chromedriver.zip -d bin/

	# Get Headless-chrome
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-29/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip headless-chromium.zip -d bin/

	# Clean
	rm headless-chromium.zip chromedriver.zip

lambda-build: clean fetch-dependencies
	mkdir build
	cp lambda_function.py build/.
	cp -r bin build/.
	cp -r lib build/.
	pip install -r requirements.txt -t build/.
	cd build/
