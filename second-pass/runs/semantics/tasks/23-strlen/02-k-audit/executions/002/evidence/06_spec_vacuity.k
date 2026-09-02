requires "/tmp/audit-work/23-strlen-independent/rebuild/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false postcondition: the real body returns isLen(S), not isLen(S)+1.
  // S = .IntSeq is a satisfying witness: actual 0, demanded 1.
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
