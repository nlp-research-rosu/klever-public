requires "verification.k"

module SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // Materially mutate the program term actually executed by the claim:
  // the early-return branch now returns false, while the destination remains
  // the original loop body returning true. The proof must reject this.
  claim [mutated-entry]:
    <mpy>
      <k>
        Module(
          ImportFrom("typing", "List")
          FuncDef("below_zero", Params("operations"),
            Assign(Name("balance"), Int(0))
            For(Name("operation"), Name("operations"),
              AugAssign(Name("balance"), "+", Name("operation"))
              If(Compare(Name("balance"), CmpOp("<", Int(0))),
                Return(Bool(false)),
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
endmodule
