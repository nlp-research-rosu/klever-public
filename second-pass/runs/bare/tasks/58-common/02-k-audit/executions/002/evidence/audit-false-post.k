requires "candidate/verification.k"

module AUDIT-FALSE-POST
  imports VERIFICATION

  // Fresh false result obligation. For the satisfying witness IS1=IS2=.Ints,
  // the real result is list(.Ints), not list(0, .Ints).
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
        => list(0, commonSpec(IS1 ; IS2))
      </k>
      <l1> list(IS1) </l1>
      <l2> list(IS2) </l2>
    </py>
endmodule
