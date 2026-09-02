requires "verification.k"

module SPEC-ACTUAL-GROUND-EVEN
  imports VERIFICATION

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
      0 |-> list(vCons(2, vCons(4, vCons(3, vCons(6, .ValSeq)))))
      =>
      (0 |-> list(vCons(2, vCons(4, vCons(3, vCons(6, .ValSeq))))))
      (1 |-> list(condRev(
        sortVS(vCons(2, vCons(4, vCons(3, vCons(6, .ValSeq))))),
        true)))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
