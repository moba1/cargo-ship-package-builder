WORKROOT := ""
CROSS_TOOLCHAIN_IMAGE := ""
IMAGE_TAG := ""
ARCH := ""
TARGET := ""
source_image_name := $(firstword $(subst :, ,$(IMAGE_TAG)))-substage1:latest
source_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
dist_dir := "$(source_dir)/dist"
process_number := $(shell nproc)

.PHONY: all
all: build-image

.PHONY: build-source
build-source:
	cd substage1; \
		tar -ch . | \
			docker build \
				--build-arg CROSS_TOOLCHAIN_IMAGE="$(CROSS_TOOLCHAIN_IMAGE)" \
				-t "$(source_image_name)" \
				-
	docker run \
		-it --rm \
		-e "WORK_ROOT=$(WORKROOT)" \
		-e "ARCH=$(ARCH)" \
		-v "$(dist_dir):/dist-dir" \
		"$(source_image_name)" /bin/bash /app/main.bash /dist-dir

.PHONY: build-image
build-image: build-source
	env DIST_DIR="$(source_dir)/source" bash substage2/src/fetch-source.bash
	rm -f substage2/dist; ln -sf "$(dist_dir)" substage2/dist
	rm -f substage2/source; ln -sf "$(source_dir)/source" substage2/source
	cd substage2; \
		tar -ch . | \
			docker build \
				--build-arg DIST_DIR=/var/tmp \
				--build-arg "TARGET=$(TARGET)" \
				--build-arg "PROCESS_NUMBER=$(process_number)" \
				-t "$(IMAGE_TAG)" \
				-

.PHONY: clean
clean:
	rm -Rf "$(source_dir)/dist" "$(source_dir)/source"

