requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: circular_shift(12, 1) is "21", not "12".
  claim [wrong-result]:
    <k>
      Call(Name("circular_shift"), (12, 1, .Exprs))
      => str(strToCodes("12"))
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
