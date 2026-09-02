requires "verification.k"

// A retV state is in the broad match domain of the proof-local helper bridges,
// but fixed call/return execution cannot complete from it because Return
// requires noRet. The bridge nonetheless fabricates the mathematical result.
module AUDIT-HELPER-BROAD-CONTEXT-SPEC
  imports COUNT-NUMS-VERIFICATION-BASE

  claim
    <k> #applyK(toCall(positiveDigitClosure), (1, .Vals)) => 1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> retV(42) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> #applyK(toCall(negativeDigitClosure), (1, .Vals)) => -1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> retV(42) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// The signed helper's proof-local bridge omits the defining scope. Rebinding
// the called negative helper to an exact closure returning 99 makes fixed
// execution return 99, while the bridge still rewrites to signedDigitSum(-1).
module AUDIT-SIGNED-FIXED-RESULT-SPEC
  imports DIGIT-FUNCTION-LEMMAS

  claim
    <k> #applyK(toCall(signedDigitClosure), (-1, .Vals)) => 99 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        ("negative_digit_sum" |-> closureVal("n", Return(Int(99)), 0)),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-SIGNED-BRIDGE-RESULT-SPEC
  imports DIGIT-FUNCTION-LEMMAS

  claim
    <k> #applyK(toCall(signedDigitClosure), (-1, .Vals)) => -1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        ("negative_digit_sum" |-> closureVal("n", Return(Int(99)), 0)),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// The loop summaries likewise omit the module binding used by countLoopBody.
// On the intended integer element -1, the rebound helper makes the body count
// one element; countFold instead uses the proof-side signedDigitSum and counts 0.
module AUDIT-COUNT-WITH-N-FIXED-RESULT-SPEC
  imports SIGNED-DIGIT-LEMMA

  claim
    <k> #loop(list(vCons(-1, .ValSeq)), Name("n"), countLoopBody) => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        ("signed_digit_sum" |-> closureVal("n", Return(Int(99)), 0)),
        parent(-1))
      1 |-> scope(
        ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 0 "n" |-> 0)
        => ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 1 "n" |-> -1),
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-COUNT-WITH-N-BRIDGE-RESULT-SPEC
  imports SIGNED-DIGIT-LEMMA

  claim
    <k> #loop(list(vCons(-1, .ValSeq)), Name("n"), countLoopBody) => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        ("signed_digit_sum" |-> closureVal("n", Return(Int(99)), 0)),
        parent(-1))
      1 |-> scope(
        ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 0 "n" |-> 0)
        => ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 0 "n" |-> -1),
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-COUNT-INITIAL-FIXED-RESULT-SPEC
  imports COUNT-LOOP-WITH-N-LEMMA

  claim
    <k> #loop(list(vCons(-1, .ValSeq)), Name("n"), countLoopBody) => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        ("signed_digit_sum" |-> closureVal("n", Return(Int(99)), 0)),
        parent(-1))
      1 |-> scope(
        ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 0)
        => ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 1 "n" |-> -1),
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-COUNT-INITIAL-BRIDGE-RESULT-SPEC
  imports COUNT-LOOP-WITH-N-LEMMA

  claim
    <k> #loop(list(vCons(-1, .ValSeq)), Name("n"), countLoopBody) => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        ("signed_digit_sum" |-> closureVal("n", Return(Int(99)), 0)),
        parent(-1))
      1 |-> scope(
        ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 0)
        => ("arr" |-> list(vCons(-1, .ValSeq)) "count" |-> 0 "n" |-> -1),
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
