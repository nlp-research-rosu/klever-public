requires "verification.k"

module SPEC-BODY-MUTATION-AUDIT
  imports VERIFICATION

  claim
    <k>
      load(Module(FuncDef("add", Params("x", "y"),
        Return(Name("x")))))
      ~> invoke("add", pyInt(X), pyInt(Y))
      => .K
    </k>
    <env> .Map => "x" |-> pyInt(X) "y" |-> pyInt(Y) </env>
    <functions>
      .Map
      => "add" |-> function("x", "y",
        Return(Name("x")))
    </functions>
    <result> 0 => X +Int Y </result>
endmodule
