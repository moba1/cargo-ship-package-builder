IMAGE_TAG := ""
WORK_ROOT := ""
ARCH := ""
TARGET := ""

.PHONY: all
all:
	tar -ch . | \
		docker build \
			-t "$(IMAGE_TAG)" \
			--build-arg "WORK_ROOT=$(WORKROOT)" \
			--build-arg "ARCH=$(ARCH)" \
			--build-arg "TARGET=$(TARGET)" \
			-
