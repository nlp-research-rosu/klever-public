requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION

  claim <k>
          #loop(str(CS:IntSeq), Name("char"), encryptLoopBody)
          => .K
        </k>
        <env> 1 </env>
        <scopes>
          0 |-> scope("encrypt" |-> encryptClosure, parent(-1))
          -1 |-> builtinsScope
          (1 |-> scope(
             ("result" |-> str(A:IntSeq))
             ("char" |-> OLD:Str)
             ("s" |-> str(INPUT:IntSeq)),
             parent(0))
           =>
           1 |-> scope(
             ("result" |-> str(encryptAcc(A, CS)))
             ("char" |-> lastChar(CS, OLD))
             ("s" |-> str(INPUT)),
             parent(0)))
        </scopes>
        <heap> .Map </heap>
endmodule

module FUNCTION-SPEC
  imports VERIFICATION-WITH-LOOP

  claim <k>
          Call(Name("encrypt"), str(CS:IntSeq))
          => str(encryptCodes(CS))
        </k>
        <env> 0 </env>
        <scopes>
          0  |-> scope("encrypt" |-> encryptClosure, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
endmodule
