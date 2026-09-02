requires "semantic.k"

module VERIFICATION
  imports MPY
  imports K-EQUAL

  // Independent mathematical folds for the two extrema.
  syntax OptInt ::= "#negFold" "(" IntSeq "," OptInt ")" [function, total]
                  | "#posFold" "(" IntSeq "," OptInt ")" [function, total]
                  | "#negStep" "(" Int "," OptInt ")" [function, total]
                  | "#posStep" "(" Int "," OptInt ")" [function, total]
                  | "#negCandidate" "(" Int "," OptInt ")" [function, total]
                  | "#posCandidate" "(" Int "," OptInt ")" [function, total]

  rule #negFold(nil, N) => N
  rule #negFold(icon(I, IS), N)
    => #negFold(IS, #negStep(I, N))
  rule #posFold(nil, P) => P
  rule #posFold(icon(I, IS), P)
    => #posFold(IS, #posStep(I, P))

  rule #negStep(I, N)
    => #if I <Int 0
       #then #negCandidate(I, N)
       #else N
       #fi
  rule #negCandidate(I, pyNone) => pyInt(I)
  rule #negCandidate(I, pyInt(N))
    => #if I >Int N
       #then pyInt(I)
       #else pyInt(N)
       #fi

  rule #posStep(I, P)
    => #if I >Int 0
       #then #posCandidate(I, P)
       #else P
       #fi
  rule #posCandidate(I, pyNone) => pyInt(I)
  rule #posCandidate(I, pyInt(P))
    => #if I <Int P
       #then pyInt(I)
       #else pyInt(P)
       #fi

  syntax Program ::= "solutionProgram" [macro]
  rule solutionProgram => Module(
    FuncDef("largest_smallest_integers", Params("lst"),
      Assign(Name("largest_negative"), NoneVal)
      Assign(Name("smallest_positive"), NoneVal)
      For(Name("value"), Name("lst"),
        If(Compare(Name("value"), CmpOp("<", Int(0))),
          If(Compare(Name("largest_negative"), CmpOp("is", NoneVal)),
            Assign(Name("largest_negative"), Name("value")),
            If(Compare(Name("value"), CmpOp(">", Name("largest_negative"))),
              Assign(Name("largest_negative"), Name("value")),
              .Stmts)),
          .Stmts)
        If(Compare(Name("value"), CmpOp(">", Int(0))),
          If(Compare(Name("smallest_positive"), CmpOp("is", NoneVal)),
            Assign(Name("smallest_positive"), Name("value")),
            If(Compare(Name("value"), CmpOp("<", Name("smallest_positive"))),
              Assign(Name("smallest_positive"), Name("value")),
              .Stmts)),
          .Stmts))
      Return(
        TupleExpr(Name("largest_negative"), Name("smallest_positive")))))

endmodule
