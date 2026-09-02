requires "verification.k"

module AUDIT-ZERO-ONLY
  imports VERIFICATION

  claim <k> Call(Name("string_sequence"), Int(0))
           => str(sequenceCodes(0)) </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope("string_sequence" |->
                closureVal(("n", .ParamNames), sequenceBody, 0), parent(-1))
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
