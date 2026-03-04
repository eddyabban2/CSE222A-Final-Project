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
        out <= {out[WIDTH-2:0], out[WIDTH-1]};

        // Self-correcting: if out ever becomes 0 (e.g. X propagation), recover
        if (out == {WIDTH{1'b0}})
            out <= {{WIDTH-1{1'b0}}, 1'b1};
      end
  end
endmodule
