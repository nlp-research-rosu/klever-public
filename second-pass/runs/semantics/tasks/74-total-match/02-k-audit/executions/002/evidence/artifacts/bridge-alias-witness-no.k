requires "verification-no-loop-bridge.k"

module BRIDGE-ALIAS-WITNESS-NO
  imports TOTAL-MATCH-VERIFICATION

  // Identical false conclusion, checked without the candidate For bridge.
  claim
    <k>
      For(
        Name("x"),
        list(strVals(ssCons(iCons(97, .IntSeq), .StrSeq))),
        AugAssign(
          Name("x"),
          "+",
          Call(Name("len"), Name("x"))) .Stmts)
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
      1  |-> scope(("x" |-> 0 => "x" |-> 1), parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
