CROSS_TOOLCHAIN_IMAGE := cross-toolchain:latest
STAGE1_IMAGE := stage1:latest
STAGE2_IMAGE := stage2:latest
WORKROOT := /work
ARCH := x86_64
TARGET := $(ARCH)-lfs-linux-gnu

.PHONY: all
all:
	make -C cross-toolchain \
		WORKROOT="$(WORKROOT)" \
		IMAGE_TAG="$(CROSS_TOOLCHAIN_IMAGE)" \
		TARGET="$(TARGET)" \
		ARCH="$(ARCH)"
	make -C stage1 \
		IMAGE_TAG="$(STAGE1_IMAGE)" \
		WORKROOT="$(WORKROOT)" \
		CROSS_TOOLCHAIN_IMAGE="$(CROSS_TOOLCHAIN_IMAGE)" \
		TARGET="$(TARGET)" \
		ARCH="$(ARCH)"

.PHONY: clean
clean:
	make -C stage1 clean

