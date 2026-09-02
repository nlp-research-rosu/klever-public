requires "verification.k"

module FUNCTION-SPEC-FALSE-RESULT
  imports VERIFICATION-WITH-LOOP

  // Deliberately false: append the code for "a" to every claimed result.
  // The empty-string witness satisfies the entry state and actually returns "".
  claim <k>
          Call(Name("encrypt"), str(CS:IntSeq))
          => str(seqConcat(encryptCodes(CS), iCons(97, .IntSeq)))
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
