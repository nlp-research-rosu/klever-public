requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: sort_array([]) returns a fresh empty list, not [99].
  // The entry precondition is satisfied by the concrete empty input object at 0.
  claim
    <k>
      Call(Name("sort_array"), (ref(0), .Exprs))
      => ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("sort_array" |-> sortArrayClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(.ValSeq)
      =>
      (0 |-> list(.ValSeq))
      (1 |-> list(vCons(99, .ValSeq)))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
