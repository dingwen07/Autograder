IMAGE_NAME = extrawdw/autograder
PLATFORMS = linux/amd64,linux/arm64

.PHONY: all build push

all: build push

build:
	docker buildx build --platform $(PLATFORMS) -t $(IMAGE_NAME) .

push: build
	docker push $(IMAGE_NAME)
