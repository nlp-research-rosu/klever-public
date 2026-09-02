requires "reference-semantics/semantics.k"

module TRIANGLE-AREA-VERIFICATION
  imports MPY

  // This is exactly the constructor tree generated in solution.mpy.
  syntax Module ::= "triangleAreaProgram" [function, total]
  rule triangleAreaProgram
    => Module(
         FuncDef("triangle_area", Params("a", "h"),
           Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Int(2)))))
endmodule
