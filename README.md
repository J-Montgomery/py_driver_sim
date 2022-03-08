# py_driver_sim
A python framework to build and test kernel drivers against simulated hardware

# Quick Usage:
Driver must currently be named "driver.c"

Python models must be added manually to the folder specified by the `models_dir`
property in `config.json`. These models are concatenated together to generate
the runtime.

# FAQ / Why use this?

* Why not write a virtual device for QEMU and run the driver in that?
  * This is a great alternative. Do this if you can. It has some disadvantages though:
    * You're limited by the subsystem support in QEMU. No SPI sensors for example
    * You're forced to implement the device model in C
    * Device passthrough is experimental and limited

* Why this way?
  * You can run this on any architecture you want, as long as there's a python interpreter and a c compiler
  * You can write the hardware model in Python

* This code is cursed
  * Yes it is. Suggestions and improvements welcome

# Adding a new device

Add the python code to the folder specified by the `models_dir` property in `config.json`. It will be automatically
picked up and concatenated with the rest of the code when the project is rebuilt.
# Make rules

`make all` builds the driver
`make test` runs the driver, which will automatically invoke the model code.

