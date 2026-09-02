requires "verification.k"

module AUDIT-NONVACUITY
  imports VERIFICATION

  // Satisfying intended-domain input: one Float and a Float threshold.
  // There are no distinct positions, so the real and claimed result is false.
  // The destination is deliberately mutated to true.
  claim [singleton-false-result]:
    <k> Call(Name("has_close_elements"),
             (list(vCons(0.0, .ValSeq)), 1.0))
        => true </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "has_close_elements" |->
               closureVal(("numbers", "threshold"),
                          HC-FUNCTION-BODY, 0),
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
