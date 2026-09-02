requires "verification-body-mutant.k"

module BODY-SENSITIVITY-WITH
  imports VERIFICATION

  claim <k> Call(Name("string_sequence"), 1)
           => str(sequenceCodes(1)) </k>
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

module BODY-SENSITIVITY-BASE
  imports VERIFICATION-BASE

  claim <k> Call(Name("string_sequence"), 1)
           => str(sequenceCodes(1)) </k>
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
