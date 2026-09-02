requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false postcondition: at X=2, Y=3 this requires 6 although execution
  // and both independent Python implementations return 5.
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
    <result> 0 => X +Int Y +Int 1 </result>
endmodule
