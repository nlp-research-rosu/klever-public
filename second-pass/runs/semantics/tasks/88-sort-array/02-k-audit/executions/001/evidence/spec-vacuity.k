requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: empty input is claimed to return a singleton [0].
  // Witness: the unique empty-input pre-state below.
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
      (1 |-> list(vCons(0, .ValSeq)))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
