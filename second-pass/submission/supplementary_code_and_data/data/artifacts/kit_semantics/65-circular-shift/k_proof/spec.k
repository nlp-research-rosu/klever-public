requires "verification.k"

module SPEC
  imports VERIFICATION

  // Validation scope:
  // - Program boundary: circularShiftClosure expands to the exact translated
  //   function value in solution.mpy, and the fixed call semantics executes it.
  // - Input domain: every X:Int and SHIFT:Int.  The three claims use the exact
  //   nested-conditional guards and collectively cover every integer pair.
  // - Observable final state: returned Str and restored call-frame cells.
  // - Property: reverse iff SHIFT exceeds the decimal-string length; preserve
  //   the canonical implementation's negative-shift behavior; otherwise take
  //   the length-sized rotation window from the doubled decimal string.

  claim [circular-shift-reverse]:
    <k>
      Call(Name("circular_shift"), (X:Int, SHIFT:Int, .Exprs))
      => circularShiftResult(X, SHIFT)
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
    requires SHIFT >Int isLen(strToCodes(Int2String(X)))

  claim [circular-shift-negative]:
    <k>
      Call(Name("circular_shift"), (X:Int, SHIFT:Int, .Exprs))
      => circularShiftResult(X, SHIFT)
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
    requires notBool (
               SHIFT >Int isLen(strToCodes(Int2String(X))))
      andBool SHIFT <Int 0

  claim [circular-shift-rotate]:
    <k>
      Call(Name("circular_shift"), (X:Int, SHIFT:Int, .Exprs))
      => circularShiftResult(X, SHIFT)
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
    requires notBool (
               SHIFT >Int isLen(strToCodes(Int2String(X))))
      andBool notBool (SHIFT <Int 0)
endmodule
