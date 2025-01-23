TEST_IMAGE=find_flakes_test
APP_IMAGE=find_flakes

setup:
	export PATH=${PATH}:${PWD}

build-image:
	docker build . --no-cache -t ${APP_IMAGE}:latest

test:
	docker build . --no-cache -t find_flakes_test:latest -f ./Dockerfile.test
	 - docker run --name find_flakes_test ${TEST_IMAGE}:latest
	docker rm find_flakes_test > /dev/null
