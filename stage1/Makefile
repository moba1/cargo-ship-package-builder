WORKROOT := ""
CROSS_TOOLCHAIN_IMAGE := ""
IMAGE_TAG := ""
source_image_name := $(firstword $(subst :, ,$(IMAGE_TAG)))-substage1:latest
source_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all
all: build-image

.PHONY: build-source
build-source:
	cd substage1; \
		tar -ch . | \
			docker build \
				--build-arg CROSS_TOOLCHAIN_IMAGE="$(CROSS_TOOLCHAIN_IMAGE)" \
				-t "$(source_image_name)" \
				-; \
	cd ..
	docker run \
		-it --rm \
		-e "WORK_ROOT=$(WORKROOT)" \
		-v "$(source_dir)/dist:/dist-dir" \
		"$(source_image_name)" /bin/bash /app/main.bash /dist-dir

.PHONY: build-image
build-image: build-source
	docker build -t "$(IMAGE_TAG)" -f substage2/Dockerfile .
