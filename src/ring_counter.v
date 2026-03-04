module ring_ctr  #(parameter WIDTH=8)
  (
	input clk,
	input rst,
  	output reg [WIDTH-1:0] out
  );

  always @ (posedge clk) begin
      if (rst)
         out <= 1;
      else begin
        out[WIDTH-1] <= out[0];
        for (int i = 0; i < WIDTH-1; i=i+1) begin
          out[i+1] <= out[i];
        end
      end
  end
endmodule