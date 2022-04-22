KERNEL_INC_DIR ?= $(PWD)/headers/freertos
OUT_DIR ?= $(abspath ./output)
CODE_DIR ?= ./system
OS_DIR ?= os

PY ?= python3
CC ?= gcc

INCLUDE_DIRS          := -I.
INCLUDE_DIRS          += -I./headers
INCLUDE_DIRS          += -I./headers/freertos
INCLUDE_DIRS          += -I./internal

CFLAGS   += -ggdb3 -fPIC -Wall
CPPFLAGS += $(INCLUDE_DIRS) -DBUILD_DIR=\"$(BUILD_DIR_ABS)\"

LDFLAGS  += -ggdb3 -pthread -L $(OUT_DIR) -l freertos -l harness
# LDFLAGS  += -Xlinker --verbose

.PHONY: default all clean format test os

PY_FILES := $(wildcard *.py)
DIRS=$(OUT_DIR)

SOURCE_FILES := $(wildcard $(CODE_DIR)/*.c)
OBJ_FILES = $(SOURCE_FILES:$(CODE_DIR)/%.c=$(OUT_DIR)/%.o)
DEP_FILE = $(OBJ_FILES:%.o=%.d)

$(OUT_DIR)/%.o : $(CODE_DIR)/%.c Makefile
	-mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -c $< -o $@

$(OUT_DIR)/driver : $(OBJ_FILES)
	-mkdir -p ${@D}
	$(CC) $^ ${LDFLAGS} -o $@

os:
	$(MAKE) -C $(OS_DIR) CC=$(CC) BUILD_DIR=$(OUT_DIR) BIN=libfreertos.so

%.py:
	black $@

format: $(PY_FILES)

harness:
	-rm -rf $(OUT_DIR)/libharness.so
	$(PY) harness.py $(OUT_DIR) libharness.so

default: os harness $(OUT_DIR)/driver Makefile

test:
	LD_LIBRARY_PATH=$(OUT_DIR) $(OUT_DIR)/driver

all: default

clean:
	rm -rf $(OUT_DIR)

$(shell mkdir -p $(DIRS))
