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
