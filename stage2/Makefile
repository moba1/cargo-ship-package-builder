STAGE1_IMAGE := ""
IMAGE_TAG := ""
source_dir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all
all:
	env DIST_DIR="$(source_dir)/source" bash fetch-source.bash
	tar -ch . | \
		docker build \
		-t "$(IMAGE_TAG)" \
		--build-arg STAGE1_IMAGE="$(STAGE1_IMAGE)" \
		--build-arg DIST_DIR=/var/tmp \
		--build-arg "PROCESS_NUMBER=$(shell nproc)" \
		-
