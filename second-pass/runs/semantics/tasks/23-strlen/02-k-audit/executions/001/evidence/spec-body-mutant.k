requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim
    <k> #invokeStrlenMutant(str(S:IntSeq)) => isLen(S) </k>
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
