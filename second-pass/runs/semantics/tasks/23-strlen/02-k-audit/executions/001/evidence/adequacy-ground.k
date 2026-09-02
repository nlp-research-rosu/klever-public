requires "verification.k"

module ADEQUACY-GROUND
  imports VERIFICATION

  claim
    <k> #invokeStrlen(str(.IntSeq)) => 0 </k>
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

  claim
    <k>
      #invokeStrlen(
        str(iCons(97, iCons(98, iCons(99, .IntSeq))))
      )
      => 3
    </k>
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
