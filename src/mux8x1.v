module mux_8to1 #( 
  parameter WIDTH = 8
  )
  ( input [WIDTH-1:0] a,                
    input [WIDTH-1:0] b,                
    input [WIDTH-1:0] c,                
    input [WIDTH-1:0] d,                
    input [WIDTH-1:0] e,                
    input [WIDTH-1:0] f,                
    input [WIDTH-1:0] g,                
    input [WIDTH-1:0] h,                
    input [WIDTH-1:0] sel,          
    output reg [WIDTH-1:0] out);         

   // This always block gets executed whenever a/b/c/d/sel changes value
   // When that happens, based on value in sel, output is assigned to either a/b/c/d
   always @ (*) begin
      case (sel)
         8'b00000001 : out = a;
         8'b00000010 : out = b;
         8'b00000100 : out = c;
         8'b00001000 : out = d;
         8'b00010000 : out = e;
         8'b00100000 : out = f;
         8'b01000000 : out = g;
         8'b10000000 : out = h;
         default : out = 0;
      endcase
   end
endmodule