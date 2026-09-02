requires "verification.k"

module FULL-PROGRAM-GROUND
  imports VERIFICATION

  claim [empty-false]:
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
        => .K
      </k>
      <input> .IntList </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result> NoResult => BoolV(false) </result>
    </mpy>

  claim [zero-boundary-false]:
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
        => .K
      </k>
      <input> cons(1, cons(-1, .IntList)) </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result> NoResult => BoolV(false) </result>
    </mpy>

  claim [crossing-true]:
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
        => .K
      </k>
      <input> cons(1, cons(-2, .IntList)) </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result> NoResult => BoolV(true) </result>
    </mpy>
endmodule
