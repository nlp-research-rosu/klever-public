requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION-WITH-LOOP

  // Fresh false result mutation of FUNCTION-SPEC. The original empty-input
  // result is str(.IntSeq); this mutation demands the one-character string
  // "x" (code 120) from the same satisfiable initial state.
  claim <k>
          Call(Name("encrypt"), str(.IntSeq))
          => str(iCons(120, .IntSeq))
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
