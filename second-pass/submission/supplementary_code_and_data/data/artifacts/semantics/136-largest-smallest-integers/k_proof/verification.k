requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Conservative symbolic type refinement.  MPY's generic list iterator
  // yields a Val; under the explicit isInt premise this equivalent rule
  // exposes the same element at sort Int so integer operators can reduce.
  syntax Int ::= intValue(Val) [function, total]
  rule intValue(I:Int) => I

  rule <k> #iterNext(list(vCons(V:Val, REST:ValSeq)))
        => #iterYield(intValue(V), list(REST)) ... </k>
    requires isInt(V)
    [priority(40)]

  // The statement blocks below are the exact constructors emitted in
  // solution.mpy, factored only to keep the claims readable.
  syntax Stmts ::= "scanBody" [function]
                 | "finishBody" [function]
                 | "solutionBody" [function]

  rule scanBody
    => If(Compare(Name("value"), CmpOp("<", Int(0))),
         If(BoolOp("or",
              Compare(Name("largest_negative"), CmpOp("==", Int(0))),
              Compare(Name("value"),
                      CmpOp(">", Name("largest_negative")))),
            Assign(Name("largest_negative"), Name("value")),
            .Stmts),
         .Stmts)
       If(Compare(Name("value"), CmpOp(">", Int(0))),
         If(BoolOp("or",
              Compare(Name("smallest_positive"), CmpOp("==", Int(0))),
              Compare(Name("value"),
                      CmpOp("<", Name("smallest_positive")))),
            Assign(Name("smallest_positive"), Name("value")),
            .Stmts),
         .Stmts)

  rule finishBody
    => If(Compare(Name("largest_negative"), CmpOp("==", Int(0))),
         Assign(Name("largest_negative"), NoneVal),
         .Stmts)
       If(Compare(Name("smallest_positive"), CmpOp("==", Int(0))),
         Assign(Name("smallest_positive"), NoneVal),
         .Stmts)
       Return(TupleExpr(Name("largest_negative"),
                        Name("smallest_positive")))

  rule solutionBody
    => Assign(Name("largest_negative"), Int(0))
       Assign(Name("smallest_positive"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("lst"), scanBody)
       finishBody

  syntax Module ::= "largestSmallestModule" [function]
  rule largestSmallestModule
    => Module(
         FuncDef("largest_smallest_integers", Params("lst"), solutionBody))

  // Mathematical model.  Zero is an internal sentinel: negStep retains the
  // greatest negative seen so far, and posStep the least positive.
  syntax Int ::= negStep(Int, Int) [function, total]
               | posStep(Int, Int) [function, total]
               | negFold(ValSeq, Int) [function, total]
               | posFold(ValSeq, Int) [function, total]
               | finalValue(ValSeq, Int) [function, total]

  rule negStep(A:Int, I:Int) => I
    requires I <Int 0 andBool A ==Int 0
  rule negStep(A:Int, I:Int) => I
    requires I <Int 0 andBool A =/=Int 0 andBool I >Int A
  rule negStep(A:Int, I:Int) => A
    requires I >=Int 0
  rule negStep(A:Int, I:Int) => A
    requires I <Int 0 andBool A =/=Int 0 andBool I <=Int A

  rule posStep(B:Int, I:Int) => I
    requires I >Int 0 andBool B ==Int 0
  rule posStep(B:Int, I:Int) => I
    requires I >Int 0 andBool B =/=Int 0 andBool I <Int B
  rule posStep(B:Int, I:Int) => B
    requires I <=Int 0
  rule posStep(B:Int, I:Int) => B
    requires I >Int 0 andBool B =/=Int 0 andBool I >=Int B

  rule negFold(.ValSeq, A:Int) => A
  rule negFold(vCons(V:Val, REST:ValSeq), A:Int)
    => negFold(REST, negStep(A, intValue(V)))
    requires isInt(V)

  rule posFold(.ValSeq, B:Int) => B
  rule posFold(vCons(V:Val, REST:ValSeq), B:Int)
    => posFold(REST, posStep(B, intValue(V)))
    requires isInt(V)

  rule finalValue(.ValSeq, OLD:Int) => OLD
  rule finalValue(vCons(V:Val, REST:ValSeq), _OLD:Int)
    => finalValue(REST, intValue(V))
    requires isInt(V)

  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq))
    => isInt(V) andBool allInts(REST)

  syntax Val ::= optionalNeg(Int) [function, total]
               | optionalPos(Int) [function, total]
  rule optionalNeg(0) => noneV
  rule optionalNeg(I:Int) => I requires I =/=Int 0
  rule optionalPos(0) => noneV
  rule optionalPos(I:Int) => I requires I =/=Int 0
endmodule
