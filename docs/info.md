## How it works

The goal of this tiny tapeout design was to mimic binary SRAM based compute in memory circuits using registers. As a result this chip consists of an 8x8 array of registers. This stores 8 8-bit integers. Since this is a meant to mimic binary based CIM circuits we only support input activations of 0 and 1. This means that the final result that is returned is every weight multiplied by an activation that is either one or zero summed together. Ideally this would be expanded to support ternary activation (-1,0,1). There is a good bit a multiplexing that is required to make this design work using entirely digital components. The output of each of the registers is multiplexed and I use a ring counter to select which one I am reading from. Since Verilog is meant for entirely digital designs, I also did my accumulation one input at a time.

## How to test

In order to test this project I mainly performed two types of tests. The first test was writing and reading weights into the 8x8 activation registers. This was done with multiple sets of numbers along with verifying that resets actually worked. The second type of test was actually performing computation and making sure that it matched expectations. I mostly did my testing in cocotb due to how easy it is to use and how it enabled the use of python instead of verilog in my testing. This is sufficient because it directly tests to two main function of the design and it also indirectly tests all of the other functionality that exists to support it, for example a 8x1 mux and ring counter.

## External hardware

No external hardware is necessary. Other than possibly a driving FPGA.

## AI Tools used 

No AI tools were used to generate Verilog code or python code. Some AI tools were used to debug some of the error messages and testing results.
