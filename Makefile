KERNEL_INC_DIR ?= /usr/src/linux-oem-5.10-headers-5.10.0-1057/include/
OUT_DIR ?= output
CODE_DIR ?= system

PY ?= python3
CC ?= gcc
CFLAGS +=-Wall
LFLAGS=-L. -l:$(OUT_DIR)/model.so

.PHONY: default all clean format test

PY_FILES := $(wildcard *.py)
DIRS=$(OUT_DIR)

$(OUT_DIR)/%.o: $(CODE_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -I $(PWD)/headers -I $(KERNEL_INC_DIR) -o $@

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
