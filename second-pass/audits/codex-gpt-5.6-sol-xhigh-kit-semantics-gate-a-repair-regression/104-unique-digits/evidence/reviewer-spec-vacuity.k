requires "verification.k"

module REVIEWER-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: [1] satisfies the theorem domain, but the real
  // function returns [1]. This postcondition instead requires the fresh result
  // list to contain [2].
  claim [wrong-singleton-result]:
    <k>
      Call(
        Name("unique_digits"),
        (list(vCons(1, .ValSeq)), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
              "unique_digits"
                |-> closureVal(("x", .ParamNames), uniqueDigitsBody, 0),
              parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(vCons(2, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
