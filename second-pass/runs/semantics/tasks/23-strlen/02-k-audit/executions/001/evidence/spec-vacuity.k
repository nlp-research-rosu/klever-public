requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: for the satisfiable empty-string state this demands 0 = 1.
  claim
    <k> #invokeStrlen(str(S:IntSeq)) => isLen(S) +Int 1 </k>
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
                    Return(Call(Name("len"), Name("string"))) .Stmts,
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
