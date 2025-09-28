IMAGE_NAME = chfi-network-vsftpd
CONTAINER_NAME = $(IMAGE_NAME)

build:
	docker build -f Dockerfile -t $(IMAGE_NAME) .

run: build
	docker run -d -p 2021:21 -p 2020:20 -p 30000-30009:30000-30009 --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

clean: stop
	docker rm $(CONTAINER_NAME)

.PHONY: build run stop clean
