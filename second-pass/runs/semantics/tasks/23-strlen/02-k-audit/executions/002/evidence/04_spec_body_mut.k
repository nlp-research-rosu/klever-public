requires "04_verification_body_mut.k"

module SPEC-BODY-MUT
  imports VERIFICATION-BODY-MUT

  // Deliberately false: the actually executed body now returns 0 for all inputs,
  // but this obligation still demands structural string length.
  claim
    <k> #invokeStrlenMut(str(S:IntSeq)) => isLen(S) </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    =>
      (0 |-> scope(
              .Map [
                "strlen" <-
                  closureVal(
                    "string",
                    Return(Int(0)) .Stmts,
                    0
                  )
              ],
              parent(-1)
            )
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
