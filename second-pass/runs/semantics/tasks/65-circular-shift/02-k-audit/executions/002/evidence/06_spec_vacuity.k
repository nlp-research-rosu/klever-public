requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports CIRCULAR-SHIFT-VERIFICATION

  // Satisfying input: X=12, SHIFT=1, LEN=2. The real result is "21".
  // This mutation demands the deliberately false result "12".
  claim [false-result-for-satisfying-input]:
    <k>
      Call(Name("circular_shift"), (12, 1))
      =>
      str(iCons(49, iCons(50, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("circular_shift" |-> circularShiftClosure, parent(-1))
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
