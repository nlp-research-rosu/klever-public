requires "/tmp/audit-work/audit-108/source/verification.k"

// The candidate SIGNED-DIGIT-LEMMA ignores the scope containing the helper
// bindings. It therefore claims a result even when fixed execution cannot
// resolve positive_digit_sum.
module SIGNED-BRIDGE-FALSE-WITNESS
  imports SIGNED-DIGIT-LEMMA

  claim
    <k> #applyK(toCall(signedDigitClosure), (12, .Vals))
      => 3 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
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

// The identical claim under the preceding layer has no signed-call shortcut.
// It enters signedFunctionBody, then becomes stuck looking up the deliberately
// absent positive_digit_sum binding.
module SIGNED-BRIDGE-FIXED-COMPARISON
  imports DIGIT-FUNCTION-LEMMAS

  claim
    <k> #applyK(toCall(signedDigitClosure), (12, .Vals))
      => 3 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
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

// The positive helper summary also omits the ret cell proved by its auxiliary
// claim. With a pre-existing return value, the real Return rule cannot fire,
// but the summary still fabricates a normal result.
module POSITIVE-BRIDGE-FALSE-WITNESS
  imports DIGIT-LOOP-LEMMAS

  claim
    <k> #applyK(toCall(positiveDigitClosure), (12, .Vals))
      => 3 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> retV(99) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module POSITIVE-BRIDGE-FIXED-COMPARISON
  imports COUNT-NUMS-VERIFICATION-BASE

  claim
    <k> #applyK(toCall(positiveDigitClosure), (12, .Vals))
      => 3 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> retV(99) </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
