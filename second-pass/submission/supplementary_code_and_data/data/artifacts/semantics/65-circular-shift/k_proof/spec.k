requires "verification.k"

module CIRCULAR-SHIFT-SPEC
  imports CIRCULAR-SHIFT-VERIFICATION

  // Together these two claims partition every nonnegative shift.
  claim [normal-shift]:
    <k>
      Call(Name("circular_shift"), (X:Int, SHIFT:Int))
      =>
      circularShiftSpec(X, SHIFT, LEN)
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
    requires LEN ==Int isLen(strToCodes(Int2String(X)))
     andBool SHIFT >=Int 0
     andBool SHIFT <=Int LEN

  claim [oversize-shift]:
    <k>
      Call(Name("circular_shift"), (X:Int, SHIFT:Int))
      =>
      circularShiftSpec(X, SHIFT, LEN)
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
    requires LEN ==Int isLen(strToCodes(Int2String(X)))
     andBool SHIFT >=Int 0
     andBool SHIFT >Int LEN
endmodule
