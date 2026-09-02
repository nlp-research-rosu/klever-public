requires "reference-semantics/semantics.k"

module IS-SORTED-VERIFICATION
  imports MPY

  // The exact loop body emitted in solution.mpy.
  syntax Stmts ::= "isSortedLoopBody" [macro]
  rule isSortedLoopBody
    => If(Compare(Name("number"), CmpOp("<", Name("previous"))),
          Assign(Name("result"), Bool(false)),
          .Stmts)
       If(Compare(Name("number"), CmpOp("==", Name("previous"))),
          AugAssign(Name("repeats"), "+", Int(1)),
          Assign(Name("repeats"), Int(1)))
       If(Compare(Name("repeats"), CmpOp(">", Int(2))),
          Assign(Name("result"), Bool(false)),
          .Stmts)
       Assign(Name("previous"), Name("number"))
       .Stmts

  // The exact translated entry point, represented as its callable value.
  syntax Val ::= "isSortedClosure" [macro]
  rule isSortedClosure
    => closureVal(
         ("lst", .ParamNames),
         Assign(Name("result"), Bool(true))
         Assign(Name("previous"), Int(0))
         Assign(Name("repeats"), Int(0))
         For(Name("number"), Name("lst"), isSortedLoopBody)
         Return(Name("result"))
         .Stmts,
         0)

  // Constructor-form instance of the supplied generic call rule.  It avoids
  // leaving a fresh frame represented as an opaque Map update during proof.
  rule <k> #applyK(toCall(isSortedClosure), ARGS:Vals) ~> CONT
        => #bindP(("lst", .ParamNames), ARGS)
           ~> Assign(Name("result"), Bool(true))
              Assign(Name("previous"), Int(0))
              Assign(Name("repeats"), Int(0))
              For(Name("number"), Name("lst"), isSortedLoopBody)
              Return(Name("result"))
              .Stmts
           ~> #endcall
           </k>
       <env> CALLER:Int => NEW:Int </env>
       <scopes>
         SCOPES:Map
         =>
         (NEW |-> scope(
           ("$plain" |-> true)
           ("lst" |-> noneV)
           ("number" |-> 0)
           ("result" |-> false)
           ("previous" |-> 0)
           ("repeats" |-> 0),
           parent(0)))
         SCOPES
       </scopes>
       <scopeLoc> NEW => NEW +Int 1 </scopeLoc>
       <stack> .List => ListItem(frame(CONT, CALLER, NEW)) ... </stack>
       [priority(40)]

  // Decidable instances of the supplied ordinary (non-cell) local-frame
  // rules.  The marker is proof-only and is never visible to the program.
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _P:Parent) ... </scopes>
       requires "$plain" in_keys(M) andBool X in_keys(M)
       [priority(30)]

  rule <k> #look("result", L:Int) => V:Val ... </k>
       <scopes>
         ... L |-> scope(("result" |-> V) REST:Map, _P:Parent) ...
       </scopes>
       requires notBool "result" in_keys(REST)
       [priority(20)]
  rule <k> #look("previous", L:Int) => V:Val ... </k>
       <scopes>
         ... L |-> scope(("previous" |-> V) REST:Map, _P:Parent) ...
       </scopes>
       requires notBool "previous" in_keys(REST)
       [priority(20)]
  rule <k> #look("repeats", L:Int) => V:Val ... </k>
       <scopes>
         ... L |-> scope(("repeats" |-> V) REST:Map, _P:Parent) ...
       </scopes>
       requires notBool "repeats" in_keys(REST)
       [priority(20)]
  rule <k> #look("number", L:Int) => V:Val ... </k>
       <scopes>
         ... L |-> scope(("number" |-> V) REST:Map, _P:Parent) ...
       </scopes>
       requires notBool "number" in_keys(REST)
       [priority(20)]

  rule <k> #bindP(("lst", .ParamNames), (V:Val, .Vals))
        => #bindP(.ParamNames, .Vals) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("lst" |-> _OLD:Val) REST:Map
           =>
           ("lst" |-> V) REST,
           _P:Parent) ...
       </scopes>
       requires notBool "lst" in_keys(REST)
       [priority(20)]

  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _P:Parent) ... </scopes>
       requires "$plain" in_keys(M)
       [priority(30)]

  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _P:Parent) ... </scopes>
       requires "$plain" in_keys(M)
       [priority(30)]

  rule <k> #bindTgt(Name("number"), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("number" |-> _OLD:Val) REST:Map
           =>
           ("number" |-> V) REST,
           _P:Parent) ...
       </scopes>
       requires notBool "number" in_keys(REST)
       [priority(20)]

  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _P:Parent) ... </scopes>
       requires "$plain" in_keys(M)
       [priority(30)]

  rule <k> Assign(Name("result"), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("result" |-> _OLD:Val) REST:Map
           =>
           ("result" |-> V) REST,
           _P:Parent) ...
       </scopes>
       requires notBool "result" in_keys(REST)
       [priority(20)]
  rule <k> Assign(Name("previous"), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("previous" |-> _OLD:Val) REST:Map
           =>
           ("previous" |-> V) REST,
           _P:Parent) ...
       </scopes>
       requires notBool "previous" in_keys(REST)
       [priority(20)]
  rule <k> Assign(Name("repeats"), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("repeats" |-> _OLD:Val) REST:Map
           =>
           ("repeats" |-> V) REST,
           _P:Parent) ...
       </scopes>
       requires notBool "repeats" in_keys(REST)
       [priority(20)]

  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ],
                          _P:Parent) ...
       </scopes>
       requires "$plain" in_keys(M) andBool X in_keys(M)
       [priority(30)]

  rule <k> AugAssign(Name("repeats"), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("repeats" |-> OLD:Val) REST:Map
           =>
           ("repeats" |-> applyBin(OP, OLD, V)) REST,
           _P:Parent) ...
       </scopes>
       requires notBool "repeats" in_keys(REST)
       [priority(20)]

  // The implementation returns this known boolean local.  Consuming the
  // local directly preempts strictness from heating a symbolic Bool under an
  // internal freezer that the Haskell backend cannot cool.
  rule <k> Return(Name("result")) ~> _ => #pop </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("result" |-> B:Bool) REST:Map, _P:Parent) ...
       </scopes>
       <ret> noRet => retV(B) </ret>
       requires notBool "result" in_keys(REST)
       [priority(20)]

  // Direct instances of the three integer guards in the loop body.  They
  // preempt strictness from placing symbolic Bool results under an internal
  // If freezer.
  rule <k>
         If(Compare(Name("number"), CmpOp("<", Name("previous"))),
            T:Stmts, _E:Stmts)
         => T
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("number" |-> X:Int)
           ("previous" |-> P:Int)
           REST:Map,
           _PAR:Parent) ...
       </scopes>
       requires X <Int P
       [priority(20)]
  rule <k>
         If(Compare(Name("number"), CmpOp("<", Name("previous"))),
            _T:Stmts, E:Stmts)
         => E
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("number" |-> X:Int)
           ("previous" |-> P:Int)
           REST:Map,
           _PAR:Parent) ...
       </scopes>
       requires X >=Int P
       [priority(20)]

  rule <k>
         If(Compare(Name("number"), CmpOp("==", Name("previous"))),
            T:Stmts, _E:Stmts)
         => T
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("number" |-> X:Int)
           ("previous" |-> P:Int)
           REST:Map,
           _PAR:Parent) ...
       </scopes>
       requires X ==Int P
       [priority(20)]
  rule <k>
         If(Compare(Name("number"), CmpOp("==", Name("previous"))),
            _T:Stmts, E:Stmts)
         => E
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           ("number" |-> X:Int)
           ("previous" |-> P:Int)
           REST:Map,
           _PAR:Parent) ...
       </scopes>
       requires X =/=Int P
       [priority(20)]

  rule <k>
         If(Compare(Name("repeats"), CmpOp(">", Int(2))),
            T:Stmts, _E:Stmts)
         => T
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("repeats" |-> C:Int) REST:Map,
                          _PAR:Parent) ...
       </scopes>
       requires C >Int 2
       [priority(20)]
  rule <k>
         If(Compare(Name("repeats"), CmpOp(">", Int(2))),
            _T:Stmts, E:Stmts)
         => E
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(("repeats" |-> C:Int) REST:Map,
                          _PAR:Parent) ...
       </scopes>
       requires C <=Int 2
       [priority(20)]

  // Constructor form of MAP's update/delete equation used by #pop.
  rule ((N:Int |-> _S:Scope) BASE:Map) [ N <- undef ] => BASE
       requires notBool N in_keys(BASE)
       [simplification]

  // Universal integer-list carrier used by the claims.
  syntax ValSeq ::= intsToVals(IntSeq)

  // Drive list iteration by the inductive source carrier, so the prover
  // branches on IntSeq constructors rather than an opaque function equality.
  rule <k> #iterNext(list(intsToVals(.IntSeq))) => #iterDone ... </k>
       [priority(30)]
  rule <k> #iterNext(list(intsToVals(iCons(I:Int, IS:IntSeq))))
        => #iterYield(I, list(intsToVals(IS))) ... </k>
       [priority(30)]

  // Straight-line summary of one exact translated loop body.  Each component
  // is the corresponding supplied Int/Bool rule: preserve false, enforce
  // PREV <= X, update the equal run length, and enforce its bound.
  rule
    <k> isSortedLoopBody ~> #loopLbl(NEXT:K) => #loopLbl(NEXT) ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("$plain" |-> true)
        ("result" |-> OK:Bool)
        ("previous" |-> PREV:Int)
        ("repeats" |-> COUNT:Int)
        ("number" |-> X:Int)
        LOCALS:Map
        =>
        ("$plain" |-> true)
        ("result" |->
          (OK
           andBool PREV <=Int X
           andBool nextRepeats(X, PREV, COUNT) <=Int 2))
        ("previous" |-> X)
        ("repeats" |-> nextRepeats(X, PREV, COUNT))
        ("number" |-> X)
        LOCALS,
        _PARENT:Parent) ...
    </scopes>
    requires notBool "$plain" in_keys(LOCALS)
     andBool notBool "result" in_keys(LOCALS)
     andBool notBool "previous" in_keys(LOCALS)
     andBool notBool "repeats" in_keys(LOCALS)
     andBool notBool "number" in_keys(LOCALS)
    [priority(20)]

  // Pure mathematical scan state.  nextRepeats counts the current run;
  // scanAll conjoins adjacent nondecreasing order and the run-length bound.
  syntax Int ::= nextRepeats(Int, Int, Int) [function, total]
  rule nextRepeats(X:Int, P:Int, C:Int) => C +Int 1
       requires X ==Int P
  rule nextRepeats(X:Int, P:Int, _C:Int) => 1
       requires X =/=Int P

  syntax ScanState ::= scanState(Bool, Int, Int)
                     | scanAll(Bool, Int, Int, IntSeq)
                       [function, total]
  rule scanAll(OK:Bool, P:Int, C:Int, .IntSeq)
    => scanState(OK, P, C)
  rule scanAll(OK:Bool, P:Int, C:Int, iCons(X:Int, R:IntSeq))
    => scanAll(
         OK
         andBool P <=Int X
         andBool nextRepeats(X, P, C) <=Int 2,
         X,
         nextRepeats(X, P, C),
         R)

  syntax Bool ::= scanResult(ScanState) [function, total]
  rule scanResult(scanState(OK:Bool, _P:Int, _C:Int)) => OK

  // On the promised nonnegative domain, this fold says precisely:
  // adjacent values never decrease and no equal-value run exceeds length two.
  syntax Bool ::= isSortedContract(IntSeq) [function, total]
  rule isSortedContract(IS:IntSeq)
    => scanResult(scanAll(true, 0, 0, IS))
endmodule

module IS-SORTED-WITH-LOOP-LEMMA
  imports IS-SORTED-VERIFICATION

  // This rule is exactly the loop claim proved in IS-SORTED-LOOP-SPEC.  The
  // second proof definition uses that established result compositionally to
  // prove the complete entry-point call.
  rule
    <k>
      #loop(list(intsToVals(IS:IntSeq)),
            Name("number"),
            isSortedLoopBody)
      ~> Return(Name("result"))
      ~> #endcall
      =>
      scanResult(scanAll(OK:Bool, PREV:Int, COUNT:Int, IS)) ~> CONT:K
    </k>
    <env> FRAME:Int => CALLER:Int </env>
    <scopes>
      FRAME |-> scope(
        ("$plain" |-> true)
        ("result" |-> OK)
        ("previous" |-> PREV)
        ("repeats" |-> COUNT)
        ("number" |-> _NUMBER:Int)
        LOCALS:Map,
        PARENT:Parent)
      BASE:Map
      =>
      BASE
    </scopes>
    <scopeLoc> CURRENT:Int => SAVED:Int </scopeLoc>
    <stack>
      ListItem(frame(CONT, CALLER, SAVED))
      STACK:List
      =>
      STACK
    </stack>
    <ret> noRet => noRet </ret>
    requires FRAME ==Int SAVED
     andBool notBool FRAME in_keys(BASE)
     andBool notBool "result" in_keys(LOCALS)
     andBool notBool "previous" in_keys(LOCALS)
     andBool notBool "repeats" in_keys(LOCALS)
     andBool notBool "number" in_keys(LOCALS)
     andBool notBool "$plain" in_keys(LOCALS)
     andBool notBool "$cells" in_keys(LOCALS)
     andBool notBool "$cells" in_keys(
       ("result" |-> OK)
       ("previous" |-> PREV)
       ("repeats" |-> COUNT)
       LOCALS)

endmodule
