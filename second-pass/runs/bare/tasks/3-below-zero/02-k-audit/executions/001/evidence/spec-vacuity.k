requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False mutation of the result constraint.  Witness:
  // B = 0 and OPS = .IntList executes the final Return(false), not true.
  claim [loop-correct-false-result]:
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
