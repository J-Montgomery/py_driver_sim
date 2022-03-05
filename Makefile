CC=gcc
CFLAGS=-Wall
LFLAGS=-L. -l:model-0.1.so
KERNEL_INC_DIR=/usr/src/linux-oem-5.10-headers-5.10.0-1057/include/
PY=python3

.PHONY: default all clean format

PY_FILES := $(wildcard *.py)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -I $(PWD)/headers -I $(KERNEL_INC_DIR) -o $@

%.py:
	black $@

format: $(PY_FILES)

model.so:
	$(PY) harness.py

driver: driver.o model.so
	$(CC) driver.o $(LFLAGS) -o $@

default: driver

test:
	LD_LIBRARY_PATH=. ./driver

all: default

clean:
	rm -f *.o
	rm -f *.so
	rm -f driver
