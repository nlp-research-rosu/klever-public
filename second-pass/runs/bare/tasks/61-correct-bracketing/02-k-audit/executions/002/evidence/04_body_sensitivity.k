requires "/tmp/audit-work/61-correct-bracketing-audit/candidate/verification.k"

module BODY-SENSITIVITY
  imports MPY-VERIFICATION

  // The actual term in <k> differs from solutionProgram at one material
  // constructor: count starts at 1, not 0.  On the satisfying input "", the
  // fixed semantics returns false, so the original result true must be rejected.
  claim [mutated-empty]:
    <mpy>
      <k>
        Run(
          Module(
            FuncDef("correct_bracketing", Params("brackets"),
              Assign(Name("count"), Int(1))
              For(Name("bracket"), Name("brackets"),
                If(Compare(Name("bracket"), CmpOp("==", Str("("))),
                  Assign(Name("count"),
                    BinOp("+", Name("count"), Int(1))),
                  If(Compare(Name("count"), CmpOp("==", Int(0))),
                    Return(Bool(false)),
                    .Stmts)
                  Assign(Name("count"),
                    BinOp("-", Name("count"), Int(1)))))
              Return(Compare(Name("count"), CmpOp("==", Int(0)))))),
          "correct_bracketing",
          "")
        => boolVal(true)
      </k>
      <functions> .Map => ?_FS:Map </functions>
      <env> .Map => ?_ENV:Map </env>
    </mpy>
endmodule
