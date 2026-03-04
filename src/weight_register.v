module weight_register #(
    parameter WIDTH = 8
)
(
    input clk,
    input [1:0] mode, 
    input [WIDTH-1:0] data, 
    output reg [WIDTH-1:0]out
);

reg [WIDTH-1:0] mem;
localparam [1:0] RESET   = 2'b00;
localparam [1:0] READ    = 2'b10;
localparam [1:0] WRITE   = 2'b10;
localparam [1:0] COMPUTE = 2'b11;

always @ (posedge clk) begin
    if (mode == RESET)
        mem <= 0;
    else if (mode == WRITE)
      mem <= data;
    else if (mode == READ) 
      out <= mem;
    else if (mode == COMPUTE)
      out <= mem & data;
end

endmodule