requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The exact translated program and its two statement blocks.  Keeping these
  // as constructor-valued functions makes the invocation claim bind the real
  // function body while keeping the loop circularity readable.
  syntax Stmts ::= "nextSmallestLoopBody" [function]
  rule nextSmallestLoopBody =>
    Assign(Name("x"), BinOp("+", Name("x"), Int(0)))
    If(UnaryOp("not", Name("found_smallest")),
      Assign(Name("smallest"), Name("x"))
      Assign(Name("found_smallest"), Bool(true)),
      If(Compare(Name("x"), CmpOp("<", Name("smallest"))),
        Assign(Name("second"), Name("smallest"))
        Assign(Name("found_second"), Bool(true))
        Assign(Name("smallest"), Name("x")),
        If(BoolOp(
          "and",
          Compare(Name("x"), CmpOp("!=", Name("smallest"))),
          BoolOp(
            "or",
            UnaryOp("not", Name("found_second")),
            Compare(Name("x"), CmpOp("<", Name("second"))))),
          Assign(Name("second"), Name("x"))
          Assign(Name("found_second"), Bool(true)),
          .Stmts)))

  syntax Stmts ::= "nextSmallestBody" [function]
  rule nextSmallestBody =>
    Expr(Str("\n    Return the second-smallest distinct integer in lst, or None when it\n    does not exist.\n    "))
    Assign(Name("found_smallest"), Bool(false))
    Assign(Name("found_second"), Bool(false))
    Assign(Name("smallest"), Int(0))
    Assign(Name("second"), Int(0))
    Assign(Name("x"), Int(0))
    For(Name("x"), Name("lst"), nextSmallestLoopBody)
    If(Name("found_second"), Return(Name("second")), .Stmts)
    Return(NoneVal)

  syntax Module ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(FuncDef("next_smallest", Params("lst"), nextSmallestBody))

  // Domain predicate for the prompt's list-of-integers contract.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, REST:ValSeq)) => isInt(V) andBool allInts(REST)

  // Guarded total projection from the dynamic Val sort to Int.  It is opaque
  // outside isInt; on the guarded domain it is merely the semantics' built-in
  // partial injection, exposed in a solver-friendly form.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V:Val) => isInt(V)

  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]

  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]

  rule projectIntTotal(I:Int) => I [simplification]
  rule projectIntTotal(projectIntTotal(V:Val)) => projectIntTotal(V)
    [simplification]

  // Guarded dispatch twins of the frozen integer rules.  They do not replace
  // program execution; they restate the same equations after sort refinement.
  rule applyBin("+", V:Val, W:Val)
    => projectIntTotal(V) +Int projectIntTotal(W)
    requires isInt(V) andBool isInt(W)
    [simplification]

  rule applyCmp("<", V:Val, W:Val)
    => projectIntTotal(V) <Int projectIntTotal(W)
    requires isInt(V) andBool isInt(W)
    [simplification]

  rule applyCmp("!=", V:Val, W:Val)
    => projectIntTotal(V) =/=Int projectIntTotal(W)
    requires isInt(V) andBool isInt(W)
    [simplification]

  // Exact mathematical fold of the program's accumulator state.
  syntax ScanState ::= scanState(Int, Bool, Int, Bool)
  syntax ScanState ::= scanStep(Int, Int, Bool, Int, Bool) [function, total]

  rule scanStep(X:Int, A:Int, false, B:Int, HB:Bool)
    => scanState(X, true, B, HB)
    [simplification]

  rule scanStep(X:Int, A:Int, true, B:Int, HB:Bool)
    => scanState(X, true, A, true)
    requires X <Int A
    [simplification]

  rule scanStep(X:Int, A:Int, true, B:Int, HB:Bool)
    => scanState(A, true, B, HB)
    requires X ==Int A
    [simplification]

  rule scanStep(X:Int, A:Int, true, B:Int, false)
    => scanState(A, true, X, true)
    requires X >Int A
    [simplification]

  rule scanStep(X:Int, A:Int, true, B:Int, true)
    => scanState(A, true, X, true)
    requires X >Int A andBool X <Int B
    [simplification]

  rule scanStep(X:Int, A:Int, true, B:Int, true)
    => scanState(A, true, B, true)
    requires X >Int A andBool X >=Int B
    [simplification]

  syntax ScanState ::= scanAfter(ValSeq, ScanState) [function, total]
  rule scanAfter(REST:ValSeq, scanState(A:Int, HA:Bool, B:Int, HB:Bool))
    => scanVS(REST, A, HA, B, HB)
    [simplification]

  syntax ScanState ::= scanVS(ValSeq, Int, Bool, Int, Bool) [function, total]
  rule scanVS(.ValSeq, A:Int, HA:Bool, B:Int, HB:Bool)
    => scanState(A, HA, B, HB)
    [simplification]
  rule scanVS(vCons(V:Val, REST:ValSeq), A:Int, HA:Bool, B:Int, HB:Bool)
    => scanAfter(REST, scanStep(projectIntTotal(V), A, HA, B, HB))
    requires isInt(V)
    [simplification]
  rule scanVS(vCons(V:Val, _:ValSeq), A:Int, HA:Bool, B:Int, HB:Bool)
    => scanState(A, HA, B, HB)
    requires notBool isInt(V)
    [simplification]

  syntax Int ::= scanSmallest(ScanState) [function, total]
  syntax Bool ::= scanFoundSmallest(ScanState) [function, total]
  syntax Int ::= scanSecond(ScanState) [function, total]
  syntax Bool ::= scanFoundSecond(ScanState) [function, total]

  rule scanSmallest(scanState(A:Int, _:Bool, _:Int, _:Bool)) => A [simplification]
  rule scanFoundSmallest(scanState(_:Int, HA:Bool, _:Int, _:Bool)) => HA [simplification]
  rule scanSecond(scanState(_:Int, _:Bool, B:Int, _:Bool)) => B [simplification]
  rule scanFoundSecond(scanState(_:Int, _:Bool, _:Int, HB:Bool)) => HB [simplification]

  syntax Int ::= lastInt(ValSeq, Int) [function, total]
  rule lastInt(.ValSeq, X0:Int) => X0 [simplification]
  rule lastInt(vCons(V:Val, REST:ValSeq), _:Int)
    => lastInt(REST, projectIntTotal(V))
    requires isInt(V)
    [simplification]
  rule lastInt(vCons(V:Val, _:ValSeq), X0:Int) => X0
    requires notBool isInt(V)
    [simplification]

  syntax Val ::= nextSmallestSpec(ValSeq) [function, total]
  rule nextSmallestSpec(VS:ValSeq)
    => #if scanFoundSecond(scanVS(VS, 0, false, 0, false))
       #then scanSecond(scanVS(VS, 0, false, 0, false))
       #else noneV
       #fi
    [simplification]
endmodule
