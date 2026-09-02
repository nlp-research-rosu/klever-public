requires "reference-semantics/semantics.k"
requires "representation.k"

module VERIFICATION-CORE-SYNTAX
  imports MPY-SYNTAX
  imports MPY-CORE
  imports INT
  imports BOOL

  syntax Stmts ::= "lsiLoopBody" [macro]
  syntax Stmts ::= "lsiBody" [macro]

  syntax Bool ::= takeNeg(Int, Int) [function, total]
                | takePos(Int, Int) [function, total]

  syntax Int ::= nextNeg(Int, Int) [function, total]
               | nextPos(Int, Int) [function, total]
               | scanNeg(IntSeq, Int) [function, total]
               | scanPos(IntSeq, Int) [function, total]

  syntax Int ::= lastValue(IntSeq, Int) [function, total]
  syntax Val ::= negativeResult(Int) [function, total]
               | positiveResult(Int) [function, total]
endmodule

module VERIFICATION-CORE
  imports MPY
  imports INT-VAL-REP
  imports VERIFICATION-CORE-SYNTAX
  imports INT
  imports BOOL

  rule lsiLoopBody
    => If(Compare(Name("value"), CmpOp("<", Int(0))),
         If(BoolOp("or",
              Compare(Name("largest_negative"), CmpOp("==", Int(0))),
              Compare(Name("value"), CmpOp(">", Name("largest_negative")))),
            Assign(Name("largest_negative"), Name("value")),
            .Stmts),
         .Stmts)
       If(Compare(Name("value"), CmpOp(">", Int(0))),
         If(BoolOp("or",
              Compare(Name("smallest_positive"), CmpOp("==", Int(0))),
              Compare(Name("value"), CmpOp("<", Name("smallest_positive")))),
            Assign(Name("smallest_positive"), Name("value")),
            .Stmts),
         .Stmts)

  rule lsiBody
    => Assign(Name("largest_negative"), Int(0))
       Assign(Name("smallest_positive"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst"), lsiLoopBody)
       Return(TupleExpr(
         IfExp(Compare(Name("largest_negative"), CmpOp("==", Int(0))),
               NoneVal,
               Name("largest_negative")),
         IfExp(Compare(Name("smallest_positive"), CmpOp("==", Int(0))),
               NoneVal,
               Name("smallest_positive"))))

  rule takeNeg(X:Int, N:Int)
    => X <Int 0 andBool (N ==Int 0 orBool X >Int N)
  rule takePos(X:Int, P:Int)
    => X >Int 0 andBool (P ==Int 0 orBool X <Int P)

  rule nextNeg(X:Int, N:Int) => X
    requires takeNeg(X, N)
  rule nextNeg(X:Int, N:Int) => N
    requires notBool takeNeg(X, N)

  rule nextPos(X:Int, P:Int) => X
    requires takePos(X, P)
  rule nextPos(X:Int, P:Int) => P
    requires notBool takePos(X, P)

  rule scanNeg(.IntSeq, N:Int) => N
  rule scanNeg(iCons(I:Int, IS:IntSeq), N:Int)
    => scanNeg(IS, nextNeg(I, N))

  rule scanPos(.IntSeq, P:Int) => P
  rule scanPos(iCons(I:Int, IS:IntSeq), P:Int)
    => scanPos(IS, nextPos(I, P))

  rule lastValue(.IntSeq, CURRENT:Int) => CURRENT
  rule lastValue(iCons(I:Int, IS:IntSeq), _:Int)
    => lastValue(IS, I)

  rule negativeResult(0) => noneV
  rule negativeResult(N:Int) => N
    requires N =/=Int 0

  rule positiveResult(0) => noneV
  rule positiveResult(P:Int) => P
    requires P =/=Int 0
endmodule
