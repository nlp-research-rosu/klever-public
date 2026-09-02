requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of entry-small: n = 1 satisfies N < 2, but the
  // submitted implementation and trusted canonical both return false, not true.
  claim
    <k>
      #entryBody ~> #endcall
      =>
      true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (
        -1 |-> B:Scope
        0 |-> scope(
          "is_prime" |-> closureVal(
            "n", .ParamNames,
            #entryBody,
            0),
          parent(-1))
        1 |-> scope("n" |-> N, parent(0)))
      =>
      (
        -1 |-> B
        0 |-> scope(
          "is_prime" |-> closureVal(
            "n", .ParamNames,
            #entryBody,
            0),
          parent(-1)))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N <Int 2
    [label(entry-small-false-result)]
endmodule
