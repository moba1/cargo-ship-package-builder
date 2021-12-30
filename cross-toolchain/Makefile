IMAGE_TAG := ""
WORK_ROOT := ""

.PHONY: all
all:
	tar -ch . | \
		docker build \
			-t "$(IMAGE_TAG)" \
			--build-arg "WORK_ROOT=$(WORKROOT)" \
			-
