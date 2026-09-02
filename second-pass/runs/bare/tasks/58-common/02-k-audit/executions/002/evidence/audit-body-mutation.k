requires "candidate/verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Fresh body-sensitivity mutant: the executed term intersects l1 with l1.
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
                  Call(Name("set"), Name("l1")))))))
        => list(commonSpec(IS1 ; IS2))
      </k>
      <l1> list(IS1) </l1>
      <l2> list(IS2) </l2>
    </py>
endmodule
