requires "verification.k"

module SPEC-LEN-BRIDGE-WITNESS
  imports VERIFICATION

  // Fixed-semantics concrete representation: the length is correctly two.
  claim [actual-list-len-two]:
    <k>
      Call(Name("len"), list(vCons(10, vCons(20, .ValSeq))))
      =>
      2
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Proof-local intVals is documented as the typed encoding of the same
  // two-element integer list, but the priority bridge forces the false value 1.
  claim [abstract-list-len-one]:
    <k>
      Call(Name("len"), list(intVals(iCons(10, iCons(20, .IntSeq)))))
      =>
      1
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // The bridge's ellipsis admits this different observable continuation too.
  // Python evaluates len([10, 20]) == 1 to false; the extended K theory proves true.
  claim [wrong-value-observed-by-comparison]:
    <k>
      Compare(
        Call(Name("len"), list(intVals(iCons(10, iCons(20, .IntSeq))))),
        CmpOp("==", Int(1)))
      =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
