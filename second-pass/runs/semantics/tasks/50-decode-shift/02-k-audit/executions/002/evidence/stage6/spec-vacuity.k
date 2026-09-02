requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: append lowercase "a" to every returned result.
  // For the satisfying input CS=.IntSeq this requires "" == "a".
  claim [false-result]:
    <k>
      Call(Name("decode_shift"), str(CS:IntSeq))
    =>
      str(seqConcat(decodeCodes(CS), iCons(97, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("decode_shift" |-> decodeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires lowerCodes(CS)
endmodule
