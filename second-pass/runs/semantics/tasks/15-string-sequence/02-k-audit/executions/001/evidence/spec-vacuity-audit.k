requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for every N >= 1, demand the sequence through N+1.
  // N=1 is a satisfying witness: the program returns "0 1", not "0 1 2".
  claim <k> Call(Name("string_sequence"), N:Int)
           => str(sequenceCodes(N +Int 1)) </k>
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
    requires N >=Int 1
endmodule
