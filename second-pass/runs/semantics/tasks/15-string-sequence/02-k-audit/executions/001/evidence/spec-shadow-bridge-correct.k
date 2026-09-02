requires "verification.k"

module AUDIT-SHADOW-BRIDGE-CORRECT
  imports VERIFICATION

  claim <k> Call(Name("string_sequence"), Int(1))
           => str(sequenceCodes(0)) </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(
                 "string_sequence" |->
                   closureVal(("n", .ParamNames), sequenceBody, 0)
                 "range" |->
                   closureVal(("a", "b", .ParamNames),
                              Return(rangeObj(0, 0, 1)) .Stmts, 0),
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
endmodule
