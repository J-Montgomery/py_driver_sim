# py_driver_sim
A python framework to build and test kernel drivers against simulated hardware

# Quick Usage:
Driver must currently be named "driver.c"

Python models must be added manually to harness.py, which concatenates them to generate the c model. 

`make all` builds the driver
`make test` runs the driver, which will automatically invoke the model code.
