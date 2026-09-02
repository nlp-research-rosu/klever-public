requires "reference-semantics/semantics.k"

module VERIFICATION-ITER-DEFINITIONAL
  imports MPY

  // The exact translated body and loop body from solution.mpy.  Keeping these
  // as macros makes the reachability claims readable while still executing
  // the program through the supplied Python semantics.
  syntax Stmts ::= "rollingMaxLoopBody" [macro]
  rule rollingMaxLoopBody =>
    If(Name("first"),
       Assign(Name("maximum"), Name("number"))
       Assign(Name("first"), Bool(false)),
       Assign(Name("maximum"),
              Call(Name("max"),
                   (Name("maximum"), Name("number"), .Exprs))))
    Expr(Call(Attribute(Name("result"), "append"), (Name("maximum"), .Exprs)))

  syntax Stmts ::= "rollingMaxBody" [macro]
  rule rollingMaxBody =>
    Expr(Str("Return the maximum seen so far at every position in numbers."))
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("first"), Bool(true))
    Assign(Name("maximum"), Int(0))
    Assign(Name("number"), Int(0))
    For(Name("number"), Name("numbers"), rollingMaxLoopBody)
    Return(Name("result"))

  syntax Module ::= "rollingMaxModule" [macro]
  rule rollingMaxModule =>
    Module(ImportFrom("typing", ("List", .ParamNames))
           FuncDef("rolling_max", Params(("numbers", .ParamNames)), rollingMaxBody))

  // IntSeq is used as a genuinely symbolic sequence of integer inputs.  This
  // embedding excludes non-integer Val elements at the sort level.
  // Auditor-only definitional presentation of the candidate's exact two
  // constructor equations. IntSeq has only these two constructors, so totality
  // adds no value assumption; [function] permits reduction under consumers.
  syntax ValSeq ::= intsVS(IntSeq) [function, total]
  rule intsVS(.IntSeq)                => .ValSeq
  rule intsVS(iCons(I:Int, R:IntSeq)) => vCons(I, intsVS(R))

  // Mathematical rolling maximum, written as an accumulator fold so its
  // recursive equation is exactly the loop invariant after one iteration.
  syntax Int ::= nextRolling(Bool, Int, Int) [function, total]
  rule nextRolling(true,  _M:Int, I:Int) => I
  rule nextRolling(false,  M:Int, I:Int) => maxInt(M, I)

  syntax ValSeq ::= rollingAcc(IntSeq, Bool, Int, ValSeq) [function, total]
  rule rollingAcc(.IntSeq, _F:Bool, _M:Int, ACC:ValSeq) => ACC
  rule rollingAcc(iCons(I:Int, R:IntSeq), F:Bool, M:Int, ACC:ValSeq)
    => rollingAcc(R, false, nextRolling(F, M, I),
                  valSeqConcat(ACC, vCons(nextRolling(F, M, I), .ValSeq)))

  // The other loop-carried locals are included in the invariant so the loop
  // lemma describes the complete final local frame, not only the result list.
  syntax Bool ::= firstAfter(IntSeq, Bool) [function, total]
  rule firstAfter(_IS:IntSeq, false)                 => false
  rule firstAfter(.IntSeq, F:Bool)                 => F
  rule firstAfter(iCons(_I:Int, _R:IntSeq), _F:Bool) => false

  syntax Int ::= maximumAfter(IntSeq, Bool, Int) [function, total]
  rule maximumAfter(.IntSeq, _F:Bool, M:Int) => M
  rule maximumAfter(iCons(I:Int, R:IntSeq), F:Bool, M:Int)
    => maximumAfter(R, false, nextRolling(F, M, I))

  syntax Int ::= numberAfter(IntSeq, Int) [function, total]
  rule numberAfter(.IntSeq, N:Int)                => N
  rule numberAfter(iCons(I:Int, R:IntSeq), _N:Int) => numberAfter(R, I)
endmodule
