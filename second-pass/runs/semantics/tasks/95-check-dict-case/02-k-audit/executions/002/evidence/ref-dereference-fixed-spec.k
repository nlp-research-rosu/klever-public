requires "verification-no-bridges.k"

module REF-DEREFERENCE-FIXED-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  // Under the fixed call layer, the priority(40) builtin-argument rule reads
  // heap object 0 before dispatching isinstance, so the result is true.
  claim [ref-to-string-isinstance]:
    <k> #applyK(toCall(builtinV("isinstance")),
                 (ref(0), typeV("str"), .Vals))
      => true
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
