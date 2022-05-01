# py_driver_sim
A python rehosting framework to build and test system code against simulated
hardware. The framework is currently specialized to FreeRTOS.

# Quick Usage:

Python models must be added manually to the folder specified by the `models_dir`
property in `config.json`. These models are concatenated together to generate
the runtime.

To build, use `make all`. To run, use `make test`.

# Dependencies

* Make
* GCC or Clang
* Python >= 3.6
* [requirements.txt](requirements.txt)

# FAQ / Why use this?

* Why not write a virtual device for QEMU and run the driver in that?
  * This is a great alternative. Do this if you can. It has some disadvantages though:
    * You're limited by the subsystem support in QEMU. No SPI sensors for example
    * You're forced to implement the device model in C
    * Device passthrough is experimental and limited

* What are some better alternatives?
  * If you have QEMU available for your system, try [HALucinator](https://github.com/halucinator/halucinator).

* Why this way?
  * You can run this on any architecture you want, as long as there's a python interpreter and a c compiler
  * You can write the hardware model in Python

* This code is cursed
  * Yes it is. Suggestions and improvements welcome

# How it works

### Overview:

The framework rehosts microcontroller code by replacing all hardware calls with
python reimplementations through an interface library dynamically generated at
compile time.

# System Architecture

    ┌──────────────────────────┐
    │                          │
    │  Application under test  │
    │                          │
    └───┬────────────────┬─────┘
        │  ▲             │   ▲
        ▼  │             │   │
    ┌──────┴──────┐      │   │
    │             │      │   │
    │    RTOS     │      │   │
    │             │      │   │
    └──┬──────────┘      │   │
       │   ▲             │   │
       │   │             │   │
       ▼   │             ▼   │
    ┌──────┴─────────────────┴─┐
    │                          │
    │     Interface library    │
    │                          │
    └──────┬──────────────┬────┘
       ▲   │              │  ▲
       │   ├────┐         │  │
       │   │    ▼         ▼  │
       │   │  ┌──────────────┴─┐
       │   │  │                │
       │   │  │ Python backend │
       │   │  │                │
       │   │  └─────┬──────────┘
       │   │        │  ▲
       │   ▼        ▼  │
    ┌──┴───────────────┴───────┐
    │                          │
    │  Host operating system   │
    │                          │
    │                          │
    └──────────────────────────┘

### The Build Process

The following are produced by the build process:
* A shared library containing the OS produced by the makefile in `os/`
* A shared library containing the runtime harness and the interface library. The
  interfaces exposed by the runtime harness are contained in `internal/`.

These libraries are linked against the binary produced by the application code
to create a test application which can be run natively on the target rehosting
architecture.

### The Interface Library

Most of the rehosting magic is made possible by a dynamically generated
interface library that stubs hardware abstraction layer (HAL) functions
and reroutes them to a backend implemented in python. This interface library
is generated at compile time by harness.py with CFFI.

### The Python Backend

The backend simulates the hardware and runtime environment that is not natively
present in the rehosted environment. Calls from the interface library are placed
on a ZeroMQ bus that routes them to an object simulating hardware. The backend
is initialized before main() is called in the application under test by the use
of a constructor function in `internal/runtime.c` and will interpret any CLI
arguments passed to the executable.

# Adding a new device

Add the python code to the folder specified by the `models_dir` property in `config.json`. It will be automatically picked up and concatenated with the rest of the code when the project is rebuilt.

# Make rules

`make all` builds the driver
`make os` builds the underlying OS as a library (currently FreeRTOS)
`make test` runs the driver, which will automatically invoke the model code.


# Relevant publications

Clements, A. A., Gustafson, E., Scharnowski, T., Grosen, P., Fritz, D., Kruegel, C., ... & Payer, M. (2020). {HALucinator}: Firmware Re-hosting Through Abstraction Layer Emulation. In *29th USENIX Security Symposium (USENIX Security 20)* (pp. 1201-1218).

Li, W., Guan, L., Lin, J., Shi, J., & Li, F. (2021). From library portability to para-rehosting: Natively executing microcontroller software on commodity hardware. *arXiv preprint arXiv*:2107.12867.


