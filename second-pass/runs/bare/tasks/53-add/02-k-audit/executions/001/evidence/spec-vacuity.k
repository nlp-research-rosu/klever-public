requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: the real execution returns X +Int Y, but this
  // destination deliberately demands one more. Witness X=2, Y=3 demands 6
  // although both Python implementations and concrete K execution return 5.
  claim
    <k>
      load(Module(FuncDef("add", Params("x", "y"),
        Return(BinOp("+", Name("x"), Name("y"))))))
      ~> invoke("add", pyInt(X), pyInt(Y))
      => .K
    </k>
    <env> .Map => "x" |-> pyInt(X) "y" |-> pyInt(Y) </env>
    <functions>
      .Map
      => "add" |-> function("x", "y",
        Return(BinOp("+", Name("x"), Name("y"))))
    </functions>
    <result> 0 => (X +Int Y) +Int 1 </result>
endmodule
