requires "verification.k"

module SPEC
  imports VERIFICATION

  // For every string represented by an arbitrary sequence of character codes,
  // the translated function returns the structural length of that sequence.
  claim
    <k> #invokeStrlen(str(S:IntSeq)) => isLen(S) </k>
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
