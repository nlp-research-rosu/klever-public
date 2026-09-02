requires "connection-verification.k"

module CONNECTION-SPEC
  imports CONNECTION-VERIFICATION

  // Deliberately bridge-free: this is the universal connection the candidate
  // would need before replacing fixed list equality by its monotonicity summary.
  claim
    <k>
      Compare(
        list(VS:ValSeq),
        CmpOp("==", list(sortVS(VS)))
      )
      => connectionNondecreasing(VS)
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
