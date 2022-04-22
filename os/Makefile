CC                    := gcc
BIN                   := posix_demo

BUILD_DIR             := ./build
BUILD_DIR_ABS         := $(abspath $(BUILD_DIR))

KERNEL_DIR            := $(PWD)

INCLUDE_DIRS          := -I.
INCLUDE_DIRS          += -I${KERNEL_DIR}/../headers/freertos

SOURCE_FILES          := $(wildcard *.c)
SOURCE_FILES          += $(wildcard ${KERNEL_DIR}/port/*.c)

CFLAGS                :=    -ggdb3
LDFLAGS               :=    -ggdb3 -pthread

  CFLAGS              +=   -O3
  LDFLAGS             +=   -O3

OBJ_FILES = $(SOURCE_FILES:%.c=$(BUILD_DIR)/%.o)

DEP_FILE = $(OBJ_FILES:%.o=%.d)

${BIN} : $(BUILD_DIR)/$(BIN)

${BUILD_DIR}/${BIN} : ${OBJ_FILES}
	-mkdir -p ${@D}
	$(CC) $^ ${LDFLAGS} -o $@

${BUILD_DIR}/%.o : %.c Makefile
	-mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -c $< -o $@

.PHONY: clean

clean:
	-rm -rf $(BUILD_DIR)
