requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  // A ground state satisfying entry-reaches-loop's source pattern.
  claim [ground-entry]:
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
      <input>
        cons(1, cons(2, cons(-4, cons(5, .IntList))))
      </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result> NoResult => BoolV(true) </result>
    </mpy>

  // A ground state satisfying loop-correct's source pattern, with B = 0.
  claim [ground-loop]:
    <mpy>
      <k>
        ListV(cons(1, cons(2, cons(-4, cons(5, .IntList)))))
        ~> loop(
          AugAssign(Name("balance"), "+", Name("operation"))
          If(Compare(Name("balance"), CmpOp("<", Int(0))),
            Return(Bool(true)),
            .Stmts))
        ~> execStmts(Return(Bool(false)))
        ~> execStmts(.Stmts)
        => .K
      </k>
      <input>
        cons(1, cons(2, cons(-4, cons(5, .IntList))))
      </input>
      <balance> 0 => 0 </balance>
      <current> 0 => 0 </current>
      <result> NoResult => BoolV(true) </result>
    </mpy>
endmodule
