CROSS_TOOLCHAIN_IMAGE := cross-toolchain:latest
STAGE1_IMAGE := stage1:latest
WORKROOT=/work

.PHONY: all
all:
	make -C cross-toolchain \
		WORKROOT="$(WORKROOT)" \
		IMAGE_TAG="$(CROSS_TOOLCHAIN_IMAGE)"
	make -C stage1 \
		IMAGE_TAG="$(STAGE1_IMAGE)" \
		WORKROOT="$(WORKROOT)" \
		CROSS_TOOLCHAIN_IMAGE="$(CROSS_TOOLCHAIN_IMAGE)"
