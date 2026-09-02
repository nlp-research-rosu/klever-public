requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact syntactic abbreviations for the two translated Python bodies.
  syntax Stmts ::= "collectLoopBody" [macro]
  rule collectLoopBody
    => If(
         Compare(Name("value"), CmpOp("==", Name("digit"))),
         Expr(Call(Attribute(Name("result"), "append"), Name("name"), .Exprs))
           .Stmts,
         .Stmts)
       .Stmts

  syntax Stmts ::= "collectDigitBody" [macro]
  rule collectDigitBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("arr"), collectLoopBody)
       Return(Name("result"))
       .Stmts

  syntax Stmts ::= "byLengthBody" [macro]
  rule byLengthBody
    => Return(
         BinOp("+",
           BinOp("+",
             BinOp("+",
               BinOp("+",
                 BinOp("+",
                   BinOp("+",
                     BinOp("+",
                       BinOp("+",
                         Call(Name("collect_digit"),
                              (Name("arr"), Int(9), Str("Nine"), .Exprs)),
                         Call(Name("collect_digit"),
                              (Name("arr"), Int(8), Str("Eight"), .Exprs))),
                       Call(Name("collect_digit"),
                            (Name("arr"), Int(7), Str("Seven"), .Exprs))),
                     Call(Name("collect_digit"),
                          (Name("arr"), Int(6), Str("Six"), .Exprs))),
                   Call(Name("collect_digit"),
                        (Name("arr"), Int(5), Str("Five"), .Exprs))),
                 Call(Name("collect_digit"),
                      (Name("arr"), Int(4), Str("Four"), .Exprs))),
               Call(Name("collect_digit"),
                    (Name("arr"), Int(3), Str("Three"), .Exprs))),
             Call(Name("collect_digit"),
                  (Name("arr"), Int(2), Str("Two"), .Exprs))),
           Call(Name("collect_digit"),
                (Name("arr"), Int(1), Str("One"), .Exprs))))
       .Stmts

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule
    => Module(
         FuncDef(
           "collect_digit",
           Params("arr", "digit", "name", .ParamNames),
           collectDigitBody)
         FuncDef(
           "by_length",
           Params("arr", .ParamNames),
           byLengthBody)
         .Stmts)

  // True exactly on ValSeq values whose elements are all Python integers.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool allInts(REST)

  // Derived sort-refinement lemma for MPY-INT's existing equality equation.
  rule applyCmp("==", V:Val, I:Int)
    => {V}:>Int ==Int I
    requires isInt(V)
    [simplification]

  // The exact accumulator result of collect_digit's remaining iterations.
  // Its off-domain totalization ignores non-integers; the theorem only uses
  // allInts inputs, where this is exactly the Python helper's behavior.
  syntax ValSeq ::= collectAcc(ValSeq, Int, Val, ValSeq) [function, total]
  rule collectAcc(.ValSeq, _:Int, _:Val, ACC:ValSeq) => ACC
  rule collectAcc(vCons(X:Val, REST:ValSeq), D:Int, N:Val, ACC:ValSeq)
    => #if isInt(X)
       #then
         #if {X}:>Int ==Int D
         #then collectAcc(
                 REST,
                 D,
                 N,
                 valSeqConcat(ACC, vCons(N, .ValSeq)))
         #else collectAcc(REST, D, N, ACC)
         #fi
       #else collectAcc(REST, D, N, ACC)
       #fi

  // The prompt's result: one group per digit, in descending digit order.
  syntax ValSeq ::= byLengthVS(ValSeq) [function, total]
  rule byLengthVS(VS:ValSeq)
    => valSeqConcat(
         valSeqConcat(
           valSeqConcat(
             valSeqConcat(
               valSeqConcat(
                 valSeqConcat(
                   valSeqConcat(
                     valSeqConcat(
                       collectAcc(VS, 9, str(strToCodes("Nine")), .ValSeq),
                       collectAcc(VS, 8, str(strToCodes("Eight")), .ValSeq)),
                     collectAcc(VS, 7, str(strToCodes("Seven")), .ValSeq)),
                   collectAcc(VS, 6, str(strToCodes("Six")), .ValSeq)),
                 collectAcc(VS, 5, str(strToCodes("Five")), .ValSeq)),
               collectAcc(VS, 4, str(strToCodes("Four")), .ValSeq)),
             collectAcc(VS, 3, str(strToCodes("Three")), .ValSeq)),
           collectAcc(VS, 2, str(strToCodes("Two")), .ValSeq)),
         collectAcc(VS, 1, str(strToCodes("One")), .ValSeq))
endmodule
