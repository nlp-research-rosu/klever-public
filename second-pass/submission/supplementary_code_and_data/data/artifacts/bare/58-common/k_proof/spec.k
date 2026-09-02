requires "verification.k"

module SPEC
  imports VERIFICATION

  // Functional correctness for arbitrary finite integer lists.  The left
  // side is exactly the constructor tree emitted in solution.mpy; the right
  // side is the independently named contract operation from verification.k.
  claim
    <py>
      <k>
        Module(
          FuncDef("common", Params("l1", "l2"),
            Return(
              Call(
                Name("sorted"),
                BinOp(
                  "&",
                  Call(Name("set"), Name("l1")),
                  Call(Name("set"), Name("l2")))))))
        => list(commonSpec(IS1 ; IS2))
      </k>
      <l1> list(IS1) </l1>
      <l2> list(IS2) </l2>
    </py>
endmodule
