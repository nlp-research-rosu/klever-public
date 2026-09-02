requires "verification.k"

module MATCH-PARENS-SPEC
  imports MATCH-PARENS-VERIFICATION

  // Inductive invariant for the semantics' #loop iterator state.  The local
  // map may already contain "char" after the first iteration.
  claim
    <k> #loop(str(S:IntSeq), Name("char"), isGoodLoopBody)
         ~> If(Compare(Name("balance"), CmpOp("==", Int(0))),
              Return(Str("T")) .Stmts,
              .Stmts)
         ~> Return(Str(""))
         ~> #endcall
      => goodValue(S, B) ~> CONT
    </k>
    <env> N => CALLER </env>
    <scopes>
      BASE:Map
      (N |-> scope(
        ("s" |-> str(INPUT:IntSeq))
        ("balance" |-> B)
        ("char" |-> OLDCHAR:Val),
        parent(0)))
      => BASE
    </scopes>
    <scopeLoc> N +Int 1 => N </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HEAPLOC </heapLoc>
    <stack>
      ListItem(frame(CONT, CALLER, N)) REST
      => REST
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires B >=Int 0
     andBool notBool (N in_keys(BASE))
    [label(loopCorrect), circularity]

  // Entry form of the loop, before the first iteration has introduced the
  // local "char" binding.  One semantic iteration reaches loopCorrect.
  claim
    <k> #loop(str(S:IntSeq), Name("char"), isGoodLoopBody)
         ~> If(Compare(Name("balance"), CmpOp("==", Int(0))),
              Return(Str("T")) .Stmts,
              .Stmts)
         ~> Return(Str(""))
         ~> #endcall
      => goodValue(S, B) ~> CONT
    </k>
    <env> N => CALLER </env>
    <scopes>
      BASE:Map
      (N |-> scope(
        ("s" |-> str(INPUT:IntSeq))
        ("balance" |-> B),
        parent(0)))
      => BASE
    </scopes>
    <scopeLoc> N +Int 1 => N </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HEAPLOC </heapLoc>
    <stack>
      ListItem(frame(CONT, CALLER, N)) REST
      => REST
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires B >=Int 0
     andBool notBool (N in_keys(BASE))
    [label(loopFirstCorrect)]

  // Correctness of the helper's real closure body and call-frame lifecycle.
  claim
    <k> #applyK(toCall(isGoodClosure), (str(S:IntSeq), .Vals))
         ~> CONT
      => goodValue(S, 0) ~> CONT
    </k>
    <env> CALLER </env>
    <scopes> SCOPES </scopes>
    <scopeLoc> N </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HEAPLOC </heapLoc>
    <stack> STACK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (N in_keys(SCOPES))
    [label(isGoodCorrect)]

  // The recursive mathematical scan and the helper's two string witnesses
  // induce the same branch choice.
  claim
    <k> #forceGood(S:IntSeq, B:Int)
         ~> goodValue(S, B:Int)
         ~> #goodBranch(THEN:Stmts, ELSE:Stmts)
         ~> CONT
      => #expectedBranch(goodFrom(S, B), THEN, ELSE)
         ~> CONT
    </k>
    <env> ENV </env>
    <scopes> SCOPES </scopes>
    <scopeLoc> SCOPELOC </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HEAPLOC </heapLoc>
    <stack> STACK </stack>
    <ret> RET </ret>
    <exc> EXC </exc>
    <exit-code> EXITCODE </exit-code>
    requires B >=Int 0
    [label(goodBranchCorrect), circularity]

  // Functional correctness of the requested HumanEval entry point.
  claim
    <k> #applyK(
          toCall(matchParensClosure),
          (list(vCons(str(A:IntSeq),
                      vCons(str(B:IntSeq), .ValSeq))), .Vals))
         ~> CONT
      => expectedAnswer(A, B) ~> CONT
    </k>
    <env> CALLER </env>
    <scopes>
      BASE:Map
      (0 |-> scope(
        ("is_good" |-> isGoodClosure) MODULELOCALS:Map,
        parent(-1)))
    </scopes>
    <scopeLoc> N </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HEAPLOC </heapLoc>
    <stack> STACK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires parensOnly(A) andBool parensOnly(B)
     andBool N >=Int 1
     andBool notBool (N +Int 1 in_keys(BASE))
     andBool notBool (N in_keys(
       BASE (0 |-> scope(
         ("is_good" |-> isGoodClosure) MODULELOCALS,
         parent(-1)))))
    [label(matchParensCorrect)]
endmodule
