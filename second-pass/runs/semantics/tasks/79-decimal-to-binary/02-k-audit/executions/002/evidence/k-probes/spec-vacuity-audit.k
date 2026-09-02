requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the real function uses N, not N + 1.
  // Satisfying witness N = 0 yields actual "db0db" but demands "db1db".
  claim <k>
          #runDecimalToBinary(N)
        =>
          str(
            iCons(
              100,
              iCons(
                98,
                seqConcat(
                  binCodes(N +Int 1),
                  iCons(100, iCons(98, .IntSeq))))))
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
    [label(decimal-to-binary-false-n-plus-one)]
endmodule
