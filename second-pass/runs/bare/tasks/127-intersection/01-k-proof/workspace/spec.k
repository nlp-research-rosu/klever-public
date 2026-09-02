requires "verification.k"

// Inductive proof of the proof lemma used by the whole-program claim.  The
// recursive primeResult reference takes exactly the same three branches as
// one concrete execution of the While: exhausted search, found factor, or
// advance divisor.  The third branch closes by circularity after progress.
module LOOP-CORRECTNESS-SPEC
  imports VERIFICATION

  claim <k>
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

// Universal correctness for all integer endpoints satisfying the prompt's
// interval precondition.  These four claims are the exhaustive choices for
// max(start1,start2) and min(end1,end2); together their right sides are exactly
// lengthResult(min(B,D)-max(A,C)).
module SPEC
  imports VERIFICATION-WITH-LOOP-LEMMA

  claim <mpy>
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

  claim <mpy>
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

  claim <mpy>
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

  claim <mpy>
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
