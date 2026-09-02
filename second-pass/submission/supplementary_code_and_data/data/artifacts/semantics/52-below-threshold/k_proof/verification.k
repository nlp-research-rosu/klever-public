requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // IntSeq gives the proof a genuinely typed inductive domain for the prompt's
  // "list of numbers". intsToVals is a symbolic ValSeq constructor whose
  // iterator equations below are exactly those of
  // vCons(I1, ... vCons(In, .ValSeq)).
  syntax ValSeq ::= intsToVals(IntSeq)

  // The generic list iterator cannot narrow through a symbolic function
  // application. These conservative cases expose one constructor of that
  // typed representation; they add no behavior for ordinary ValSeq terms.
  rule <k> #iterNext(list(intsToVals(.IntSeq))) => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(intsToVals(iCons(I:Int, REST:IntSeq))))
        => #iterYield(I, list(intsToVals(REST))) ... </k>
       [priority(40)]

  // Mathematical contract: every element is strictly less than T.
  syntax Bool ::= belowThresholdSpec(IntSeq, Int) [function, total]
  rule belowThresholdSpec(.IntSeq, _:Int) => true
  rule belowThresholdSpec(iCons(I:Int, REST:IntSeq), T:Int)
    => (I <Int T) andBool belowThresholdSpec(REST, T)

  // Exact translated function body from solution.mpy, factored only to keep
  // the claims readable. These are macros, not replacement execution rules.
  syntax Stmts ::= "belowThresholdLoopBody" [macro]
  rule belowThresholdLoopBody
    => If(Compare(Name("number"), CmpOp(">=", Name("t"))),
          Return(Bool(false)),
          .Stmts)

  syntax Stmts ::= "belowThresholdBody" [macro]
  rule belowThresholdBody
    => Expr(Str(
         "Return True if all numbers in the list l are below threshold t.\n    >>> below_threshold([1, 2, 4, 10], 100)\n    True\n    >>> below_threshold([1, 20, 4, 10], 5)\n    False\n    "))
       For(Name("number"), Name("l"), belowThresholdLoopBody)
       Return(Bool(true))

  syntax KItem ::= #belowThresholdCall(IntSeq, Int) [macro]
  rule #belowThresholdCall(IS:IntSeq, T:Int)
    => Call(
         closureVal(("l", "t", .ParamNames), belowThresholdBody, 0),
         (list(intsToVals(IS)), T, .Exprs))
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Derived loop-summary rule. LOOP-SPEC proves this exact reachability
  // property against VERIFICATION-BASE (which does not contain this rule);
  // SPEC then uses it to compose the end-to-end call proof.
  rule
    <k> #loop(list(intsToVals(IS:IntSeq)),
              Name("number"),
              belowThresholdLoopBody)
         ~> (Return(Bool(true)) .Stmts)
         ~> #endcall
      => belowThresholdSpec(IS, T)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      1 |-> scope(
        "l"      |-> list(intsToVals(_ORIGINAL:IntSeq))
        "number" |-> _OLD:Int
        "t"      |-> T:Int,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> BUILTINS:Scope
      =>
      0  |-> scope(.Map, parent(-1))
      -1 |-> BUILTINS
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [priority(40)]
endmodule
