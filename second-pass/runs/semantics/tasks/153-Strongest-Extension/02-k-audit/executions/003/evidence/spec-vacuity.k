requires "verification.k"

module STRONGEST-EXTENSION-SPEC-VACUITY
  imports STRONGEST-EXTENSION-VERIFICATION

  // Deliberately false: the real body inserts "." (ASCII 46), while this
  // destination requires "!" (ASCII 33).
  claim
    <k>
      Call(
        Name("Strongest_Extension"),
        str(CLASS:IntSeq),
        list(vCons(
          str(E1:IntSeq),
          vCons(str(E2:IntSeq),
          vCons(str(E3:IntSeq), .ValSeq)))))
    =>
      str(seqConcat(
        seqConcat(CLASS, iCons(33, .IntSeq)),
        bestExtension(
          vCons(str(E1), vCons(str(E2), vCons(str(E3), .ValSeq))),
          E1,
          extensionStrength(E1))))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(false-separator),
     depends(extension-strength-correct, selection-loop-correct)]
endmodule
