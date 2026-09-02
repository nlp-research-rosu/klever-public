requires "verification.k"

module LOOP-CORRECTNESS-LABELED
  imports VERIFICATION

  claim [loop-correctness]:
        <k>
          While(Compare(
            BinOp("*", Name("divisor"), Name("divisor")),
            CmpOp("<=", Name("length"))),
            If(Compare(
              BinOp("%", Name("length"), Name("divisor")),
              CmpOp("==", Int(0))),
              Return(Str("NO")),
              .Stmts)
            Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
          ~> (Return(Str("YES")) .Stmts)
          => primeResult(N, D)
        </k>
        <env> _RHO:Map
          "length" |-> intVal(N)
          "divisor" |-> (intVal(D) => ?_VD:Value)
        </env>
        requires N >=Int 2 andBool D >=Int 2
endmodule

module SPEC-LABELED
  imports VERIFICATION-WITH-LOOP-LEMMA

  claim [entry-case-1]:
        <mpy>
          <k>
            solutionProgram
            ~> runWith(
                 TupleExpr(Int(A), Int(B)),
                 TupleExpr(Int(C), Int(D)))
            => lengthResult(B -Int A)
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
        requires A <=Int B andBool C <=Int D
          andBool C <=Int A andBool D >=Int B

  claim [entry-case-2]:
        <mpy>
          <k>
            solutionProgram
            ~> runWith(
                 TupleExpr(Int(A), Int(B)),
                 TupleExpr(Int(C), Int(D)))
            => lengthResult(D -Int A)
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
        requires A <=Int B andBool C <=Int D
          andBool C <=Int A andBool D <Int B

  claim [entry-case-3]:
        <mpy>
          <k>
            solutionProgram
            ~> runWith(
                 TupleExpr(Int(A), Int(B)),
                 TupleExpr(Int(C), Int(D)))
            => lengthResult(B -Int C)
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
        requires A <=Int B andBool C <=Int D
          andBool C >Int A andBool D >=Int B

  claim [entry-case-4]:
        <mpy>
          <k>
            solutionProgram
            ~> runWith(
                 TupleExpr(Int(A), Int(B)),
                 TupleExpr(Int(C), Int(D)))
            => lengthResult(D -Int C)
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
        requires A <=Int B andBool C <=Int D
          andBool C >Int A andBool D <Int B
endmodule
