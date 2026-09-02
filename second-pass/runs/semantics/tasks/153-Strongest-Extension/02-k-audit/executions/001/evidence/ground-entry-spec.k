requires "/tmp/audit-work/reconstruction/verification.k"

module GROUND-ENTRY-SPEC
  imports STRONGEST-EXTENSION-VERIFICATION

  // Satisfying instance of the submitted entry claim:
  // class C, extensions ["a", "A", "B"]; scores -1, 1, 1.
  claim
    <k>
      Call(
        Name("Strongest_Extension"),
        str(iCons(67, .IntSeq)),
        list(vCons(
          str(iCons(97, .IntSeq)),
          vCons(
            str(iCons(65, .IntSeq)),
            vCons(str(iCons(66, .IntSeq)), .ValSeq)))))
    =>
      str(iCons(67, iCons(46, iCons(65, .IntSeq))))
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
    [label(ground-entry)]
endmodule
