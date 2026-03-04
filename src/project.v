/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_cir #( 
  parameter WIDTH = 8, 
  parameter DEPTH = 8, 
  parameter ADDR_WIDTH = $clog2(DEPTH)
  )
(
    input  wire [7:0] ui_in,    // one row of out input array
    output wire [7:0] uo_out,   // one row of our output array 
    input  wire [7:0] uio_in,   // [1:0] - 00 reset 
                                      // - 01 read
                                      // - 10 write
                                      // - 11 compute 
                                // [1] - ready (input)
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  typedef enum logic [2:0] {
    RESET   = 3'b000,
    READ    = 3'b001,
    WRITE   = 3'b010,
    COMPUTE = 3'b011, 
    IDLE    = 3'b101
  } state_t;

  state_t current_state, next_state;

  wire ring_counter_reset = current_state == RESET;
  wire [DEPTH-1:0]counter_out;
  ring_ctr ring_counter
	(
		.clk(clk),
		.rst(ring_counter_reset),
		.out(counter_out)
	);

always @(posedge clk) begin
  if(!rst_n)
    current_state <= RESET;
  else if (counter_out[7] || current_state == RESET)
    current_state <= next_state;
end

always @(*) begin
    next_state = READ; // default: hold state
    case (uio_in[1:0])
        READ:    next_state = READ;
        WRITE:   next_state = WRITE;
        COMPUTE: next_state = COMPUTE;
        RESET:   next_state = RESET;  
        default: next_state = current_state;
    endcase
end

  logic [(DEPTH*2)-1:0] weight_register_states;
  wire [(DEPTH*WIDTH)-1:0] weight_registers_outputs;
  wire [WIDTH-1:0] current_reg_output;
  mux_8to1 output_selector(
    .a(weight_registers_outputs[WIDTH*1-1:0]),
    .b(weight_registers_outputs[WIDTH*2-1:WIDTH*1]),
    .c(weight_registers_outputs[WIDTH*3-1:WIDTH*2]),
    .d(weight_registers_outputs[WIDTH*4-1:WIDTH*3]),
    .e(weight_registers_outputs[WIDTH*5-1:WIDTH*4]),
    .f(weight_registers_outputs[WIDTH*6-1:WIDTH*5]),
    .g(weight_registers_outputs[WIDTH*7-1:WIDTH*6]),
    .h(weight_registers_outputs[WIDTH*8-1:WIDTH*7]),
    .sel(counter_out), 
    .out(current_reg_output)
  );

  genvar i;
	// Generate for loop to instantiate N times
	generate
		for (i = 0; i < DEPTH; i = i + 1) begin
      always @(*) begin
        weight_register_states[i*2+1 : i*2] = counter_out[i] ? current_state[1:0] : 2'b01;
      end
      weight_register curr_reg (clk, weight_register_states[i*2+1 : i*2], ui_in, weight_registers_outputs[(WIDTH*(i+1))-1:(WIDTH*(i))]);
		end
	endgenerate

  reg [WIDTH-1: 0] final_result;
  always @ (posedge clk) begin
    // if we are in compute mode do accumulate 
  if(current_state == COMPUTE) begin
    if(counter_out == 8'b00000001)
      final_result <= current_reg_output;
    else
      final_result <= final_result + current_reg_output;
  end else if(current_state == READ)
    final_result <= current_reg_output;
    // if we are in write mode print the write data 
  else if(current_state == WRITE)
    final_result <= ui_in;
    
  else
    final_result <= 0;
  end

  assign uio_out = 0;
  assign uio_oe  = 0;
  assign uo_out = final_result;
  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
