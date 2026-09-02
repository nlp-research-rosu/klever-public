requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim <k>
          #runDecimalToBinaryMutated(N)
        =>
          str(
            iCons(
              100,
              iCons(
                98,
                seqConcat(
                  binCodes(N),
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
    [label(decimal-to-binary-mutated-body-must-fail)]
endmodule
