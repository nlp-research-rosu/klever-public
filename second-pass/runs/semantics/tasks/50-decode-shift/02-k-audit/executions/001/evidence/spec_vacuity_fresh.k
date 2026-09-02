requires "verification.k"

module SPEC-VACUITY-FRESH
  imports VERIFICATION

  // Deliberately false: append one extra "a" (code 97) to the required result.
  // Witness CS=.IntSeq satisfies lowerCodes, but the real result is "" and this
  // destination requires "a".
  claim [decode-shift-extra-a]:
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
