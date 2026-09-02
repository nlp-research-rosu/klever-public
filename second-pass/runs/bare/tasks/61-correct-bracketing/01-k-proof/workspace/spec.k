requires "verification.k"

module SPEC
  imports MPY-VERIFICATION

  // Loop invariant: at any nonnegative current depth N, executing the
  // remaining characters S and the function's final return computes exactly
  // bracketSpec(N,S).  CURRENT is the loop variable's previous value.
  claim [loop]:
        <mpy>
          <k>
            forLoop("bracket", S:String,
              If(Compare(Name("bracket"), CmpOp("==", Str("("))),
                Assign(Name("count"),
                  BinOp("+", Name("count"), Int(1))),
                If(Compare(Name("count"), CmpOp("==", Int(0))),
                  Return(Bool(false)),
                  .Stmts)
                Assign(Name("count"),
                  BinOp("-", Name("count"), Int(1)))))
            ~> Return(Compare(Name("count"), CmpOp("==", Int(0)))) .Stmts
            => boolVal(bracketSpec(N, S))
          </k>
          <functions> _FS:Map </functions>
          <env>
            "bracket" |-> strVal(_CURRENT:String)
            "brackets" |-> strVal(_ORIGINAL:String)
            "count" |-> intVal(N:Int)
            => ?_FINAL_ENV:Map
          </env>
        </mpy>
        requires N >=Int 0

  claim [main]:
        <mpy>
          <k> Run(solutionProgram, "correct_bracketing", S:String)
            => boolVal(bracketSpec(0, S)) </k>
          <functions> .Map => ?_FS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>

  claim [example-open]: <mpy>
          <k> Run(solutionProgram, "correct_bracketing", "(")
            => boolVal(false) </k>
          <functions> .Map => ?_FS:Map </functions> <env> .Map => ?_ENV:Map </env>
        </mpy>
  claim [example-pair]: <mpy>
          <k> Run(solutionProgram, "correct_bracketing", "()")
            => boolVal(true) </k>
          <functions> .Map => ?_FS:Map </functions> <env> .Map => ?_ENV:Map </env>
        </mpy>
  claim [example-nested]: <mpy>
          <k> Run(solutionProgram, "correct_bracketing", "(()())")
            => boolVal(true) </k>
          <functions> .Map => ?_FS:Map </functions> <env> .Map => ?_ENV:Map </env>
        </mpy>
  claim [example-bad-prefix]: <mpy>
          <k> Run(solutionProgram, "correct_bracketing", ")(()")
            => boolVal(false) </k>
          <functions> .Map => ?_FS:Map </functions> <env> .Map => ?_ENV:Map </env>
        </mpy>
endmodule
