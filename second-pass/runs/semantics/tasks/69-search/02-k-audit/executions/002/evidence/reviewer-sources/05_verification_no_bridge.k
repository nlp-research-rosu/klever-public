requires "reference-semantics/semantics.k"

module SEARCH-VERIFICATION-NO-BRIDGE
  imports MPY

  // The exact statement blocks emitted from solution.py.  Naming them keeps
  // the loop invariants in spec.k readable; these are syntax macros only.
  syntax Stmts ::= "#innerBody" [macro]
  rule #innerBody
    => If(Compare(Name("item"), CmpOp("==", Name("value"))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts) .Stmts

  syntax Stmts ::= "#outerBody" [macro]
  rule #outerBody
    => Assign(Name("count"), Int(0))
       For(Name("item"), Name("lst"), #innerBody)
       If(Compare(Name("count"), CmpOp(">=", Name("value"))),
          If(Compare(Name("value"), CmpOp(">", Name("result"))),
             Assign(Name("result"), Name("value")) .Stmts,
             .Stmts) .Stmts,
          .Stmts) .Stmts

  syntax Stmts ::= "#searchBody" [macro]
  rule #searchBody
    => Assign(Name("result"), UnaryOp("-", Int(1)))
       For(Name("value"), Name("lst"), #outerBody)
       Return(Name("result")) .Stmts

  // A refinement sort using the *same* ValSeq constructors gives symbolic
  // inputs an Int-only constructor induction principle without a conversion
  // wrapper that would obscure list iteration.
  syntax IntValSeq ::= ".ValSeq" | vCons(Int, IntValSeq)
  syntax ValSeq ::= IntValSeq

  syntax Bool ::= allPositive(IntValSeq) [function, total]
  rule allPositive(.ValSeq) => true
  rule allPositive(vCons(X:Int, XS:IntValSeq))
    => X >Int 0 andBool allPositive(XS)

  syntax Bool ::= nonEmpty(IntValSeq) [function, total]
  rule nonEmpty(.ValSeq) => false
  rule nonEmpty(vCons(_:Int, _:IntValSeq)) => true

  // Mathematical frequency and contract result.  greatestFreq folds over the
  // original list, retaining exactly the largest positive X whose occurrence
  // count in the complete list is at least X.
  syntax Int ::= frequency(Int, IntValSeq) [function, total]
  rule frequency(_:Int, .ValSeq) => 0
  rule frequency(X:Int, vCons(Y:Int, YS:IntValSeq))
    => (#if X ==Int Y #then 1 #else 0 #fi) +Int frequency(X, YS)

  syntax Int ::= chooseFreq(Int, IntValSeq, Int) [function, total]
  rule chooseFreq(X:Int, ALL:IntValSeq, BEST:Int) => X
    requires X >Int 0
     andBool frequency(X, ALL) >=Int X
     andBool X >Int BEST
  rule chooseFreq(X:Int, ALL:IntValSeq, BEST:Int) => BEST
    requires notBool (X >Int 0
              andBool frequency(X, ALL) >=Int X
              andBool X >Int BEST)

  syntax Int ::= greatestFreq(IntValSeq) [function, total]
               | greatestFreqFrom(IntValSeq, IntValSeq, Int) [function, total]
  rule greatestFreq(ALL:IntValSeq)
    => greatestFreqFrom(ALL, ALL, -1)
  rule greatestFreqFrom(.ValSeq, _:IntValSeq, BEST:Int) => BEST
  rule greatestFreqFrom(vCons(X:Int, XS:IntValSeq), ALL:IntValSeq, BEST:Int)
    => greatestFreqFrom(XS, ALL, chooseFreq(X, ALL, BEST))

endmodule
