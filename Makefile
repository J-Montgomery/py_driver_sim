KERNEL_INC_DIR ?= $(PWD)/headers/freertos
OUT_DIR ?= $(abspath ./output)
CODE_DIR ?= ./system
OS_DIR ?= os

PY ?= python3
CC ?= gcc

INCLUDE_DIRS          := -I.
INCLUDE_DIRS          += -I./headers
INCLUDE_DIRS          += -I./headers/freertos

CFLAGS   += -ggdb3 -fPIC -Wall
LDFLAGS  += -ggdb3 -pthread -L. -L $(OUT_DIR) -l freertos
CPPFLAGS += $(INCLUDE_DIRS) -DBUILD_DIR=\"$(BUILD_DIR_ABS)\"
CFLAGS +=-Wall
LFLAGS=-L. -l:$(OUT_DIR)/freertos.so

.PHONY: default all clean format test os

PY_FILES := $(wildcard *.py)
DIRS=$(OUT_DIR)

SOURCE_FILES := $(wildcard $(CODE_DIR)/*.c)
OBJ_FILES = $(SOURCE_FILES:$(CODE_DIR)/%.c=$(OUT_DIR)/%.o)
DEP_FILE = $(OBJ_FILES:%.o=%.d)

#$(OUT_DIR)/%.o: $(CODE_DIR)/%.c
#	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

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

$(OUT_DIR)/model.so:
	rm -rf $@
	$(PY) harness.py $(OUT_DIR) model.so

#$(OUT_DIR)/driver: $(OUT_DIR)/driver.o
#	$(CC) $< $(LFLAGS) -o $@

default: os $(OUT_DIR)/driver Makefile

test: default
	LD_LIBRARY_PATH=$(OUT_DIR) $(OUT_DIR)/driver

all: default

clean:
	rm -rf $(OUT_DIR)

$(shell mkdir -p $(DIRS))
