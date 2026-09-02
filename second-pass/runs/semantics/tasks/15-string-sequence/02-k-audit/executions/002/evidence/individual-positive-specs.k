requires "verification.k"

module AUDIT-LOOP-ONLY
  imports VERIFICATION-BASE

  claim <k>
          #loop(rangeObj(I:Int, N:Int +Int 1, 1), Name("i"), sequenceLoopBody)
          ~> Return(Name("result")) ~> #endcall
        => str(sequenceCodes(N))
        </k>
        <env> 1 => 0 </env>
        <scopes>
          (1 |-> scope("result" |-> str(sequenceCodes(I -Int 1))
                      "n" |-> N "i" |-> J:Int, parent(0))
           0 |-> scope("string_sequence" |->
                 closureVal(("n", .ParamNames), sequenceBody, 0), parent(-1))
           -1 |-> builtinsScope)
          => (1 |-> scope("result" |-> str(sequenceCodes(I -Int 1))
                         "n" |-> N "i" |-> J, parent(0))
              0 |-> scope("string_sequence" |->
                    closureVal(("n", .ParamNames), sequenceBody, 0), parent(-1))
              -1 |-> builtinsScope) [1 <- undef]
        </scopes>
        <scopeLoc> 2 => 1 </scopeLoc>
        <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
        <ret> noRet </ret>
    requires I >=Int 1 andBool (N ==Int 0 orBool N >=Int 1)
     andBool (I ==Int N +Int 1 orBool I <Int N +Int 1)
endmodule

module AUDIT-NEGATIVE-ONLY
  imports VERIFICATION

  claim <k> Call(Name("string_sequence"), N:Int)
           => str(.IntSeq) </k>
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
    requires N <Int 0
endmodule

module AUDIT-NEGATIVE-BASE
  imports VERIFICATION-BASE

  claim <k> Call(Name("string_sequence"), N:Int)
           => str(.IntSeq) </k>
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
    requires N <Int 0
endmodule

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

module AUDIT-POSITIVE-ONLY
  imports VERIFICATION

  claim <k> Call(Name("string_sequence"), N:Int)
           => str(sequenceCodes(N)) </k>
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
