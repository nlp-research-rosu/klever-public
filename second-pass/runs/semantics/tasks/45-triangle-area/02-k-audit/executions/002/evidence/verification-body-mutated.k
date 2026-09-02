requires "reference-semantics/semantics.k"

module TRIANGLE-AREA-BODY-MUTATION-VERIFICATION
  imports MPY

  syntax Module ::= "triangleAreaProgramMutation" [function, total]
  rule triangleAreaProgramMutation
    => Module(
         FuncDef("triangle_area", Params("a", "h"),
           Return(BinOp("/", BinOp("+", Name("a"), Name("h")), Int(2)))))
endmodule
