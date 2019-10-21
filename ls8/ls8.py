#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

#from ls8.cpu import CPU

cpu = CPU()

cpu.load("../LS8/examples/stack.ls8")
cpu.run()
