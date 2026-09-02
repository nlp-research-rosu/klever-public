requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the final suffix is "dc" (code 99 for c), not "db".
  // N = 0 satisfies the precondition and the real result is "db0db".
  claim <k>
          #runDecimalToBinary(N)
        =>
          str(
            iCons(
              100,
              iCons(
                98,
                seqConcat(
                  binCodes(N),
                  iCons(100, iCons(99, .IntSeq))))))
        </k>
        <env> 0 </env>
        <scopes>
           0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires N >=Int 0
    [label(false-final-character)]
endmodule
