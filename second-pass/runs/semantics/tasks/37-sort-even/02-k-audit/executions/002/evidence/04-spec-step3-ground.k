requires "verification-step3.k"

module SPEC-STEP3-GROUND
  imports VERIFICATION-STEP3

  // With the material body mutation l[::2] -> l[::3], this is the real result.
  claim [mutated-result]:
    <k>
      Call(
        Name("sort_even"),
        list(vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq))))))
      ~> #observeResult
    =>
      list(vCons(4, vCons(6, vCons(5, vCons(4, .ValSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
        ("sort_even" |-> sortEvenClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HEAP </heap>
    <heapLoc> 0 => ?HL </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // This is the original program's required result and is false for the mutant.
  claim [original-result]:
    <k>
      Call(
        Name("sort_even"),
        list(vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq))))))
      ~> #observeResult
    =>
      list(vCons(3, vCons(6, vCons(5, vCons(4, .ValSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
        ("sort_even" |-> sortEvenClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HEAP </heap>
    <heapLoc> 0 => ?HL </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
