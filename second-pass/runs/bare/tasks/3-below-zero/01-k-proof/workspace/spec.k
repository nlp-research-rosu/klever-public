requires "verification.k"

module SPEC
  imports VERIFICATION

  // The actual Module term generated in solution.mpy reaches the semantic
  // state immediately before iteration, for an arbitrary input list.
  claim [entry-reaches-loop]:
    <mpy>
      <k>
        Module(
          ImportFrom("typing", "List")
          FuncDef("below_zero", Params("operations"),
            Assign(Name("balance"), Int(0))
            For(Name("operation"), Name("operations"),
              AugAssign(Name("balance"), "+", Name("operation"))
              If(Compare(Name("balance"), CmpOp("<", Int(0))),
                Return(Bool(true)),
                .Stmts))
            Return(Bool(false))))
        =>
        ListV(OPS) ~> loop(
          AugAssign(Name("balance"), "+", Name("operation"))
          If(Compare(Name("balance"), CmpOp("<", Int(0))),
            Return(Bool(true)),
            .Stmts))
          ~> execStmts(Return(Bool(false)))
          ~> execStmts(.Stmts)
      </k>
      <input> OPS </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result> NoResult </result>
    </mpy>

  // Induction over OPS.  The claim mentions the exact translated loop body
  // and exact post-loop return, so it proves early return and the boundary
  // condition (zero is not below zero), not merely a helper function.
  claim [loop-correct]:
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
      <result> NoResult => BoolV(belowZeroFrom(B, OPS)) </result>
    </mpy>
    [circularity]
endmodule
