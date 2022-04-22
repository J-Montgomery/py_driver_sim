KERNEL_INC_DIR ?= $(PWD)/headers/freertos
OUT_DIR ?= $(abspath ./output)
CODE_DIR ?= system
OS_DIR ?= os

PY ?= python3
CC ?= gcc
CFLAGS +=-Wall
LFLAGS=-L. -l:$(OUT_DIR)/model.so -l:$(OUT_DIR)/freertos.so

.PHONY: default all clean format test os

PY_FILES := $(wildcard *.py)
DIRS=$(OUT_DIR)

$(OUT_DIR)/%.o: $(CODE_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -I $(PWD)/headers -I $(KERNEL_INC_DIR) -o $@

os:
	$(MAKE) -C $(OS_DIR) CC=$(CC) BUILD_DIR=$(OUT_DIR) BIN=freertos.so

%.py:
	black $@

format: $(PY_FILES)

$(OUT_DIR)/model.so:
	rm -rf $@
	$(PY) harness.py $(OUT_DIR) model.so

$(OUT_DIR)/driver: $(OUT_DIR)/driver.o $(OUT_DIR)/model.so
	$(CC) $< $(LFLAGS) -o $@

default: $(OUT_DIR)/driver

test: default
	LD_LIBRARY_PATH=. ./$(OUT_DIR)/driver

all: default

clean:
	rm -rf $(OUT_DIR)

$(shell mkdir -p $(DIRS))
