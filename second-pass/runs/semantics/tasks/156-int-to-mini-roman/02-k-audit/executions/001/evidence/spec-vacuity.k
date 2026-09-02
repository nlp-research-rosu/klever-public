requires "/tmp/audit-work/candidate/verification.k"

module AUDIT-SPEC-VACUITY
  imports ROMAN-VERIFICATION

  // Deliberately false: append one extra lowercase "x" to the genuine result.
  // For the satisfying witness N=1, the program returns "i" but this target is
  // "ix".
  claim [romanWrongExtraX]:
    <k>
      Call(Name("int_to_mini_roman"), Int(N))
      => str(seqConcat(romanSpec(N), iCons(120, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", romanThousandsBody, 0)
        "_roman_hundreds"
          |-> closureVal("digit", romanHundredsBody, 0)
        "_roman_tens"
          |-> closureVal("digit", romanTensBody, 0)
        "_roman_ones"
          |-> closureVal("digit", romanOnesBody, 0)
        "int_to_mini_roman"
          |-> closureVal("number", romanSolutionBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1 andBool N <=Int 1000
endmodule
