requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Ground body-sensitivity witness: the executed body returns x, while the
  // original addition postcondition still requires 5 at x=2, y=3.
  claim
    <k>
      load(Module(FuncDef("add", Params("x", "y"),
        Return(Name("x")))))
      ~> invoke("add", pyInt(2), pyInt(3))
      => .K
    </k>
    <env> .Map => "x" |-> pyInt(2) "y" |-> pyInt(3) </env>
    <functions>
      .Map
      => "add" |-> function("x", "y", Return(Name("x")))
    </functions>
    <result> 0 => 5 </result>
endmodule
