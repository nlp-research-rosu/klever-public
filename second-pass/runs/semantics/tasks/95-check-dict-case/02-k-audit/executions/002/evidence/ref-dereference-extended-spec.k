requires "verification.k"

module REF-DEREFERENCE-EXTENDED-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  // The candidate's priority(30) false splitter sees ref(0) as syntactically
  // non-string and preempts the fixed priority(40) heap dereference.
  claim [ref-to-string-isinstance]:
    <k> #applyK(toCall(builtinV("isinstance")),
                 (ref(0), typeV("str"), .Vals))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> 0 |-> str(iCons(97, .IntSeq)) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
