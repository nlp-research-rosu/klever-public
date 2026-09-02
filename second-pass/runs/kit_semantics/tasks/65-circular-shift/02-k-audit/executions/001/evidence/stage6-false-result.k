requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Satisfying rotate-branch witness: len(str(100)) = 3 and shift = 1.
  // The actual result is "010"; this deliberately demands unchanged "100".
  claim [wrong-rotate-result]:
    <k>
      Call(Name("circular_shift"), (100, 1, .Exprs))
      => str(strToCodes("100"))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
              "circular_shift" |-> circularShiftClosure,
              parent(-1))
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
