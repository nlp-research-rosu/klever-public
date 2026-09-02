requires "verification.k"

module SPEC-ENTRY-ONLY
  imports VERIFICATION

  claim [entry]:
    <k>
      Call(Name("decode_cyclic"), (str(CS), .Exprs))
      =>
      str(decodeCodes(CS))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("decode_cyclic" |-> decodeClosure, parent(-1))
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
