requires "verification.k"

module FRESH-VACUITY-SPEC
  imports VERIFICATION

  // Reviewer-authored false result obligation.
  // Witness: IS1 = .Ints and IS2 = .Ints.  The program returns list(.Ints),
  // while this destination demands an extra leading 0.
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
