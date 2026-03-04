# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

RESET_STATE = 0
READ_STATE = 1
WRITE_STATE = 2
COMPUTE_STATE = 3 
IDLE_STATE = 5
@cocotb.test()
async def write_test_1(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1


    dut._log.info("Test project behavior")
    input_values = [1,2,3,4,5,6,7,8]
    dut.uio_in.value = WRITE_STATE
    await ClockCycles(dut.clk, 1)
    # setting next state as early as possible
    dut.uio_in.value = READ_STATE
    for input_value in input_values:
        dut.ui_in.value = input_value
        await ClockCycles(dut.clk, 1)
    
    # wait once cycles for mode switch
    await ClockCycles(dut.clk, 2) 
    for input_value in input_values:
        assert dut.uo_out.value == input_value
        await ClockCycles(dut.clk, 1)

@cocotb.test()
async def write_test_2(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1


    dut._log.info("Test project behavior")
    input_values = [34,115,141,94,103,222,42,58]
    dut.uio_in.value = WRITE_STATE
    await ClockCycles(dut.clk, 1)
    # setting next state as early as possible
    dut.uio_in.value = READ_STATE
    for input_value in input_values:
        dut.ui_in.value = input_value
        await ClockCycles(dut.clk, 1)
    
    # wait once cycles for mode switch
    await ClockCycles(dut.clk, 2) 
    for input_value in input_values:
        assert dut.uo_out.value == input_value
        await ClockCycles(dut.clk, 1)

@cocotb.test()
async def compute_test_1(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1


    dut._log.info("Test project behavior")
    input_weights = [1,2,3,4,5,6,7,8]
    dut.uio_in.value = WRITE_STATE
    await ClockCycles(dut.clk, 1)
    # setting next state as early as possible
    dut.uio_in.value = COMPUTE_STATE
    for input_value in input_weights:
        dut.ui_in.value = input_value
        await ClockCycles(dut.clk, 1)
    
    # wait once cycles for mode switch
    # await ClockCycles(dut.clk, 1) 
    input_activations = [1,1,1,1,1,1,1,1]
    ptr = 0 
    sum = 0
    while ptr < len(input_activations)+2:
        if ptr < len(input_activations):
            dut.ui_in.value = input_activations[ptr]
        if ptr > 1:
            sum += input_activations[ptr -2]*input_weights[ptr -2]
            assert sum == dut.uo_out.value
        await ClockCycles(dut.clk, 1)
        ptr +=1 

@cocotb.test()
async def compute_test_2(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1


    dut._log.info("Test project behavior")
    input_weights = [1,2,3,4,5,6,7,8]
    dut.uio_in.value = WRITE_STATE
    await ClockCycles(dut.clk, 1)
    # setting next state as early as possible
    dut.uio_in.value = COMPUTE_STATE
    for input_value in input_weights:
        dut.ui_in.value = input_value
        await ClockCycles(dut.clk, 1)
    
    # wait once cycles for mode switch
    # await ClockCycles(dut.clk, 1) 
    input_activations = [0,1,0,1,0,1,1,1]
    ptr = 0 
    sum = 0
    while ptr < len(input_activations)+2:
        if ptr < len(input_activations):
            dut.ui_in.value = input_activations[ptr]
        if ptr > 1:
            sum += input_activations[ptr -2]*input_weights[ptr -2]
            dut._log.info(f"Sum should be: {sum}")
            assert sum == dut.uo_out.value
        await ClockCycles(dut.clk, 1)
        ptr +=1 

@cocotb.test()
async def compute_test_3(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1


    dut._log.info("Test project behavior")
    input_weights = [12,14,30,2,8,3,42,58]
    dut.uio_in.value = WRITE_STATE
    await ClockCycles(dut.clk, 1)
    # setting next state as early as possible
    dut.uio_in.value = COMPUTE_STATE
    for input_value in input_weights:
        dut.ui_in.value = input_value
        await ClockCycles(dut.clk, 1)
    
    # wait once cycles for mode switch
    # await ClockCycles(dut.clk, 1) 
    input_activations = [0,1,0,1,0,1,1,1]
    ptr = 0 
    sum = 0
    while ptr < len(input_activations)+2:
        if ptr < len(input_activations):
            dut.ui_in.value = input_activations[ptr]
        if ptr > 1:
            sum += input_activations[ptr -2]*input_weights[ptr -2]
            dut._log.info(f"Sum should be: {sum}")
            assert sum == dut.uo_out.value
        await ClockCycles(dut.clk, 1)
        ptr +=1 

@cocotb.test()
async def write_test_3(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1


    dut._log.info("Test project behavior")
    input_values = [19,115,141,94,10,222,42,55]
    dut.uio_in.value = WRITE_STATE
    await ClockCycles(dut.clk, 1)
    # setting next state as early as possible
    dut.uio_in.value = READ_STATE
    for input_value in input_values:
        dut.ui_in.value = input_value
        await ClockCycles(dut.clk, 1)
    
    # wait once cycles for mode switch
    await ClockCycles(dut.clk, 2) 
    for input_value in input_values:
        assert dut.uo_out.value == input_value
        await ClockCycles(dut.clk, 1)