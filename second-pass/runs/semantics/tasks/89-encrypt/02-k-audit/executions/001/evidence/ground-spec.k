requires "verification.k"

module GROUND-SPEC
  imports VERIFICATION-WITH-LOOP

  claim [empty]:
        <k> Call(Name("encrypt"), str(.IntSeq)) => str(.IntSeq) </k>
        <env> 0 </env>
        <scopes>
          0  |-> scope("encrypt" |-> encryptClosure, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>

  claim [hi]:
        <k>
          Call(
            Name("encrypt"),
            str(iCons(104, iCons(105, .IntSeq))))
          =>
          str(iCons(108, iCons(109, .IntSeq)))
        </k>
        <env> 0 </env>
        <scopes>
          0  |-> scope("encrypt" |-> encryptClosure, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>

  claim [uppercase-A]:
        <k>
          Call(Name("encrypt"), str(iCons(65, .IntSeq)))
          =>
          str(iCons(121, .IntSeq))
        </k>
        <env> 0 </env>
        <scopes>
          0  |-> scope("encrypt" |-> encryptClosure, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
endmodule
