requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation of loop-correct. For B = 0 and OPS =
  // .IntList, real execution returns BoolV(false), not BoolV(true).
  claim [false-loop-result]:
    <mpy>
      <k>
        ListV(OPS) ~> loop(
          AugAssign(Name("balance"), "+", Name("operation"))
          If(Compare(Name("balance"), CmpOp("<", Int(0))),
            Return(Bool(true)),
            .Stmts))
          ~> execStmts(Return(Bool(false)))
          ~> execStmts(.Stmts)
        => .K
      </k>
      <input> _ORIGINAL </input>
      <balance> B => 0 </balance>
      <current> _C => 0 </current>
      <result> NoResult => BoolV(true) </result>
    </mpy>
    [circularity]
endmodule
